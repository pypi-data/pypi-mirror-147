## Synopsis

Provides Zero Touch Provisioning functions for Fortinet assets using FortiManager.

Initial Setup
#############

ZTPLite requires a system that is running python3

To install ztplite is simple. All that is required is to run:

.. code-block:: python

    pip install ztplite


A good practice is always to perform python package installs from a virtual environment so as not to interfere with the system requirements. See the python docs or other documents about virtual environments (venv or virtualenv) such as `Virtual Environment Docs <https://docs.python.org/3/tutorial/venv.html>`_

Program Usage
*************

To get ZTPLite working, a python module acting as a driver must be called. This driver is minimal and must call the :ref:`Controller's<Controller Module>` *provision_unregistered_devices* function. Once that call is made, the rest of the program runs automatically.

To define the driver (we will call it *ztpl_main.py*), things could not be simpler. As stated before it simply needs to call a function within the :ref:`Controller<Controller Module>` that looks to provision unregistered devices called (drumroll please) *provision_unregistered_devices*. A full driver module is provided here:

.. code-block:: python

    #!/usr/bin/env python3
    from ztplite import ztplcontroller

    def main():

        ztplcontroller.provision_unregistered_devices()

    if __name__ == "__main__":
        main()


In the case that follows the calling module (remember that we named it *ztpl_main.py*) is executed. Shown below is the call and an explanation of the arguments string that would be used for an example run....so:

.. code-block:: python

    python ztpl_main.py -s 10.1.1.1 -o /home/fortinet/ztpdemo/ztplite.log -c /home/fortinet/ztpdemo/configyml.yml -i /home/fortinet/ztpdemo/instructions.json --ssl -D


- This would call a driver python module named *ztpl_main.py* with the target FMG at 10.1.1.1

- The information log would be at /home/fortinet/ztpdemo/ztplite.log

- The configuration file is the yaml file at /home/fortinet/ztpdemo/configyml.yml

- The instruction file is a json file at /home/fortinet/ztpdemo/instructions.json

- The conversation with the FMG will utilize ssl

- The code will be running in Debug mode as well so the default debug log will be in affect. If the call needed to place the debug log specifically, the -d flag should have been used as discussed below in the :ref:`Additional Argument Information` section

Clearly the above call would be hosted in a cron job somewhere or within a task that called it from within a virtual environment every hour or day or whatever timeframe the customer found acceptable. Any other task management process (other than cron) could be used to call the program of course.

Additional Argument Information
*******************************

ztpl_main.py    [-h] [-i INSTRUCTION_FILE] [-c CONFIG_FILE]
                [-s FMG_ADDRESS] [-u FMG_UNAME] [-p FMG_PWORD]
                [-o LOG_LOCATION] [-d DEBUG_LOG_LOCATION]
                [--use_syslog] [--syslog_addr SYSLOG_ADDR] [--syslog_port SYSLOG_PORT] [--syslog_fac SYSLOG_FAC]
                [--new_pass NEW_PASS] [-v V] [-D] [--run_test] [--ssl]

- Configuration:

  -i, --instruction_file INSTRUCTION_FILE_PATH: Instruction file path providing text to code structure. Defaults to ztpltexttocode.json in the directory where the main driver module is called

  -c, --config_file CONFIG_FILE: Config file path providing a location where the configuration file is located. No default is provided and this is a requirement

  -s, --fmg_address FMG_ADDR_STRING: FMG address or FQDN to FMG performing the ZTP operations

- Authentication:

  -u, --fmg_uname FMG_UNAME: FMG username used for authentication. Default is *admin*

  -p, --fmg_pword FMG_PWORD: FMG password used for authentication. Default is a blank password

- Local Logging:

  -o, --log_location LOG_LOCATION: Standard log location. Defaults to a log in the local directory named *ztplite.log*

  -d, --debug_log_location DEBUG_LOG_LOCATION: Debug Log location, default is the current directory with a filename of *debug.log*

- Remote Logging:

  --use_syslog: Sets requirement for syslog logging. Default is *false*

  --syslog_addr SYSLOG_ADDR: IP address of listening syslog server. Defaults to */dev/log* for local host logging.

  --syslog_port SYSLOG_PORT: Port used for syslog server. Default is *514*

  --syslog_fac SYSLOG_FAC: Facility for syslog server logging. Default is *user*

- Optional Arguments:

  -h, --help: Display this help message and exit

  --new_pass NEW_PASSWORD: New Password for all FortiGates during this process

  -v: Runs code in verbose mode. Append multiple letter v for verbosity (i.e. -vvvv)

  -D, --debug: Run in debug mode. Enables debug logging and console debugging

  --ssl: Connect to FMG using SSL. Default is *false*

  --run_test: Run a test to determine if the instruction file has correct requirements in the DATA-REQ list. No actual modifications will take place if run_test is set
