#!/usr/bin/env python3
# Template Author: NhanDD <hp.duongducnhan@gmail.com>

"""
Simple Packer and (later) unpacker for MKP Files
MKP is the Package format for Check_MK
"""
import os
from cmk_tools import pack_mkp


base_path = os.getcwd()
package_name = "{{cookiecutter.agent_id}}"
checks_file = 'agent_{{cookiecutter.agent_id}}.py'
lib_file = 'agent_{{cookiecutter.agent_id}}.py'
wato_file = '{{cookiecutter.agent_id}}_register.py'
checks_file_path = os.path.join(base_path, 'check_invoker', checks_file)
lib_file_path = os.path.join(base_path, 'active_check', lib_file)
wato_file_path = os.path.join(base_path, 'wato', wato_file)


if __name__ == "__main__":
    pack_mkp(
        package_name=package_name,
        checks_file=checks_file,
        lib_file=lib_file,
        wato_file=wato_file,
        checks_file_path=checks_file_path,
        lib_file_path=lib_file_path,
        wato_file_path=wato_file_path,
        base_path=base_path
    )