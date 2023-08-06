import argparse
import os
import sys


class Arguments(object):

    def __init__(self, desc):
        """

        :param desc: Description string for argument display
        :type desc: str
        """
        self._parser = argparse.ArgumentParser(description=desc)
        config_group = self._parser.add_argument_group("configuration")
        config_group.add_argument("-i", "--instruction_file",
                                  help="Instruction file providing text to code structure. Defaults to "
                                       "ztpltexttocode.json in the current directory.", default=None)
        config_group.add_argument("-c", "--config_file",
                                  help="Config file location. No default provided and is a requirement.",
                                  default=None)
        config_group.add_argument("-l", "--local_script_loc",
                                  help="Local script location directory. No default provided", default=None)
        auth_group = self._parser.add_argument_group("authentication")
        self._parser.add_argument("-s", "--fmg_address", default="10.0.0.1", help="FMG address")
        auth_group.add_argument("-u", "--fmg_uname", default="admin", help="FMG username")
        auth_group.add_argument("-p", "--fmg_pword", default="", help="FMG password")
        loc_log_group = self._parser.add_argument_group("local logging")
        loc_log_group.add_argument("-o", "--log_location", default=None,
                                   help="standard log location. Defaults to a log in the local directory named "
                                        "ztplite.log")
        loc_log_group.add_argument("-d", "--debug_log_location", help="Debug Log location, default is the current "
                                                                      "directory with a filename of debug.log")
        remote_log_group = self._parser.add_argument_group("remote logging")
        remote_log_group.add_argument("--use_syslog", action="store_true", default=False,
                                      help="Sets requirement for syslog logging. Default is false")
        remote_log_group.add_argument("--syslog_addr", default="/dev/log",
                                      help="IP address of listening syslog server. Defaults to /dev/log for local "
                                           "host logging.")
        remote_log_group.add_argument("--syslog_port", default=514, help="Port used for syslog server. Default is 514")
        remote_log_group.add_argument("--syslog_fac", default="user",
                                      help="Facility for syslog server logging. Default is user")
        self._parser.add_argument("--new_pass", default=None,
                                  help="New Password for all FortiGates during this process")
        self._parser.add_argument("-v", action="append",
                                  help="Runs code in verbose mode. Append multiple vs for verbosity")
        self._parser.add_argument("-D", "--debug", action="store_true", default=False,
                                  help="Run in debug mode. Enables debug logging and console debugging.")
        self._parser.add_argument("--ssl", action="store_true", default=False,
                                  help="Connect to FMG using SSL. Default is false")
        self.args = self._parser.parse_args()

    def __setitem__(self, key, value):
        vars(self.args)[key] = value

    @property
    def text_to_code_file(self):
        """

        :return: File path to a text to code file for use, by default this is ztplinstructions.json in the same directory as the calling module
        """
        if self.args.instruction_file is not None:
            return self.args.instruction_file
        else:
            return os.path.join(os.path.dirname(sys.argv[0]), "ztplinstructions.json")

    @property
    def instruction_file(self):
        """

        :return: File path to a text to code file for use, by default this is ztplinstructions.json in the same directory as the calling module
        """
        if self.args.instruction_file is not None:
            return self.args.instruction_file
        else:
            return os.path.join(os.path.dirname(sys.argv[0]), "ztplinstructions.json")

    @property
    def config_file(self):
        """

        :return: File path to a configuration file for use.
        """
        if self.args.config_file is not None:
            return self.args.config_file
        else:
            return None

    @property
    def fmg_address(self):
        """

        :return: FMG address or FQDN
        """
        return self.args.fmg_address

    @property
    def fmg_uname(self):
        """

        :return: Username for login purposes to FMG.
        """
        return self.args.fmg_uname

    @property
    def fmg_pword(self):
        """

        :return: Password for login purposes to FMG.
        """
        return self.args.fmg_pword

    @property
    def log_location(self):
        """

        :return: Log file location. Default is a file named ztplite.log in the same directory as the calling module
        """
        if self.args.log_location is not None:
            return self.args.log_location
        else:
            return os.path.join(os.path.dirname(sys.argv[0]), "ztplite.log")

    @property
    def local_scr_location(self):
        """

        :return: Local script directory location. Default is None
        """
        return self.args.local_script_loc

    @property
    def debug_log_location(self):
        """

        :return: Debug log location.
        """
        if self.args.debug_log_location is not None:
            return self.args.debug_log_location
        else:
            return os.path.join(os.path.dirname(sys.argv[0]), "debug.log")

    @property
    def uses_syslog(self):
        """

        :return: Boolean value to determine whether a syslog logger will be utilized.
        """
        return self.args.use_syslog

    @property
    def syslog_addr(self):
        """

        :return: Syslog address if syslog logging is enabled.
        """
        return self.args.syslog_addr if self.uses_syslog else None

    @property
    def syslog_port(self):
        """

        :return: Syslog port if syslog logging is enabled.
        """
        return self.args.syslog_port if self.uses_syslog else None

    @property
    def syslog_fac(self):
        """

        :return: Syslog facility if syslog logging is enabled.
        """
        return self.args.syslog_fac if self.uses_syslog else None

    @property
    def new_pass(self):
        """

        :return: Password that will be placed on all FGTs in a provisioning run.
        """
        return self.args.new_pass

    @property
    def verbosity(self):
        """

        :return: List representing level of verbosity.
        """
        return self.args.v

    @property
    def debug_mode(self):
        """

        :return: Boolean value to determine whether the program is in debug mode.
        """
        return self.args.debug

    @property
    def use_ssl(self):
        """

        :return: Boolean value to determine whether connection to FMG uses SSL.
        """
        return self.args.ssl
