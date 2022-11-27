import os
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_lines
import logging
import netmiko

def run_command(module: AnsibleModule, connection: netmiko.ConnectHandler):
    args = module.params
    results = {}
    command = args.get('command')
    try:
        if not connection.check_enable_mode():
            connection.enable()
        results['stdout']=connection.send_command(command).strip(connection.find_prompt())
    except Exception as err:
        logging.error("Exception: %s", err.message)
        results['changed'] = False
        raise err

    return results

def load(module: AnsibleModule):
    args = module.params
    prompts = args.get('prompt')
    device_params = {
        "device_type": args.get('device_type'),
        "ip": args.get('host'),
        "port": args.get('port'),
        "verbose": False
    }
    try:
        connection = netmiko.ConnectHandler(**device_params)
    except Exception as err:
        logging.error("Exception: %s", err.message)
        raise err

    results = run_command(module, connection)

    module.exit_json(**results)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            port=dict(required=True),
            command=dict(required=True),
            device_type=dict(required=False, default='cisco_ios_telnet'),
            prompt=dict(required=True),
        ),
        supports_check_mode=False
    )
    load(module)


if __name__ == '__main__':
    main()
