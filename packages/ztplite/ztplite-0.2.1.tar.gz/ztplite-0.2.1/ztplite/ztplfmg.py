import os
import sys
import datetime
from . import ztpllogging
import base64
import time
import json
from pyFMG.fortimgr import FortiManager, FMGBaseException, FMGConnectionError
from abc import ABC, abstractmethod
from enum import IntEnum
from logging import Formatter, FileHandler, INFO
from jinja2 import Template


class CustomResponseCode(IntEnum):
    """
    Basic ENUM to provide code response codes that can be utilized by the caller.
        - SUCCESS = 0
        - NON_SUCCESS = -100000
        - GEN_EXCEPTION = -100001
        - KEY_NOT_EXIST = -100002
        - KEY_ERROR = -100003
        - TASK_EXCEPTION = -100004
    """
    SUCCESS = 0
    NON_SUCCESS = -100000
    GEN_EXCEPTION = -100001
    KEY_NOT_EXIST = -100002
    KEY_ERROR = -100003
    TASK_EXCEPTION = -100004


class TaskTimedOutException(Exception):
    """Used to maintain details on if a task did not finish in time"""

    def __init__(self, *args):
        super(TaskTimedOutException, self).__init__(*args)


class TaskReportedErrorException(Exception):
    """Used to maintain details on if a task did not finish in time"""

    def __init__(self, *args):
        super(TaskReportedErrorException, self).__init__(*args)


