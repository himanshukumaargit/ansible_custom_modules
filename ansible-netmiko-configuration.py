from ansible.module_utils.basic import AnsibleModule
import logging
import netmiko
import difflib

def get_config(connection:netmiko.ConnectHandler):
    connection.enable()
    return connection.send_command("show running-config")

def diff_config(cfg_old,cfg_new):
    return difflib.unified_diff(cfg_old.strip().splitlines(),
                                cfg_new.strip().splitlines(),
                                fromfile='old config',
                                tofile='new config',
                                lineterm='')

def install_config(module: AnsibleModule):
    args = module.params
    device = {
    "username":args['user'],
    "password":args['password'],
    "device_type":args['device_type'],
    "host":args['host'],
    'port':args['port']
    }
    config_set = open(args.get('config_file')).readlines()
    result={}
    try:
        with netmiko.ConnectHandler(**device) as connection:
            original_config = get_config(connection)
            output=connection.send_config_set(config_set,cmd_verify=True,error_pattern="% Invalid input")
            connection.save_config()
            result['stdout']=output            
            result['changed'] = True
            if args['diff_file']:
                new_config = get_config(connection)
                diff = diff_config(original_config, new_config)
                if diff is not None:
                    diff_file = module.params['diff_file']
                    if diff_file is not None:
                        try:
                            with open(diff_file, "w") as file_handle:
                                file_handle.write('\n'.join(diff))
                        except Exception as err:
                            result['stderr']= err
            

    except Exception as e:
        result['changed'] = False
        result['stderr']= e
            
    module.exit_json(**result)            
            

def main():
    module = AnsibleModule(
        argument_spec=dict(
                    host=dict(required=True),
                    port=dict(required=False),
                    user=dict(required=True),
                    password=dict(required=True),
                    device_type=dict(required=False, default='cisco_ios'),
                    config_file=dict(required=True),
                    diff_file=dict(required=False,default=None),              
        ),
        supports_check_mode=True
    )
    install_config(module)

if __name__ == '__main__':
    main()    