import logging
from . import ztpllogging
import time
from .ztplargs import Arguments
from .ztplfmg import CustomResponseCode, ZTPLFortiManager, FMGConnectionError
from .ztplconfiguration import Configurator


def set_local_loggers(log_location, *args):
    """
    Sets the local logger. For default location see the args module. To add more handlers the provision_unregistered_devices() call just needs handlers (as many as you'd like) sent in via the args reference. For instance if a syslog handler AND the default log was wanted, the call to this function would look like 'logger = set_local_loggers(args.log_location, sysloghandler_ref)'

    :param log_location: Location of the log provided by the arguments or left to default will be a local directory file called ztplite.log
    :type log_location: str
    :param args: List reference provided by the python runtime. Used in this function to add multiple handlers in this one call. If multiple handlers are needed, create them in the main() function and add them as arguments at the end of this call as shown in the instructions to this function
    :type args: list
    :return: logger ref
    :rtype: logging.logger
    """
    ztpllogging.set_loggers(logging.FileHandler(log_location, mode="a"), *args)
    logger = ztpllogging.get_logger()
    return logger


def get_config_and_instruction_info(config_file_location, ins_file_location, logger_ref):
    """
    Retrieves an in-memory hash of the configuration file and the instruction file. The application initially has a YAML file and a JSON file for the configuration file. There is a CSV converter as well, however it is not fully fleshed out as of release due to the fact that the CSV mapping will need to be hard coded. The instruction file is a JSON file.

    :param config_file_location: Location of the configuration file that will be used as set in the arguments of the application
    :type config_file_location: str
    :param ins_file_location: Location of the instruction file that will be used as set in the arguments of the application
    :type ins_file_location: str
    :param logger_ref: Reference to the logger instance
    :type logger_ref: logging.logger
    :return: Full dictionary in-memory representations of the configuration file in use (by default the YAML file) and the instruction file in use (by default the JSON file)
    :rtype: tuple
    """
    program_config = Configurator.get_translation(config_file_location, logger_ref)
    full_instructions = Configurator.get_translation(ins_file_location, logger_ref)

    if program_config is None or full_instructions is None:
        logger_ref.critical(
            f"A critical configuration requirement was not met. The application had critical issues retrieving "
            f"information from {config_file_location if program_config is None else ins_file_location}. The "
            f"application cannot continue in this state. Please correct the issue. Terminating...")
        exit(1)
    return program_config, full_instructions


def get_unregistered_devices(fmg_ref, ser_number_list, logger_ref):
    """

    :param fmg_ref: Reference to a Fortimanager instance
    :type fmg_ref: ZTPLFortiManager
    :param ser_number_list: Reference to an in-memory list of every key in the yaml file - which are all the SNs of the FGTs needing provisioning
    :type ser_number_list: list
    :param logger_ref: Reference to the logger instance
    :type logger_ref: logging.logger
    :return: Dictionary of all device serial numbers and their names if it matched a serial number setting in the configuration file referenced with program_config_hash_ref. Format is: {fgt_sn2: fgt_name2, fgt_sn2: fgt_name2}
    :rtype: dict
    """
    fgt_sn_to_promote_dict = None
    res_code, unauth_device_dict = fmg_ref.get_unauthorized_devices()
    if res_code == CustomResponseCode.SUCCESS:
        fgt_sn_to_promote_dict = {sn: name for sn, name in unauth_device_dict.items() if sn in
                                  Configurator.match_lists([*unauth_device_dict], ser_number_list)}
        if not fgt_sn_to_promote_dict:
            logger_ref.info(f"There are no FGTs that match the requirements for provisioning. Terminating....")
            exit(0)
    else:
        logger_ref.critical("The capability to retrieve Unauthorized Devices did not succeed and a "
                            "non-successful response was retrieved. This issue must be corrected prior "
                            "to the application continuing. Please correct the issue. Terminating...")
        exit(1)
    return fgt_sn_to_promote_dict


def promote_device(fmg_ref, dev_config_template, logger_ref):
    """
    Handles the promotion process of an unregistered device by calling the correct BaseFMGAction object (PromoteDevice)

    :param fmg_ref: Reference to a Fortimanager instance
    :type fmg_ref: ZTPLFortiManager
    :param dev_config_template: Reference to the Key,Value configuration information for a FORTIGATE and the DEFAULTS template that all configurations have
    :type dev_config_template: Dictionary
    :param logger_ref: Reference to the logger instance
    :type logger_ref: logging.logger
    :return: Code from the PromoteDevice BaseFMGAction object PromoteDevice
    :rtype: int
    """
    code, res = fmg_ref.PromoteDevice(fmg_ref).perform(**dev_config_template)
    if code != CustomResponseCode.SUCCESS:
        logger_ref.critical(f"FGT with SN {dev_config_template['sn']} could not be promoted. See "
                            f"errors above in the log. This is critical and this FGT will not be able to be "
                            f"provisioned further. The app will continue with further provisioning efforts if "
                            f"any are required.")
    return code