class ZTPConnectionError(FMGConnectionError):
    """Simple wrapper for connection error issues"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BaseFMGAction(ABC):
    """
    The BaseClass for an action that will be encapsulated for the ZTP FMG. This is an abstract base class and is not meant to be instantiated as a concrete class but provides the perform method which is where action is meant to take place in the command

    :param ztplfmg: Reference to the FMG
    :type ztplfmg: ZTPLFortiManager
    """

    def __init__(self, ztplfmg):
        super().__init__()
        self._fmg = ztplfmg
        self._logger = ztpllogging.get_logger()
        self._dev_name = ""
        self._adom = ""

    @property
    def ext_logger(self):
        """
        Get property to retrieve logging instance

        :return: A ZTPLLogging instance for logging perform function activity
        :rtype: ZTPLLogging
        """
        return self._logger

    @ext_logger.setter
    def ext_logger(self, logger):
        """
        Setter to set logging capability

        :param logger: ZTPLogging instance utilized to log perform function activity
        :type logger: ZTPLLogging
        """
        self._logger = logger

    @staticmethod
    def non_success_code_warning_str(class_name, code, *args):
        """
        Standard static function that returns a string denoting the fact that a code that was not 0 was returned

        :param class_name: Class name that has the issue
        :type class_name: str
        :param code: Code provided by FMG
        :type code: int
        :param args: Used in case specific information needs to be added to the default string. Helps with loops that have information that needs to be spelled out even more than the default
        :type args: str list
        :return: Static string denoting a consistent logging capability for code responses that are not 0
        :rtype: str
        """
        return f"While the {class_name} was performing its function the FMG returned a response code that indicated " \
               f"a non-successful response. Normally this means that data provided to the FMG was not correct for " \
               f"the call at hand. The data will be returned but likely the response does not contain the required " \
               f"data. The code returned from the FMG was {code}. " \
               f"{' Specifics are: ' + '. '.join(args) if args else ''}"

    @staticmethod
    def not_proper_parameter_info_str(class_name, device_name, *args):
        """
        Standard static function that returns a string denoting the fact that the required information to make the call was not provded as a parameter

        :param class_name: Class name that has the issue
        :type class_name: str
        :param device_name: Name of the device that is being provisioned during the exception
        :type device_name: str
        :return: Static string denoting a consistent logging capability for when perform is called on a class without the correct input information
        :rtype: str
        """
        return f"Information required to ensure the correct data was retrieved from the FMG was not presented to " \
               f"the process being performed by {class_name} while working on device {device_name}." \
               f"{' Specifics are: ' + '. '.join(args) if args else ''}"

    @staticmethod
    def task_exception_warning_str(class_name, device_name, *args):
        return f"Task exception encountered during a process being performed by {class_name} on " \
               f"device {device_name}. {' Specifics are: ' + '. '.join(args) if args else ''}"

    @staticmethod
    def generic_exception_warning_str(class_name, device_name, *args):
        return f"A generic exception was encountered during a process being performed by {class_name} " \
               f"on {device_name}. {' Specifics are: ' + '. '.join(args) if args else ''}"

    @abstractmethod
    def perform(self, **kwargs):
        """
        Abstract method used to perform some activity on the FMG

        :param kwargs: Key word arguments needed for the perform function to work when key-words are required
        :return: Return (code, result) consisting of the code returned as the first element and a result object dictionary or None
        :rtype: tuple
        """
        pass

    def handle_task_run(self, result_dict, proc_name, fgt_name, sleep_time=5, retrieval_fail_gate=10, timeout=120):
        """
        Function to handle all aspects of a task's process

        :param result_dict: Result of the call to the FMG returning a response about the task being monitored
        :type result_dict: dict
        :param proc_name: Name of the calling class
        :type proc_name: str
        :param fgt_name: FGT name that the FMG is working on for this task
        :type fgt_name: str
        :param sleep_time: Number of seconds to sleep between each task call. Default is 5 seconds
        :type sleep_time: int
        :param retrieval_fail_gate: Number of times a non-zero code response from a Task request is allowed. This is to ensure the task even exists and will give the FMG time to catch up if it is having issues. The Default is 10 times, but this is seldom used or changed
        :type retrieval_fail_gate: int
        :param timeout: Number of seconds that the Task is allowed to run before timing out. Default is 120 seconds, which is fine for most tasks, however for tasks such as Upgrading this may need to be upped significantly
        :type timeout: int
        :return: Return (code, result) tuple from FMG task consisting of the code returned as the first element and a result object dictionary
        :rtype: tuple
        :raises: FMGBaseException if no task id is found in the result_dict parameter or task id is found to be None. Also raised if a reply from a task call within the loop comes back with a num_err attribute missing entirely
        :raises: TaskTimedOutException if a task continues to run past the task timout time set in the PyFMG module
        :raises: TaskReportedErrorException if a call to the task returns with the num_err attribute having a value other than 0
        """
        if "task" in result_dict or "taskid" in result_dict:
            task_id = result_dict.get("task")
            if task_id is None:
                task_id = result_dict.get("taskid")
        else:
            self.ext_logger.error(f"Error encountered during {proc_name} while provisioning {fgt_name}. "
                                  f"The task was either not created or not formatted correctly. "
                                  f"Terminating...please check issue manually")
            raise FMGBaseException
        if task_id is not None:
            task_code, task_res = self._fmg.track_task(task_id, sleep_time, retrieval_fail_gate, timeout)
            if task_code == 1:
                self.ext_logger.error(f"Error encountered during {proc_name} while provisioning {fgt_name}. "
                                      f"The task more than likely did not finish in time or correctly and as such "
                                      f"the process failed. Terminating...please check issue manually. "
                                      f"The Task ID is {task_id}")
                raise TaskTimedOutException
            elif task_code == 0:
                number_err = task_res.get("num_err")
                if number_err is None:
                    self.ext_logger.error(f"Error encountered during {proc_name} while provisioning {fgt_name}. "
                                          f"The task completed, but was not formatted correctly upon completion and "
                                          f"had no report on if there were errors within the process or not. "
                                          f"Terminating...please check issue manually. The Task ID is {task_id}")
                    raise FMGBaseException(f"Response returned did not have proper data to find task info")
                elif number_err != 0:
                    self.ext_logger.error(f"Error encountered during {proc_name} while provisioning {fgt_name}. "
                                          f"The task completed, but reported that there was an error during the run. "
                                          f"The number of errors reported is {number_err}. Terminating...please "
                                          f"check issue manually. The Task ID is {task_id}")
                    raise TaskReportedErrorException(f"Number of errors was {number_err}")
                else:
                    # return in case code wants to use task output
                    return task_code, task_res
        else:
            self.ext_logger.error(f"Error encountered during {proc_name} while provisioning {fgt_name}. "
                                  f"The task result from the create task process does not seem to have created a "
                                  f"sufficient task. Terminating...please check issue manually")
            raise FMGBaseException

    def handle_standard_exceptions(func):
        """
        Utilized as a decorator for all BaseFMGAction perform() functions. This wraps the functions in
        try..except blocks that catch the most problematic issues so the code does not need to be repeated on each
        Action

        :param func: Original perform() function reference
        :type func: function
        :return: Decorator function reference
        :rtype: function
        """
        def wrap_action(self, **kwargs):
            ext_logger = ztpllogging.get_logger()
            if not kwargs:
                ext_logger.error(BaseFMGAction.not_proper_parameter_info_str(func.__class__.__name__,
                                                                             "No device name provided"))
                return CustomResponseCode.KEY_NOT_EXIST, None
            dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            try:
                return func(self, **kwargs)
            except KeyError as ke:
                ext_logger.error(BaseFMGAction.not_proper_parameter_info_str(func.__class__.__name__,
                                                                             dev_name, str(ke)))
                return CustomResponseCode.KEY_ERROR, None
            except (FMGBaseException, TaskReportedErrorException, TaskTimedOutException) as ex:
                ext_logger.error(BaseFMGAction.task_exception_warning_str(func.__class__.__name__, dev_name, str(ex)))
                return CustomResponseCode.TASK_EXCEPTION, None
            except:
                ext_logger.error(BaseFMGAction.generic_exception_warning_str(func.__class__.__name__, dev_name))
                return CustomResponseCode.GEN_EXCEPTION, None
        return wrap_action

    handle_standard_exceptions = staticmethod(handle_standard_exceptions)


class ZTPLFortiManager(FortiManager):
    """
    Class utilized to embody functions that the FMG provides. ZTPLFortiManager utilizes pyFMG as a backend solution,
    but provides functions specific to ZTP

    :param host: IP Address or FQDN of FMG
    :type host: str
    :param user: Username of API user. Default is empty string
    :type user: str
    :param passwd: Password of API user. Default is empty string
    :type passwd: str
    :param debug: Sets debug options for FMG. If debug is set to true logging of all FMG actions will take place and be placed within the debug log
    :type debug: bool
    :param use_ssl: Mandates whether the FMG connection will use SSL. Default is True
    :type use_ssl: bool
    :param verify_ssl: Mandates whether the connection will verify the certificate on the FMG. Default is False
    :type verify_ssl: bool
    :param timeout: Timeout setting of the connection object that will connect to the FMG. Default is 300 seconds
    :type timeout: int
    :param disable_request_warnings: Mandates whether the connection request will log warnings about errors/exceptions. Default is False
    :type disable_request_warnings: bool
    """

    def __init__(self, host=None, user="", passwd="", debug=False, use_ssl=True,
                 verify_ssl=False, timeout=300, disable_request_warnings=False):
        super().__init__(host, user, passwd, debug, use_ssl, verify_ssl, timeout, disable_request_warnings)
        self._debug = debug

    def set_debug_logger(self, log_loc,
                         fmt=Formatter("%(asctime)s - %(name)s: %(message)s ", "%m/%d/%Y %I:%M:%S %p"),
                         *args):
        """
        Sets the logger for debug information from the FMG. By default this is a FileHandler located at log_loc.

        :param log_loc: Location for the default debug log handler
        :type log_loc: str
        :param fmt: Formatter for default log handler. Default is "%(asctime)s - %(name)s: %(message)s ", "%m/%d/%Y %I:%M:%S %p"
        :type fmt: logging.Formatter
        :param args: Args list of handlers added to FMG debug log capability
        """
        if self._debug:
            if args:
                for log_obj in args:
                    self.addHandler(log_obj)
            else:
                self.getLog("fmg.debug", INFO)
                fh = FileHandler(log_loc)
                fh.setLevel(INFO)
                fh.setFormatter(fmt)
                self.addHandler(fh)

    def get_unauthorized_devices(self):
        """
        Function that utilizes the FMG instance (self) and does a call to get all unregistered FGT devices

        :return: CustomResponse code that identifies if the process was successful, and the unregistered devices that were found (if any) in the format {fgt_sn: fgt_name, fgt_sn: fgt_name}. If there are no items found in the unregistered device API response, None is returned in place of the dictionary
        :rtype: tuple
        """
        ext_logger = ztpllogging.get_logger()
        try:
            ext_logger.info(f"Retrieving unregistered devices from FMG")
            code, res = self.get("/dvmdb/device", fields=["name", "sn"], filter=["mgmt_mode", "==", "UNREG"], loadsub=0)
            if code == CustomResponseCode.SUCCESS:
                if res:
                    if len(res) > 0:
                        unreg_dict_of_fgts = {n["sn"]: n["name"] for n in res if "fg" in n["sn"].lower()}
                        ext_logger.info(f"Found the following serial numbers as unregistered "
                                        f"devices: {', '.join(list(unreg_dict_of_fgts))}")
                        return code, unreg_dict_of_fgts
                else:
                    return CustomResponseCode.SUCCESS, {}
            else:
                ext_logger.warning(BaseFMGAction.non_success_code_warning_str("get_unauthorized_devices", code))
            return CustomResponseCode.NON_SUCCESS, None
        except:
            ext_logger.error(f"An exception was handled during the operation to retrieve unregistered devices "
                             f"from FMG. FMG possibly is not accessible or the credentials provided are "
                             f"incorrect.")
            return CustomResponseCode.GEN_EXCEPTION, None

    class AssignToDeviceGroups(BaseFMGAction):
        """
        Uses 'devicename', 'adom', and 'grouplists.groups_list'  k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to make a FGT a member of the Device Group(s)**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', and 'grouplists'  k:v information
            Instructs the FMG to make a FGT a member of the Device Group(s)

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'devicename', 'adom', and 'group_lists'  k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"groups": ["grp_name", "grp_name"]]}) of all unregistered devices found during the perform function call or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            successful_runs = []
            all_success = True
            for group in kwargs.get("configuration", {}).get("group_lists", []):
                self.ext_logger.info(f"Attempting to add FGT {self._dev_name} to the {group} device group")
                code, res = self._fmg.add(f"/dvmdb/adom/{self._adom}/group/{group}/object member",
                                          data=[{"name": self._dev_name, "vdom": "root"}])
                if code == CustomResponseCode.SUCCESS:
                    self.ext_logger.info(f"FGT {self._dev_name} added successfully to the {group} device group")
                    successful_runs.append(group)
                else:
                    all_success = False
                    self.ext_logger.warning(
                        BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code,
                                                                   f"Group name affected is {group}"))
            if all_success:
                return CustomResponseCode.SUCCESS, {"groups": successful_runs}
            else:
                return CustomResponseCode.NON_SUCCESS, {"groups": successful_runs}

    class AssignMetaData(BaseFMGAction):
        """
        Uses 'devicename', 'adom', and 'meta' (metadata dictionary)  k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to update a device's metadata with values that are sent from the configuration file**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        def check_and_add_metadata(self, meta_required_hash, **kwargs):
            """
            Instructs the FMG to add Metadata fields if they are not already in the FMG Database

            :param meta_required_hash: Dictionary describing metadata that needs to updated on the FMG
            :type meta_required_hash: dict
            :param kwargs: FGT configuration dictionary pass from the internal perform function
            :type kwargs: dict
            :return: CustomResponseCode describing success or not
            :rtype: CustomResponseCode
            """
            code, res = self._fmg.get(f"/dvmdb/adom/{self._adom}/device/{self._dev_name}", option=["get meta"],
                                      fields=["meta fields"])
            try:
                meta_field_required_hash_list = [
                    {"data": {"name": meta, "importance": "optional", "length": 255, "status": 1},
                     "url": "/dvmdb/_meta_fields/device"} for meta in list(meta_required_hash.keys()) if
                    meta not in list(res["meta fields"].keys())]
                if meta_field_required_hash_list:
                    code, res = self._fmg.free_form("add", data=meta_field_required_hash_list)
                    if code == CustomResponseCode.SUCCESS:
                        self.ext_logger.info(f"Metadata attribute(s) successfully added to the FMG")
                        return CustomResponseCode.SUCCESS
                else:
                    self.ext_logger.info(f"Metadata attribute(s) were not required to be added to the FMG")
                    return CustomResponseCode.SUCCESS
            except:
                self.ext_logger.error("Error encountered when adding metadata")
            return CustomResponseCode.NON_SUCCESS

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', and 'meta' (metadata dictionary)  k:v information
            Instructs the FMG to update a device's metadata with values that are sent from the configuration file

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'devicename', 'adom', and 'meta' (metadata dictionary)  k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"meta fields": meta_hash_none_removed}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            meta_hash = kwargs.get("meta", {})
            # ensure all are strings
            for k, v in meta_hash.items():
                meta_hash[k] = str(v)
            if meta_hash:
                # ensure anything with value of None or empty string is removed
                meta_hash_none_removed = {k: v for k, v in meta_hash.items() if v != "None" and v != ""}
                if meta_hash_none_removed:
                    # check if any metadata needs to be added to the FMG
                    self.ext_logger.info(f"Checking if metadata attributes need to be added to FMG")
                    code = self.check_and_add_metadata(meta_hash_none_removed, **kwargs)
                    if code == CustomResponseCode.SUCCESS:
                        self.ext_logger.info(f"Attempting to update FGT {self._dev_name}'s metadata info")
                        code, res = self._fmg.update(f"/dvmdb/adom/{self._adom}/device/{self._dev_name}",
                                                     meta___fields=meta_hash_none_removed)
                        if code == CustomResponseCode.SUCCESS:
                            self.ext_logger.info(f"Added metadata values successfully to {self._dev_name}")
                            return CustomResponseCode.SUCCESS, {"meta fields": meta_hash_none_removed}
                        else:
                            self.ext_logger.error(
                                BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
                            return CustomResponseCode.NON_SUCCESS, None
            return CustomResponseCode.NON_SUCCESS, None

    class ChangePassword(BaseFMGAction):
        """
        Uses 'devicename', 'adom', and 'device_pw' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to update a device's password both on the device and on the FMG device db**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', and 'device_pw' k:v information
            Instructs the FMG to update a device's password both on the device and on the FMG device db

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'devicename', 'adom', and 'device_pw' k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"success": True}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            dev_pw = kwargs.get("configuration", {}).get("device_pw")
            if dev_pw is not None:
                self.ext_logger.info(f"Attempting to change the password on FGT {self._dev_name}")
                code, res = self._fmg.update(f"/dvmdb/adom/{self._adom}/device/{self._dev_name}", adm_pass=dev_pw)
                if code == CustomResponseCode.SUCCESS:
                    self.ext_logger.info(f"Password changed on the FMG Device DB for FGT {self._dev_name}")
                    self.ext_logger.info(f"Password change now being attempted on FGT {self._dev_name} directly")
                    pword_script_text = f"config system admin\nedit admin\nset password {dev_pw}\nnext\nend"
                    script_name = f"{self._dev_name}_pword"
                    code, res = self._fmg.set(f"/dvmdb/adom/{self._adom}/script/", content=pword_script_text,
                                              name=script_name, type="cli", target="remote_device")
                    if code == CustomResponseCode.SUCCESS:
                        self.ext_logger.info(f"Script {script_name} has been created on the FMG. Executing script on "
                                             f"FGT {self._dev_name}")
                        code, res = self._fmg.execute(f"/dvmdb/adom/{self._adom}/script/execute", script=script_name,
                                                      adom=self._adom, scope=[{"name": self._dev_name, "vdom": "root"}])
                        self.handle_task_run(res, type(self).__name__, self._dev_name)
                        self.ext_logger.info(f"Password script {script_name} run successfully on FGT {self._dev_name}")
                        self.ext_logger.info(f"Attempting deletion of script {script_name} from FMG")
                        code, res = self._fmg.delete(f"/dvmdb/adom/{self._adom}/script/{script_name}")
                        if code == CustomResponseCode.SUCCESS:
                            self.ext_logger.info(f"The script {script_name} was deleted successfully from the FMG")
                            return CustomResponseCode.SUCCESS, {"success": True}
                        else:
                            self.ext_logger.warning(
                                f"The script {script_name} was not deleted successfully from the FMG. Please check the "
                                f"FMG manually and delete this script. Processing will continue.")
                    else:
                        self.ext_logger.warning(f"Password change directly on FGT {self._dev_name} did not complete "
                                                f"successfully. The FMG Device DB and the local FGT passwords do not "
                                                f"match. Please correct this manually or the FMG may have issues with "
                                                f"future actions on this FGT.")
            return CustomResponseCode.NON_SUCCESS, None

    class ApplyPolPkg(BaseFMGAction):
        """
        Uses 'devicename', pol_pkg, 'adom', and 'vdom_list' (if more vdoms than root) k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to apply a policy package to a device**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', pol_pkg, 'adom', and 'vdom_list' (if more vdoms than root) k:v information
            Instructs the FMG to apply a policy package to a device

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'devicename', pol_pkg, 'adom', and 'vdom_list' (if more vdoms than root) k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"pol_pkg": kwargs["pol_pkg"]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            pol_pkg = kwargs.get("templates", {}).get("pol_pkg")
            scope = [{"name": self._dev_name, "vdom": "root"}]
            # handle vdoms
            if kwargs.get('vdom_lists', []):
                scope = [{"name": self._dev_name, "vdom": vdom} for vdom in kwargs.get("vdom_lists", [])]
            self.ext_logger.info(f"Attempting to assign FGT {self._dev_name} as a target of the pol package {pol_pkg}")
            code, res = self._fmg.add(f"/pm/pkg/adom/{self._adom}/{pol_pkg}/scope member", data=scope)
            if code == CustomResponseCode.SUCCESS:
                self.ext_logger.info(f"FGT {self._dev_name} has been added as a target of the policy package {pol_pkg} "
                                     f"successfully")
                return CustomResponseCode.SUCCESS, {"pol_pkg": pol_pkg}
            else:
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            return CustomResponseCode.NON_SUCCESS, None

    class AssignSDWANTemplate(BaseFMGAction):
        """
        Uses 'devicename', 'adom', 'sd_wan', and 'vdom_list' (if more vdoms than root) k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to add a device as a target of an SDWAN template**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', 'sd_wan', and 'vdom_list' (if more vdoms than root) k:v information
            Instructs the FMG to add a device as a target of an SDWAN template

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'devicename', 'adom', 'sd_wan', and 'vdom_list' (if more vdoms than root) k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"sd_wan": kwargs["sd_wan"]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            sd_wan = kwargs.get("templates", {}).get("sd_wan")
            # handle vdoms
            scope = [{"name": self._dev_name, "vdom": "root"}]
            if kwargs.get('vdom_lists', []):
                scope = [{"name": self._dev_name, "vdom": vdom} for vdom in kwargs.get("vdom_lists", [])]
            self.ext_logger.info(f"Attempting to assign FGT {self._dev_name} as a target of the SD-WAN template "
                                 f"{sd_wan}")
            sdwan_add_info = [
                {
                    "data": scope,
                    "url": f"/pm/wanprof/adom/{self._adom}/{sd_wan}/scope member",
                }
            ]
            code, res = self._fmg.free_form("add", data=sdwan_add_info)
            if code == CustomResponseCode.SUCCESS:
                self.ext_logger.info(f"FGT {self._dev_name} has been added as a target of the SD-WAN template {sd_wan} "
                                     f"successfully")
                return CustomResponseCode.SUCCESS, {"sd_wan": sd_wan}
            else:
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            return CustomResponseCode.NON_SUCCESS, None

    class InstallPolicyPackage(BaseFMGAction):
        """
        Uses 'pol_pkg', 'adom', 'devicename', 'vdom_list' (if more vdoms) k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to execute the installation of a policy package on a device**

        """
        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'pol_pkg', 'adom', 'devicename', 'vdom_list' (if more vdoms) k:v information
            Instructs the FMG to execute the installation of a policy package on a device

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'pol_pkg', 'adom', 'devicename', 'vdom_list' (if more vdoms) k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"scope": scope, "pol_pkg": kwargs["pol_pkg"]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            pol_pkg = kwargs.get("templates", {}).get("pol_pkg")
            # handle vdoms
            scope = [{"name": self._dev_name, "vdom": "root"}]
            if kwargs.get('vdom_lists', []):
                scope = [{"name": self._dev_name, "vdom": vdom} for vdom in kwargs.get("vdom_lists", [])]
            self.ext_logger.info(f"Attempting the installation of Policy Package {pol_pkg}")
            code, res = self._fmg.execute("securityconsole/install/package", adom=self._adom, scope=scope, pkg=pol_pkg)
            if code == CustomResponseCode.SUCCESS:
                self.ext_logger.info(f"Policy Package {pol_pkg} has been set for execution on FGT {self._dev_name}")
                self.handle_task_run(res, type(self).__name__, self._dev_name)
                self.ext_logger.info(f"Policy Package {pol_pkg} reported successful completion on FGT {self._dev_name}")
                return CustomResponseCode.SUCCESS, {"scope": scope, "pol_pkg": pol_pkg}
            self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            return CustomResponseCode.NON_SUCCESS, None

    class ExecuteCLITemplateGrp(BaseFMGAction):
        """
        Uses 'cli_template_groups.name', 'adom', 'devicename', and 'vdom_list' (if more vdoms) k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to assign a CLI Template Group, execute it (if told to do so in the configuration information), and then remove it from assignment (again if told to do so in the configuration information) on a device**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'cli_template_groups.name', 'adom', 'devicename', and 'vdom_list' (if more vdoms) k:v information
            Instructs the FMG to assign a CLI Template Group, execute it (if told to do so in the configuration information), and then remove it from assignment (again if told to do so in the configuration information) on a device

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'cli_template_groups.name', 'adom', 'devicename', and 'vdom_list' (if more vdoms) k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"template_groups": [list of templates run]]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            scope = [{"name": self._dev_name, "vdom": "root"}]
            cli_temp_grps = kwargs.get("templates", {}).get("cli_template_groups", {}).get("cltg", [])
            # handle vdoms
            if kwargs.get('vdom_lists', []):
                scope = [{"name": self._dev_name, "vdom": vdom} for vdom in kwargs.get("vdom_lists", [])]
            self.ext_logger.info(f"Attempting the execution of CLI template group{'s' if cli_temp_grps else ''}")
            successful_runs = []
            all_success = True
            for cli_template_group in cli_temp_grps:
                code, res = self._fmg.add(f"/pm/config/adom/{self._adom}/obj/cli/template-group/"
                                          f"{cli_template_group['name']}/scope member", data=scope)
                if code == CustomResponseCode.SUCCESS:
                    self.ext_logger.info(f"FGT {self._dev_name} has been added as a target to "
                                         f"{cli_template_group['name']}")
                    if cli_template_group["execute"][0].lower() == "y":
                        code, res = self._fmg.execute(f"securityconsole/install/device",
                                                      scope=scope, adom=self._adom, flags=["install_chg", ])
                        if code == CustomResponseCode.SUCCESS:
                            self.ext_logger.info(f"CLI Template Group {cli_template_group['name']} has been set for "
                                                 f"execution on FGT {self._dev_name}")
                            self.handle_task_run(res, type(self).__name__, self._dev_name)
                            self.ext_logger.info(f"CLI Template Group {cli_template_group['name']} reported successful "
                                                 f"completion on FGT {self._dev_name}")
                            successful_runs.append(cli_template_group)
                        else:
                            all_success = False
                            self.ext_logger.warning(
                                BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code,
                                                                           f"Template group affected is "
                                                                           f"{cli_template_group}"))
                    else:
                        self.ext_logger.info(f"The CLI Template Group {cli_template_group['name']} is not set to "
                                             f"execute")
                        continue  # no use checking if one that is set not to execute should be deleted
                else:
                    all_success = False
                    self.ext_logger.warning(
                        BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code,
                                                                   f"Template group affected is "
                                                                   f"{cli_template_group}"))
                    continue  # no use checking if one that is set not to execute should be deleted
                # if not marked to remain delete it. if remain not on this object consider it needing to be removed
                try:
                    if cli_template_group["remain"][0].lower() == "n":
                        code, res = self._fmg.delete(f"/pm/config/adom/{self._adom}/obj/cli/"
                                                     f"template-group/{cli_template_group['name']}/scope member",
                                                     data=scope)
                        if code == CustomResponseCode.SUCCESS:
                            self.ext_logger.info(f"FGT {self._dev_name} has been removed as a target for "
                                                 f"{cli_template_group['name']}")
                    else:
                        self.ext_logger.info(f"FGT {self._dev_name} remains as a target to {cli_template_group['name']} "
                                             f"as instructed by the configuration")
                except (KeyError, IndexError):
                    code, res = self._fmg.delete(f"/pm/config/adom/{self._adom}/obj/cli/template-group/"
                                                 f"{cli_template_group['name']}/scope member", data=scope)
                    if code == CustomResponseCode.SUCCESS:
                        self.ext_logger.info(f"FGT {self._dev_name} has been removed as a target for "
                                             f"{cli_template_group['name']}")
            if all_success:
                return CustomResponseCode.SUCCESS, {"template_groups": successful_runs}
            else:
                return CustomResponseCode.NON_SUCCESS, {"template_groups": successful_runs}

    class ExecuteCLIScriptGrp(BaseFMGAction):
        """
        Uses 'cli_script_groups.name', 'adom' 'devicename', 'vdom_list' (if more vdoms), and pol_pkg (if run on pp) k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to execute a CLI Script Group on the FMG**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'cli_script_groups.name', 'adom' 'devicename', 'vdom_list' (if more vdoms), and pol_pkg (if run on pp) k:v information
            Instructs the FMG to execute a CLI Script Group on the FMG

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'cli_script_groups.name', 'adom' 'devicename', 'vdom_list' (if more vdoms), and pol_pkg (if run on pp) k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"scripts_groups": [successful script group list]]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            scope = [{"name": self._dev_name, "vdom": "root"}]
            cli_script_grps = kwargs.get("templates", {}).get("cli_script_groups", {}).get("clsg", [])
            # handle vdoms
            if kwargs.get('vdom_lists', []):
                scope = [{"name": self._dev_name, "vdom": vdom} for vdom in kwargs.get("vdom_lists", [])]
            successful_runs = []
            all_success = True
            for cli_script in cli_script_grps:
                self.ext_logger.info(f"Attempting the execution of CLI script group {cli_script}")
                if kwargs.get("templates", {}).get("pol_pkg", False):
                    pol_pkg = kwargs.get("templates", {}).get("pol_pkg", False)
                    code, res = self._fmg.execute(f"/dvmdb/adom/{self._adom}/script/execute", script=cli_script,
                                                  adom=self._adom, scope=scope, package=pol_pkg)
                else:
                    code, res = self._fmg.execute(f"/dvmdb/adom/{self._adom}/script/execute", script=cli_script,
                                                  adom=self._adom, scope=scope)
                if code == CustomResponseCode.SUCCESS:
                    self.ext_logger.info(f"CLI script {cli_script} has been set for "
                                         f"execution during FGT {self._dev_name}'s provisioning process")
                    self.handle_task_run(res, type(self).__name__, self._dev_name)
                    self.ext_logger.info(f"CLI script {cli_script} reported successful completion during FGT "
                                         f"{self._dev_name}'s provisioning process")
                    successful_runs.append(cli_script)
                else:
                    all_success = False
                    self.ext_logger.warning(
                        BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code,
                                                                   f"Script group affected is {cli_script}"))
            if all_success:
                return CustomResponseCode.SUCCESS, {"scripts_groups": successful_runs}
            else:
                return CustomResponseCode.NON_SUCCESS, {"scripts_groups": successful_runs}

    class ExecuteLocalCLIScript(BaseFMGAction):
        """
        Uses 'local_cli_scripts.groupname', 'local_cli_scripts.location', 'adom' and 'devicename', 'pol_pkg' (if running on policy package), and 'vdom_list' (if more vdoms) k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to find a local script in a location on the local directory, render the script using Jinja2, apply it to the FMG and then either execute it directly on a device, on a device db, or on a pol pkg on the FMG based on the configuration file setting and then delete the script
        'local_cli_scripts.scripts_location will default to a directory local to script path/local_scr/**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)
            self._created_scripts = []

        def __script_exists(self, path):
            if os.path.exists(path):
                return True
            else:
                self.ext_logger.error(f"Error encountered during execution processes on {self._dev_name}. "
                                      f"The location for scripts is set for {path} but does not exist. "
                                      f"Please ensure the script repository on the automation machine is "
                                      f"in the correct location and the correct scripts are created and named "
                                      f"appropriately. Terminating...please check issue manually")
                return False

        def __delete_scripts(self, scripts_created):
            if len(scripts_created) > 0:
                for script_name_on_fmg in scripts_created:
                    code, res = self._fmg.delete(
                        f"/dvmdb/adom/{self._adom}/script/{script_name_on_fmg}")
                    if code == CustomResponseCode.SUCCESS:
                        self.ext_logger.info(
                            f"The script {script_name_on_fmg} was deleted successfully from the FMG")
                    else:
                        self.ext_logger.warning(
                            f"The script {script_name_on_fmg} was not deleted successfully from the FMG. "
                            f"Please check the FMG manually and delete this script. Deletion process will "
                            f"continue, as this is not seen as a critical failure")

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'local_cli_scripts.groupname', 'local_cli_scripts.location', 'adom' and 'devicename', 'pol_pkg' (if running on policy package), and 'vdom_list' (if more vdoms) k:v information
            Instructs the FMG to find a local script in a location on the local directory, render the script using Jinja2, apply it to the FMG and then either execute it directly on a device, on a device db, or on a pol pkg on the FMG based on the configuration file setting and then delete the script
            'local_cli_scripts.scripts_location will default to a directory local to script path/local_scr/

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'local_cli_scripts.groupname', 'local_cli_scripts.location', 'adom' and 'devicename', 'pol_pkg' (if running on policy package), and 'vdom_list' (if more vdoms) k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"local_scripts": [successful local scripts that were run]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            local_script_location = kwargs.get("local_script_location")
            scope = [{"name": self._dev_name, "vdom": "root"}]
            local_cli_scripts = kwargs.get("templates", {}).get("local_cli_scripts", {}).get("lcs", [])
            # handle vdoms
            if kwargs.get('vdom_lists', []):
                scope = [{"name": self._dev_name, "vdom": vdom} for vdom in kwargs.get("vdom_lists", [])]
            # need a reference to this if object dies
            successful_runs = []
            scripts_created = []
            all_success = True
            for local_cli_script in local_cli_scripts:
                script_loc = os.path.join(str(local_script_location), str(local_cli_script.get("name", "")))
                if not self.__script_exists(script_loc):
                    all_success = False
                    return CustomResponseCode.NON_SUCCESS, None
                script_name_on_fmg = f"{local_cli_script['name']}_{datetime.datetime.now().microsecond}"
                target = local_cli_script.get("run_on", "").lower()
                if target == "db" or target == "device_db":
                    target = "device_database"
                elif target == "pol_pkg" or target == "pp" or target == "adom" or target == "adom_database":
                    target = "adom_database"
                else:
                    target = "remote_device"
                template_out = ""
                with open(script_loc, "r", encoding="utf-8-sig") as scr_fil:
                    script_contents = scr_fil.read()
                    template_out = Template(script_contents).render(**kwargs)
                code, res = self._fmg.set(f"/dvmdb/adom/{self._adom}/script/", content=template_out,
                                          name=script_name_on_fmg, type="cli", target=target)
                if code == CustomResponseCode.SUCCESS:
                    pol_pkg = kwargs.get("templates", {}).get("pol_pkg", "")
                    scripts_created.append(script_name_on_fmg)
                    self.ext_logger.info(f"Script {script_name_on_fmg} has been created on the FMG and is being "
                                         f"executed")
                    if target == "adom_database":
                        code, res = self._fmg.execute(f"/dvmdb/adom/{self._adom}/script/execute", adom=self._adom,
                                                      script=script_name_on_fmg, package=pol_pkg, scope=scope,
                                                      flags=["create_task", "nonblocking"])
                    else:
                        code, res = self._fmg.execute(f"/dvmdb/adom/{self._adom}/script/execute", adom=self._adom,
                                                      script=script_name_on_fmg, scope=scope,
                                                      flags=["create_task", "nonblocking"])
                    try:
                        self.handle_task_run(res, type(self).__name__, self._dev_name)
                        self.ext_logger.info(f"CLI script {script_name_on_fmg} run successfully during FGT "
                                             f"{self._dev_name} provisioning")
                        successful_runs.append(script_name_on_fmg)
                    except (TaskReportedErrorException, TaskTimedOutException, FMGBaseException):
                        self.ext_logger.warning(f"Due to the previous exception that was logged, the script that had "
                                                f"issues - {script_name_on_fmg} - will not be deleted. This should "
                                                f"give the author the capability to identify what the problem with "
                                                f"{script_name_on_fmg} is. However, after the process is over, the "
                                                f"script will need to be deleted manually")
                        try:
                            scripts_created.remove(script_name_on_fmg)
                        except ValueError:
                            self.ext_logger.warning(f"A removal attempt was made against a script that was not in the "
                                                    f"scripts_created collection. This is not harmful to the overall "
                                                    f"process but is indicative of a possible issue with the "
                                                    f"underlying concept. Report this warning to the developer if "
                                                    f"possible. The script name that was attempted to be removed was "
                                                    f"{script_name_on_fmg}")
                else:
                    all_success = False
                    self.ext_logger.error(f"The script {script_name_on_fmg} was not created successfully on the FMG. "
                                          f"Stopping execution of all cleanup scripts and terminating provisioning "
                                          f"process. Please check the FMG and this device manually")
            self.__delete_scripts(scripts_created)
            if all_success:
                return CustomResponseCode.SUCCESS, {"local_scripts": successful_runs}
            else:
                return CustomResponseCode.NON_SUCCESS, {"local_scripts": successful_runs}

    class InstallDevice(BaseFMGAction):
        """
        Uses 'adom', 'devicename', and 'vdom_list' (if more vdoms) k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to execute the installation of a device configuration on a device**
        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'adom', 'devicename', and 'vdom_list' (if more vdoms) k:v information
            Instructs the FMG to execute the installation of a device configuration on a device

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'adom', 'devicename', and 'vdom_list' (if more vdoms) k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"success": True}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            scope = [{"name": self._dev_name, "vdom": "root"}]
            # handle vdoms
            if kwargs.get('vdom_lists', []):
                scope = [{"name": self._dev_name, "vdom": vdom} for vdom in kwargs.get("vdom_lists", [])]
            code, res = self._fmg.execute(f"securityconsole/install/device", scope=scope, adom=self._adom,
                                          flags=["install_chg", ])
            if code == CustomResponseCode.SUCCESS:
                self.ext_logger.info(f"Device installation set for {self._dev_name}")
                self.handle_task_run(res, type(self).__name__, self._dev_name)
                self.ext_logger.info(f"Device installation on {self._dev_name} reported successful completion")
                return CustomResponseCode.SUCCESS, {"success": True}
            else:
                self.ext_logger.warning(
                    BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code, f"Device affected "
                                                                                              f"was {self._dev_name}"))
            return CustomResponseCode.NON_SUCCESS, None

    class DeleteDevice(BaseFMGAction):
        """
        Uses 'devicename' and 'adom' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to delete a FGT from the managed device list**
        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename' and 'adom' k:v information
            Instructs the FMG to delete a registered device from the FMG

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'devicename' and 'adom' k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"device": device name}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            self.ext_logger.info(f"Attempting the deletion of FGT {self._dev_name} from the {self._adom} ADOM")
            code, res = self._fmg.execute("dvm/cmd/del/dev-list", adom=self._adom,
                                          del__dev__member__list=[{"name": self._dev_name}])
            if code == CustomResponseCode.SUCCESS:
                self.ext_logger.info(f"FGT {self._dev_name} deleted as a managed device from the {self._adom} ADOM")
                return CustomResponseCode.SUCCESS, {"device": self._dev_name}
            else:
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            return CustomResponseCode.NON_SUCCESS, None

    class PromoteDevice(BaseFMGAction):
        """
        Uses 'serialnumber' and 'adom' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to promote an unregistered device to a specific adom**
        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'sn' and 'adom' k:v information
            Instructs the FMG to promote an unregistered device to a specific adom

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'sn' and 'adom' k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"device action": "promote_unreg", "mgmt_mode": "fmg", "name": name of fmg, "adm_usr": "admin"}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            ser_number = kwargs.get("sn")
            device = {
                "device action": "promote_unreg",
                "mgmt_mode": "fmg",
                "name": kwargs.get("discovered_hostname", ser_number),
                "adm_usr": "admin"
            }
            self.ext_logger.info(f"Attempting the promotion of FGT identified as {ser_number} to the {self._adom} ADOM")
            code, res = self._fmg.execute("/dvm/cmd/add/device", adom=self._adom, device=device,
                                          flags=["create_task", "nonblocking"])
            if code == CustomResponseCode.SUCCESS:
                self.handle_task_run(res, type(self).__name__, str(ser_number))
                self.ext_logger.info(f"FGT {self._dev_name} added as a managed device in the {self._adom} ADOM")
                return CustomResponseCode.SUCCESS, device
            else:
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            return CustomResponseCode.NON_SUCCESS, None

    class AssignDeviceName(BaseFMGAction):
        """
        Uses 'serialnumber', 'devicename', and 'adom' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to set the devicename of a device on the FMG so it can be used as a handle for the device throughout the provision process**
        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'serialnumber', 'devicename', and 'adom' k:v information
            Instructs the FMG to set the devicename of a device on the FMG so it can be used as a handle for the device throughout the provision process

            :param kwargs: FGT configuration dictionary required for the perform function. 'serialnumber', 'devicename', and 'adom' k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"name": kwargs["configuration"]["devicename"], "serialnumber": kwargs["serialnumber"]) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            ser_number = kwargs.get("sn")
            discovered_hostname = kwargs.get("discovered_hostname", ser_number)
            self.ext_logger.info(f"Attempting to update FGT with device name {self._dev_name} for the FGT identified "
                                 f"as {ser_number}")
            code, res = self._fmg.update(f"/dvmdb/adom/{self._adom}/device/{discovered_hostname}", name=self._dev_name)
            if code == CustomResponseCode.SUCCESS:
                self.ext_logger.info(f"FGT identified as {ser_number} after promotion had its device name on the "
                                     f"system changed to {self._dev_name} successfully")
                return CustomResponseCode.SUCCESS, {"name": self._dev_name, "serialnumber": ser_number}
            else:
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            return CustomResponseCode.NON_SUCCESS, None

    class CheckDeviceIsAlive(BaseFMGAction):
        """
        Uses 'devicename', 'adom', 'checkdevicetimer' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the application to check for a response from a get system status call on the FGT**
        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        def __fgt_responded(self, **kwargs):
            # WON'T WORK ON 5.6 FGTs
            inner_dict = {
                "action": "get",
                "resource": "/api/v2/monitor/system/status/select",
                "target": [f"adom/{self._adom}/device/{self._dev_name}"]
            }
            try:
                code, res = self._fmg.execute("sys/proxy/json", data=inner_dict)
                if code == CustomResponseCode.SUCCESS:
                    status = res[0]["response"].get("status", "failed")
                    if status == "success":
                        return {"success": True}
                return {"success": False}
            except:
                return {"success": False, "exception": True}

        def __delay_and_check(self, **kwargs):
            timed_out = True
            delay_after_process = int(kwargs.get("checkdevicetimer", {}).get("delay_after_process", 60))
            delay_per_check_cycle = int(kwargs.get("checkdevicetimer", {}).get("delay_per_check_cycle", 10))
            delay_max_check_times = int(kwargs.get("checkdevicetimer", {}).get("delay_max_check_times", 60))
            self.ext_logger.info(f"Allowing FGT {self._dev_name} time to finish the previous process. "
                                 f"Sleeping for {delay_after_process} secs")
            time.sleep(delay_after_process)
            for timehack in range(0, int(delay_max_check_times) + 1):
                self.ext_logger.info(f"Executing status lookup on FGT {self._dev_name}...this is "
                                     f"cycle: {timehack + 1}")
                fgt_responded_dict = self.__fgt_responded(**kwargs)
                if not fgt_responded_dict["success"]:
                    if fgt_responded_dict.get("exception", False):
                        timed_out = False
                        break
                    else:
                        time.sleep(delay_per_check_cycle)
                else:
                    timed_out = False
                    self.ext_logger.info(f"Rcvd response from status check on FGT {self._dev_name}. Inserting 10s "
                                         f"delay then continuing")
                    time.sleep(10.0)
                    break
            if timed_out:
                self.ext_logger.error(f"FGT {self._dev_name} never responded after a Check Device Is Alive "
                                      f"action was sent. This FGT is considered down and will probably not be able to "
                                      f"continue through any further processes. Check this FGT's connectivity")
                return {"success": False}
            return {"success": True}

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', 'timers.timer', k:v information
            Instructs the FMG to proxy an a call to the FGT looking just for a response. It then will wait and check the FGT's process based on what is set in timers in the configuration file

            :param kwargs: FGT configuration dictionary required for the perform function. 'devicename', 'adom', 'timers.timer', k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"target": kwargs["configuration"]["devicename"]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            if self.__delay_and_check(**kwargs)["success"]:
                self.ext_logger.info(f"FGT {self._adom} responded successfully. Continuing....")
                return CustomResponseCode.SUCCESS, {"target": self._dev_name}
            return CustomResponseCode.NON_SUCCESS, None

    class RebootDevice(BaseFMGAction):
        """
        Uses 'devicename', 'adom' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the application to push a reboot action to the FGT via the sys/proxy/json using monitor/system/os/reboot**
        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        def __reboot_device(self, **kwargs):
            inner_dict = {
                "action": "post",
                "resource": "/api/v2/monitor/system/os/reboot",
                "target": [f"adom/{self._adom}/device/{self._dev_name}"]
            }
            code = -65000
            try:
                code, res = self._fmg.execute("sys/proxy/json", data=inner_dict)
                if code == CustomResponseCode.SUCCESS:
                    status = res[0]["response"].get("status", "failed")
                    if status == "success":
                        self.ext_logger.info(f"FGT {self._dev_name} was successfully issued the reboot action")
                        return {"success": True}
                    else:
                        self.ext_logger.warning(f"FGT {self._dev_name} was issued the reboot action and the "
                                                f"action was received by the FGT, however, the FGT reported back that "
                                                f"the execution of the reboot was not successful")
                        return {"success": False}
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
                return {"success": False}
            except:
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
                return {"success": False, "exception": True}

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', k:v information
            Instructs the FMG to proxy a call to FGT to reboot. This action will not wait for a response. If the FGT needs to respond, the proper step would be to add another action using CheckDeviceIsAlive action

            :param kwargs: FGT configuration dictionary required for the perform function. 'devicename', 'adom', k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"target": kwargs["devicename"]}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            if self.__reboot_device(**kwargs)["success"]:
                return CustomResponseCode.SUCCESS, {"target": self._dev_name}
            return CustomResponseCode.NON_SUCCESS, None

    class UpgradeManagedDevice(BaseFMGAction):
        """
        Uses 'devicename', 'adom', and 'enforced.enforced_version' k:v information.

        Could use 'timers.timer', If timers are not provided, the application will default to 'delay_after_process' of 1 minute, PER firmware step required (if skip_upgrade steps, there is only one step required), delay_per_check_cycle of 10 seconds, and delay_max_check_times of 60 - which is 60 times per delay cycle (10 in this case) times EACH step in the upgrade path

        Could use 'enforced.from_fgd', 'enforced.skip_upgrade_steps'. If 'enforced.from_fgd' is not provided, default is 'N'. If 'enforced.skip_upgrade_steps' is not provided default is 'N'

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to upgrade a managed device to a specific release using the native FMG capabilities released in FMG 6.4.0 and above**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        def __upgrade_and_delay(self, **kwargs):
            # "IMAGE_UPGRADE_BOOT_ALT_PARTITION": 1,
            # "IMAGE_UPGRADE_SKIP_RETRIEVE": 2, - don't do retrieve after image upgrade
            # "IMAGE_UPGRADE_SKIP_MULTI_STEPS": 4, - skip multi steps
            # "IMAGE_UPGRADE_FORTIGUARD_IMG": 8, - download from FGD
            # "IMAGE_UPGRADE_PREVIEW": 16, -

            enforced_version = kwargs.get("enforced_firmware", {}).get("enforced_version")
            if enforced_version is None:
                self.ext_logger.error(f"FGT {self._dev_name} failed to complete its upgrade. No enforced version could "
                                      f"be found. Foregoing the delay after process as instructed, as a "
                                      f"failure will be registered and process execution will be managed by the "
                                      f"instructions provided")
                return {"success": False}
            firmware_flag = 0
            image_from_fgd = False
            skip_multi_steps = False
            device = [{"name": self._dev_name}]
            image = {"release": enforced_version}
            from_fgd = kwargs.get("enforced_firmware", {}).get("from_fgd", "y")
            if from_fgd.lower() == "y":
                image_from_fgd = True
                firmware_flag += 8
            skip_upgrade = kwargs.get("enforced_firmware", {}).get("skip_upgrade_steps", "n")
            if skip_upgrade.lower() == "y":
                skip_multi_steps = True
                firmware_flag += 4
                # since skipping steps add not to do retrieve after upgrade as well
                firmware_flag += 2
            delay_after_process = int(kwargs.get("enforced_firmware", {}).get("delay_after_process", 120))
            delay_per_check_cycle = int(kwargs.get("enforced_firmware", {}).get("delay_per_check_cycle", 10))
            delay_max_check_times = int(kwargs.get("enforced_firmware", {}).get("delay_max_check_times", 120))
            log_str = f"Firmware information is: Enforced version: {enforced_version}, Skip multi steps: " \
                      f"{skip_multi_steps}, Pull from FGD: {image_from_fgd}"
            # if not skip_multi_steps:
            #     log_str += f". Upgrade Steps are: {', '.join(path)}"
            if skip_multi_steps:
                log_str += f". Since skipping upgrade steps was configured, the FMG will be told to not perform a " \
                           f"retrieve after the image upgrade is complete"

            timeout = delay_max_check_times * delay_per_check_cycle
            # if not skip_multi_steps:
            #     timeout *= len(path)

            self.ext_logger.info(f"Attempting to upgrade the managed device FGT {self._dev_name}. The following "
                                 f"applies: Delay after process: {delay_after_process}, Delay per task check: "
                                 f"{delay_per_check_cycle}, Number of times task checked prior to timeout: "
                                 f"{delay_max_check_times}. Total timeout is: {timeout}. {log_str}")
            code, res = self._fmg.execute("/um/image/upgrade", adom=self._adom, device=device, flags=firmware_flag,
                                          create_task="enable", image=image)
            if code == CustomResponseCode.SUCCESS:
                self.handle_task_run(res, type(self).__name__, self._dev_name, sleep_time=delay_per_check_cycle,
                                     timeout=timeout)
                self.ext_logger.info(f"FGT {self._dev_name} has completed its upgrade to release {enforced_version}. "
                                     f"Sleeping for {delay_after_process} seconds as requested")
                time.sleep(delay_after_process)
                return {"success": True}
            else:
                self.ext_logger.error(f"FGT {self._dev_name} failed to complete its upgrade to release "
                                      f"{enforced_version}. Foregoing the delay after process as instructed, as a "
                                      f"failure will be registered and process execution will be managed by the "
                                      f"instructions provided")
            return {"success": False}

        def __check_if_upgrade_required(self, **kwargs):
            device = [{"name": self._dev_name}]
            # we know enforced_version exists - from calling function check
            enforced_version = kwargs.get("enforced_firmware", {}).get("enforced_version")
            image = {"release": enforced_version}
            code, res = self._fmg.execute("/um/image/upgrade", adom=self._adom, device=device, flags=16, image=image,
                                          create_task="disable")
            path = None
            upgrade_path_arr = res.get("upgrade_path", None)
            if upgrade_path_arr is not None:
                try:
                    path = upgrade_path_arr[0].get("path", None)
                except IndexError:
                    pass

            if code != 0:
                self.ext_logger.error(f"During a call to determine upgrade path for the Managed Device "
                                      f"{self._dev_name}, the FMG returned an error with a code integer "
                                      f"of {code}. This operation cannot continue and will report that there was a "
                                      f"failure on the entire UpgradeManagedDevice Action")
                return {"success": False, "path": None}
            if path is None:
                self.ext_logger.error(f"During a call to determine upgrade path for the Managed Device "
                                      f"{self._dev_name}, the FMG returned a successful call result but "
                                      f"returned an improper response in the result body. This operation cannot "
                                      f"continue and will report that there was a failure on the entire "
                                      f"UpgradeManagedDevice Action")
                return {"success": False, "path": None}
            if len(path) == 0:
                self.ext_logger.warning(f"An attempt to upgrade the Managed Device identified as "
                                        f"{self._dev_name} returned a response that it could not be upgraded. "
                                        f"This is not necessarily a negative report. The Managed Device could already "
                                        f"be on the correct version, or the version sent as required could be "
                                        f"incorrect. A successful response is being returned because this is not "
                                        f"necessarily indicative of an error.")
            else:
                self.ext_logger.info(f"During a call to determine upgrade path for the Managed Device "
                                     f"{self._dev_name}, the FMG determined that the proper upgrade path is as "
                                     f"follows: {', '.join(path)}")
            return {"success": True, "path": path}

        def __check_version_successful(self):
            code, res = self._fmg.get("/cli/global/system/status")
            major = 0
            minor = 0
            if code != 0:
                return {"success": False}
            try:
                major = int(res["Major"])
                minor = int(res["Minor"])
                if major >= 6 and minor >= 4:
                    return {"success": True}
            except (KeyError, ValueError):
                return {"success": False}
            return {"success": False}

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', and 'enforced_firmware.enforced' k:v information.

            Could require 'timers.timer', If timers are not provided, the application will default to 'delay_after_process' of 2 minutes, PER firmware step required (if skip_upgrade steps, there is only one step required), delay_per_check_cycle of 10 seconds, and delay_max_check_times of 60 - which is a ten minute upgrade PER step

            Could require 'enforced_firmware.from_fgd', 'enforced_firmware.skip_upgrade_steps'. If 'enforced_firmware.from_fgd' is not provided, default is 'N'. If 'enforced_firmware.skip_upgrade_steps' is not provided default is 'N'

            Calling perform(key word arguments from configuration):

            **Instructs the FMG to upgrade a managed device to a specific release using the native FMG capabilities released in FMG 6.4.0 and above. By default, the **

            :param kwargs: FGT configuration dictionary required for the perform function. Uses 'serialnumber' and 'adom' k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"target": kwargs["devicename"], "version": required_version}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            if not self.__check_version_successful()["success"]:
                self.ext_logger.warning(f"An attempt to upgrade the Managed Device cannot be performed, the FMG "
                                        f"version either returned an error or returned that it was not version "
                                        f"6.4.0 or higher which is a requirement for this action.")
                return CustomResponseCode.NON_SUCCESS, None

            enforced_version = kwargs.get("enforced_firmware", {}).get("enforced_version")
            if enforced_version is None:
                self.ext_logger.warning("An attempt to upgrade the Managed Device cannot be performed, a FOS version "
                                        "that is being enforced needs to be applied as an enforced_version in the "
                                        "configuration file")
                return CustomResponseCode.NON_SUCCESS, None

            # Check to ensure that what version has been asked for makes sense and that there's even an update needed
            # upgrade_required = self.__check_if_upgrade_required(**kwargs)
            # return {"success": True, "path": path}
            # if upgrade_required["success"]:
            # if len(upgrade_required["path"]) == 0:
            #     return CustomResponseCode.SUCCESS, {"target": self._dev_name, "version": enforced_version}
            # else:
            # Run an upgrade and follow the task.
            # if self.__upgrade_and_delay(upgrade_required["path"], **kwargs)["success"]:
            if self.__upgrade_and_delay(**kwargs)["success"]:
                return CustomResponseCode.SUCCESS, {"target": self._dev_name, "version": enforced_version}
            return CustomResponseCode.NON_SUCCESS, None

    class UpgradeFortiGate(BaseFMGAction):
        """
        Uses 'devicename', 'adom', 'timers.timer', 'firmware_objects.firmware_info' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to proxy an upgrade firmware call to the FGT. It then will wait and check the FGT's process based on what is set in timers in the configuration file**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        def __firmware_exists(self, path):
            if os.path.exists(path):
                return True
            else:
                self.ext_logger.error(f"Error encountered during execution processes on {self._dev_name}. "
                                      f"The location for firmware is set for {path} but does not exist. "
                                      f"Please ensure the firmware repository on the automation machine is "
                                      f"in the correct location and the firmware can be referenced. "
                                      f"Terminating...please check issue manually")
                return False

        def __fgt_on_requested_build(self, **kwargs):
            required_build = "1111"
            code, res = self._fmg.get(f"/dvmdb/adom/{self._adom}/device/{self._dev_name}", fields=["build", ])
            if code == CustomResponseCode.SUCCESS:
                reported_build = str(res.get("build", "0000"))
                required_build = str(kwargs.get("firmware_objects", {}).get("firmware_build", "1111"))
                if required_build[0] == "0":
                    required_build = required_build[1:]
                if reported_build == required_build:
                    self.ext_logger.info(f"FGT {self._dev_name} is already on build {reported_build}, no "
                                         f"upgrade required")
                    return True
            self.ext_logger.info(f"FGT {self._dev_name} is not on build {required_build}...upgrade required")
            return False

        def __fgt_responded_after_upgrade(self, **kwargs):
            # WON'T WORK ON 5.6 FGTs
            inner_dict = {
                "action": "get",
                "resource": "/api/v2/monitor/system/status/select",
                "target": [f"adom/{self._adom}/device/{self._dev_name}"]
            }
            try:
                code, res = self._fmg.execute("sys/proxy/json", data=inner_dict)
                if code == CustomResponseCode.SUCCESS:
                    status = res[0]["response"].get("status", "failed")
                    if status == "success":
                        return {"success": True}
                return {"success": False}
            except:
                return {"success": False, "exception": True}

        def __delay_for_upgrade_and_check(self, **kwargs):
            timed_out = True
            delay_after_process = int(kwargs.get("firmware_objects", {}).get("delay_after_process", 60))
            delay_per_check_cycle = int(kwargs.get("firmware_objects", {}).get("delay_per_check_cycle", 10))
            delay_max_check_times = int(kwargs.get("firmware_objects", {}).get("delay_max_check_times", 60))
            self.ext_logger.info(f"Allowing FGT {self._dev_name} to upgrade and reboot. Sleeping for "
                                 f"{delay_after_process} secs")
            time.sleep(delay_after_process)
            for time_hack in range(0, int(delay_max_check_times) + 1):
                self.ext_logger.info(f"Executing status lookup on FGT {self._dev_name}...this is cycle: {time_hack + 1}")
                fgt_responded_dict = self.__fgt_responded_after_upgrade(**kwargs)
                if not fgt_responded_dict["success"]:
                    if fgt_responded_dict.get("exception", False):
                        timed_out = False
                        break
                    else:
                        time.sleep(delay_per_check_cycle)
                else:
                    timed_out = False
                    self.ext_logger.info(f"Received response from status check on FGT {self._dev_name}. Inserting 60s "
                                         f"delay then continuing")
                    time.sleep(60.0)
                    break
            if timed_out:
                return {"success": False}
            return {"success": True}

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'devicename', 'adom', 'timers.timer', 'firmware_objects.firmware_info' k:v information
            Instructs the FMG to proxy an upgrade firmware call to the FGT. It then will wait and check the FGT's process based on what is set in timers in the configuration file

            :param kwargs: FGT configuration dictionary required for the perform function. 'serialnumber', 'devicename', and 'adom' k:v information
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"target": kwargs["devicename"], "payload": full_path_to_file}) or tuple of (CustomCode, None) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            # todo make interface have ability to upload firmware and put it in a common location
            if kwargs.get("firmware_objects", {}).get("firmware_location", None) is None:
                kwargs["firmware_objects"]["firmware_location"] = os.path.join(os.path.dirname(sys.argv[0]),
                                                                               "firmware/")
            full_path = f"{kwargs['firmware_objects']['firmware_location']}" \
                        f"{kwargs['firmware_objects']['firmware_file']}"
            if not self.__firmware_exists(full_path):
                return CustomResponseCode.NON_SUCCESS, None
            if self.__fgt_on_requested_build(**kwargs):
                return CustomResponseCode.SUCCESS, {"target": self._dev_name, "payload": full_path}
            self.ext_logger.info(f"Attempting to modify the firmware on FGT {self._dev_name}")
            with open(full_path, 'rb') as db_file:
                b64file = base64.b64encode(db_file.read())
            body = {
                "action": "post",
                "resource": "/api/v2/monitor/system/firmware/upgrade",
                "target": [f"adom/{self._adom}/device/{self._dev_name}"],
                "payload": {
                    "file_content": b64file.decode("utf-8"),
                    "source": "upload"
                }
            }
            code, res = self._fmg.execute("sys/proxy/json", data=body)
            if code == CustomResponseCode.SUCCESS:
                self.ext_logger.info(f"FGT {self._dev_name} was successfully pushed firmware and instructed to "
                                     f"execute an upgrade")
                if self.__delay_for_upgrade_and_check(**kwargs)["success"]:
                    self.ext_logger.info(f"FGT {self._dev_name} reported a successful upgrade. Continuing....")
                    return CustomResponseCode.SUCCESS, {"target": self._dev_name, "payload": full_path}
                else:
                    self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            else:
                self.ext_logger.error(BaseFMGAction.non_success_code_warning_str(self.__class__.__name__, code))
            return CustomResponseCode.NON_SUCCESS, None


    class ExecuteProxyInstruction(BaseFMGAction):
        """
        Uses 'adom' and 'devicename', 'proxy_json_scripts' k:v information

        Calling perform(key word arguments from configuration):

        **Instructs the FMG to send a proxy API call to the FGT being provisioned. Uses a list of script names held in the proxy_json_scripts k:v pairs held in the configuration file. Script format in this case must be the JSON body used for the /sys/proxy/json call.**

        """

        def __init__(self, ztplfmg):
            super().__init__(ztplfmg)

        def __script_exists(self, path):
            if os.path.exists(path):
                return True
            else:
                self.ext_logger.error(f"Error encountered during execution processes on {self._dev_name}. "
                                      f"The location for json proxy body is set for {path} but does not exist. "
                                      f"Please ensure the script repository on the automation machine is "
                                      f"in the correct location and the correct json proxy body scripts are created "
                                      f"and named appropriately. Terminating...please check issue manually")
                return False

        @BaseFMGAction.handle_standard_exceptions
        def perform(self, **kwargs):
            """
            Uses 'adom' and 'devicename', 'proxy_json_scripts' k:v information
            **Instructs the FMG to send a proxy API call to the FGT being provisioned. Uses a list of script names held in the proxy_json_scripts k:v pairs held in the configuration file. Script format in this case must be the JSON body used for the /sys/proxy/json call.**
            By default the UI tool keeps the scripts in a directory local to the process path/local_scr/

            :param kwargs: FGT configuration dictionary
            :type kwargs: dict
            :return: Return (code, dictionary) tuple in the format (code from FMG response, {"proxy_json_scripts": [successful proxy scripts that were run]}) or tuple of (CustomCode, {"proxy_json_scripts": [successful proxy scripts that were run]}) in the case that there is an exception or if the process was found to be not successful
            :rtype: tuple
            """
            self._dev_name = kwargs.get("configuration", {}).get("devicename", "device name not found")
            self._adom = kwargs.get("configuration", {}).get("adom")
            local_script_location = kwargs.get("local_script_location")
            proxy_json_scripts = kwargs.get("templates", {}).get("proxy_json_scripts", {}).get("pjs", [])
            successful_runs = []
            all_success = True
            for proxy_json_script in proxy_json_scripts:
                script_loc = os.path.join(str(local_script_location), str(proxy_json_script.get("name", "")))
                if not self.__script_exists(script_loc):
                    all_success = False
                    return CustomResponseCode.NON_SUCCESS, None
                with open(script_loc, "r", encoding="utf-8-sig") as scr_fil:
                    try:
                        proxy_body = json.load(scr_fil)
                    except json.JSONDecodeError:
                        self.ext_logger.info(f"Script {proxy_json_script.get('name', '')} was not formatted "
                                             f"correctly. Stopping all action for this run of proxied scripting as "
                                             f"this is a critical event. Please ensure "
                                             f"{proxy_json_script.get('name', '')} is valid JSON in future runs. "
                                             f"Terminating this Action unsuccessfully")
                        return CustomResponseCode.NON_SUCCESS, {"proxy_json_scripts": successful_runs}
                proxy_body["target"] = [f"adom/{self._adom}/device/{self._dev_name}"]
                code, res = self._fmg.execute("sys/proxy/json", data=proxy_body)
                if code == CustomResponseCode.SUCCESS:
                    try:
                        response_val = res[0].get("response", {}).get("http_status", 0)
                        if response_val == 200:
                            self.ext_logger.info(f"Script {proxy_json_script.get('name', '')} has been proxied "
                                                 f"successfully to the FGT and the FGT has responded with a successful "
                                                 f"response")
                            successful_runs.append(proxy_json_script.get("name", ""))
                        else:
                            self.ext_logger.info(f"Script {proxy_json_script.get('name', '')} has been proxied "
                                                 f"successfully to the FGT but the FGT has responded with code "
                                                 f"{response_val}.")
                    except IndexError:
                        self.ext_logger.info(f"Script {proxy_json_script.get('name', '')} has been proxied "
                                             f"successfully from the FMG point of view, but the response from the "
                                             f"FGT was malformed. Processing will continue, however success cannot be "
                                             f"guaranteed")
                else:
                    all_success = False
                    self.ext_logger.error(f"The script {proxy_json_script.get('name', '')} was not proxied and run "
                                          f"successfully on the FGT")
            if all_success:
                return CustomResponseCode.SUCCESS, {"proxy_json_scripts": successful_runs}
            else:
                return CustomResponseCode.NON_SUCCESS, {"proxy_json_scripts": successful_runs}
