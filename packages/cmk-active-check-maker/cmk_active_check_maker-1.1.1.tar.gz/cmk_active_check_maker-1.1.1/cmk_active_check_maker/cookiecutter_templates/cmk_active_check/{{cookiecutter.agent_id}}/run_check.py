#!/usr/bin/env python3
# Template Author: NhanDD <hp.duongducnhan@gmail.com>

import os
import pathlib
from active_check.agent_nhandd_active_check import run_active_check


HOST_IP = '127.0.0.1'
SNMP_COMMUNITY = 'public'
SAMPLE_DATA = {
    'name': '{{cookiecutter.author_name}}',
    'email': '{{cookiecutter.email}}'
}
OTHER_KWARGS = {}


if __name__ == '__main__':
    print('log file will be written to', os.path.join(pathlib.Path.home(), 'fmon_active_check_logs'))
    run_active_check(SAMPLE_DATA, HOST_IP, SNMP_COMMUNITY, **OTHER_KWARGS)