def assign_device_name(fmg_ref, dev_config_template, logger_ref):
    """
    Handles the device name assignment in the FMG - this ensures the code has the proper reference to address the Managed Device for the rest of the application's processing. The function calls the correct BaseFMGAction object (AssignDeviceName)

    :param fmg_ref: Reference to a Fortimanager instance
    :type fmg_ref: ZTPLFortiManager
    :param dev_config_template: Reference to the Key,Value configuration information for a FORTIGATE and the DEFAULTS template that all configurations have
    :type dev_config_template: Dictionary
    :param logger_ref: Reference to the logger instance
    :type logger_ref: logging.logger
    :return: Code from the PromoteDevice BaseFMGAction object PromoteDevice
    :rtype: int
    """
    code, res = fmg_ref.AssignDeviceName(fmg_ref).perform(**dev_config_template)
    if code != CustomResponseCode.SUCCESS:
        logger_ref.critical(f"FGT with SN {dev_config_template['sn']} could not be assigned a device "
                            f"name properly. See if there are any descriptive errors above in the log. "
                            f"This is critical and this FGT will not be able to be provisioned further. The app "
                            f"will continue with further provisioning efforts if any are required.")
    return code


def run_fmg_actions_on_device(fmg_ref, cmd, fgt_configuration, default_config, logger_ref):
    """
    Performs each Action that a FMG can perform on the FGT being provisioned. Each Action is called out in an Instruction provided in the instruction file

    :param fmg_ref: Reference to a Fortimanager instance
    :type fmg_ref: ZTPLFortiManager
    :param cmd: Command entry that houses all information that a FMG needs to run a discrete action
    :type cmd: Dictionary
    :param fgt_configuration: Configuration items associated with this specific FGT pulled from the configuration file
    :type fgt_configuration: Dictionary
    :param default_config: Configuration items associated with the DEFAULT configuration template in the configuration file
    :type default_config: Dictionary
    :param logger_ref: Reference to the logger instance
    :type logger_ref: logging.logger
    :return: Dictionary representing success or failure in the following format. {"success": True} | {"success": False}
    :rtype: Dictionary
    """
    time.sleep(cmd.get("DELAY_BEFORE", 0))
    fmg_action = getattr(fmg_ref, cmd["ACTION"])
    if cmd.get("DATA_REQ", []):
        # deal with those ACTIONS within an instruction that required data (such as timers or called out execution
        # scripts etc...)
        if not Configurator.fix_special_data_required_keys(fgt_configuration, cmd["DATA_REQ"][0],
                                                           cmd["ACTION"], default_config)["success"]:
            logger_ref.error(f"Data for an instruction could not be found while performing the "
                             f"provisioning on FGT with serial number {fgt_configuration['sn']}. This FGT will "
                             f"not be able to continue provisioning. The app will continue with other FGTs if "
                             f"required. The command where this failure took place was {cmd['ACTION']}")
            return {"success": False}
    continue_instruction = cmd.get("CONTINUE_ON_FAILURE", "n")
    code, res = fmg_action(fmg_ref).perform(**fgt_configuration)
    if code != CustomResponseCode.SUCCESS and continue_instruction.lower() == "n":
        logger_ref.warning(f"The response from the command {cmd['ACTION']} was not successful "
                           f"and the action controller for that action is set to not continue "
                           f"without success. Continuing with further FGTs if any are required, but "
                           f"the FGT with serial number {fgt_configuration['sn']} will have to be "
                           f"handled manually once the issue that caused this status is fixed")
        return {"success": False}
    return {"success": True}


