import os
from ansible.module_utils.basic import AnsibleModule
import logging
import netmiko

def install_config(module: AnsibleModule, connection: netmiko.ConnectHandler):
    args = module.params
    results = {}
    config_file = os.path.abspath(args['config_file'])
    results['file'] = config_file
    results['changed'] = False
    logging.info("loading %s", config_file)
    config_set = open(config_file).readlines()
    try:
        if not connection.check_enable_mode():
            connection.enable()
        connection.send_config_set(config_set)
        results['changed'] = True
    except Exception as err:
        logging.error("Exception: %s", err.message)
        raise err
    connection.save_config()
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

    results = install_config(module, connection)

    module.exit_json(**results)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            port=dict(required=True),
            config_file=dict(required=True),
            device_type=dict(required=False, default='cisco_ios_telnet'),
            prompt=dict(required=True),
        ),
        supports_check_mode=False
    )
    load(module)


if __name__ == '__main__':
    main()
# set ANSIBLE_LIBRARY env variable to current file path
