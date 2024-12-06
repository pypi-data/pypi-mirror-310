#!/usr/bin/env python3
# Template Author: NhanDD <hp.duongducnhan@gmail.com>

# enable if you want to use libs
# require install extra libs: snmp, requests
# import netsnmp
# import re
# import ast
import json
import os
import sys
from cmk_tools import (
    setup_log, 
    make_request, 
    terminate_check,
    is_test_device,
)
# from datetime import datetime, timezone
from pathlib import Path
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# -----------------------------------------   
#   DO NOT MODIFY BELLOW CONSTANTS
#   you could add more constants if you need
# -----------------------------------------   

#
DEBUG = "DEBUG"
OK = "OK"
WARN = "WARN"
WARNING = "WARNING"
CRITICAL = "CRITICAL"
ERROR = "ERROR"
UNKNOWN = "UNKNOWN"


# -----------------------------------------   
# create logger, DO NOT MODIFY logger and log function
logger = setup_log("{{cookiecutter.agent_id}}-logger")
def log(msg, **kwargs):  
    logger.info(msg, extra={'service_name': '{{cookiecutter.agent_id}}',})
    

def run():
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    try:
        args = sys.argv[1:]
        while args:
            section = args.pop(0)
            if section == '--data':
                formatted_json = args.pop(0).replace("'", '"')
                data = json.loads(formatted_json)
            if section == '--ip':
                ip = str(args.pop(0))
            if section == '--hostname':
                hostname = str(args.pop(0))
                if hostname:
                    is_test_device(hostname)
            if section == '--community':
                community = str(args.pop(0))
    except Exception as e:
        terminate_check(UNKNOWN, f"Error when parse arguments with error: {e}")
    
    if not data:
        terminate_check(UNKNOWN, "Missing data argument")
    if not ip:
        terminate_check(UNKNOWN, "Missing ip argument")
    
    # run agent 
    try:
        run_active_check(data, ip, community, hostname=hostname)
    except Exception as e:
        terminate_check(UNKNOWN, f"Error when run active check with error: {e}")
    

# ----------------------------------------- 
#   Your code begin here, entry point is run_active_check function
#   You could define other function to support run_active_check function
#   DO NOT MODIFY ABOVE, If you need other id, create new plugin template!
# -----------------------------------------        
def run_active_check(data, host_ip, snmp_community, **kwargs):
    log(f"run check with data {data} for host {host_ip} with community {snmp_community} and kwargs {kwargs}")
    # your code here
    # .....
    # .....
    # here is my example, remove it and replace with your code 
    return example_get_os_info()
    
def example_get_os_info():
    # example cod
    import platform
    # Gather OS details
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    architecture = platform.architecture()
    node = platform.node()
    machine = platform.machine()
    processor = platform.processor()

    # show message then exit
    terminate_check(
        OK,    
        f"Operating System: {os_name}, Version: {os_version}, Release: {os_release}, Architecture: {architecture[0]}, Hostname: {node}, Machine: {machine}, Processor: {processor}"
    )


if __name__ == '__main__':
    # ----------------------------------------- 
    #   DO NOT MODIFY
    # -----------------------------------------    
    run()
    # -----------------------------------------