def provision_unregistered_devices():
    """
    Used as a kickoff point for a "main" file to call to get a full provision cycle going. This entire module is so that any function can be called from "main" and the file can be whatever name the engineer wants to make it as long as it has access to the module itself everything will work. If a "main" driver needs to call another function one can be created in this module with ease and other options will be able to be built from here. Arguments could be expanded with subparsers as well to have sub-actions utilized if someone wanted to expand this.

    Function loops through each FGT in the promotion dictionary after it's been compared with the configuration file. If the Serial Number of an unregistered device matches a serial number found in the configuration file (normally a YAML file), then it is considered for provisioning.
    After the provisioning determination is made, the FGTs specific actions are pulled from the instructions file (the JSON file), which allows the engineer to tell the FMG each action that should be performed on a FGT just by utilizing the correct names of the Commands that the BaseFMGAction object gives. Using these instructions and a reference to where the data are found in the configuration file, again just in text, the code knows where to get all the data required to perform all actions on the device
    """
    ###############################################
    # Get arguments and set loggers up
    args = Arguments("ZTP Lite Base")
    logger = set_local_loggers(args.log_location)

    ###############################################
    full_config, full_instructions = get_config_and_instruction_info(args.config_file, args.instruction_file, logger)
    if full_config.get("DEFAULTS") is None:
        logger.critical(f"A critical configuration requirement was not met. The application could not find a DEFAULTS "
                        f"stanza in the configuration file located at {args.config_file}. Terminating...")
        exit(1)
    try:
        with ZTPLFortiManager(args.fmg_address, args.fmg_uname, args.fmg_pword,
                              args.debug_mode, use_ssl=args.use_ssl, disable_request_warnings=True) as fmg:

            # DEBUG - COMMENT THE BELOW
            fmg.set_debug_logger(args.debug_log_location)

            # return will be {"sn": "name", "sn2", "name2", ...} if there are serial numbers to be promoted
            # DEBUG - COMMENT THE BELOW
            fgt_sn_to_promote_dict = get_unregistered_devices(fmg, [*full_config], logger)
            # DEBUG - UNCOMMENT THE BELOW FOR FAKE FGT REFERENCE
            # fgt_sn_to_promote_dict = {"12345": "hostnamehere"}
            ###############################################
            # Run through each FGT's provision instructions
            for fgt_sn in fgt_sn_to_promote_dict:
                fgt_config = full_config[fgt_sn]
                # inject the local_script_location
                fgt_config["local_script_location"] = args.local_scr_location
                fgt_config["discovered_hostname"] = fgt_sn_to_promote_dict[fgt_sn]
                # extract fgt configuration information and json from instruction file based on the SN and the
                # templates.instructions attribute in the configuration file
                logger.info(f"Beginning instructions search for the FGT with SN {fgt_sn}")
                Configurator.config_key_val_mapper(fgt_config, full_config["DEFAULTS"])
                try:
                    fgt_instruction_list = full_instructions["INSTRUCTIONS"][fgt_config["templates"]["instructions"]]
                except KeyError:
                    fgt_instruction_list = []
                if not fgt_instruction_list:
                    logger.warning(f"The FGT with SN {fgt_sn} was to be promoted but no instruction list of actions "
                                   f"could be found to match what was called for in the configuration for this FGT. "
                                   f"This FGT will be bypassed for promotion and ZTP. Ensure the configuration is set "
                                   f"correctly for this FGT's instructions")
                    continue
                # inject the new password if it's coming from args and not in the FGT config or if FGT config
                # has it as a blank string
                fgt_config_password = fgt_config["configuration"].get("device_pw", None)
                if fgt_config_password == "":
                    fgt_config_password = None
                if args.new_pass is not None and fgt_config_password is None:
                    fgt_config["configuration"]["device_pw"] = args.new_pass

                # promotion and setting the devicename is a requirement, no use to use inspection for these.
                # DEBUG - COMMENT THE BELOW 4 lines
                if promote_device(fmg, fgt_config, logger) != CustomResponseCode.SUCCESS:
                    continue
                if assign_device_name(fmg, fgt_config, logger) != CustomResponseCode.SUCCESS:
                    continue

                ###############################################
                # Run through each Action for a FGT's provisioning instructions
                for cmd in fgt_instruction_list:
                    if not run_fmg_actions_on_device(fmg, cmd, fgt_config, full_config["DEFAULTS"], logger)["success"]:
                        break
                else:
                    time.sleep(cmd.get("DELAY_AFTER", 0))
                    logger.info(f"All actions completed on FGT with serial number {fgt_sn}. Continuing...")
            else:
                logger.info(f"Application process for all FGTs is complete")
    except AttributeError as ae:
        logger.error(f"Handled an attribute error - more than likely an instruction was called in the instruction "
                     f"file that has not been created in the ztplfmg class or there was a misspelling or "
                     f"misconfiguration with one of the instructions entered in the instruction file. The "
                     f"error information is: {str(ae)}")
    except FMGConnectionError as fce:
        logger.error(f"Handled a connection error - more than likely FMG IP address or FQDN is incorrect or the FMG "
                     f"is not currently active on the network. The error information is: {str(fce)}")
