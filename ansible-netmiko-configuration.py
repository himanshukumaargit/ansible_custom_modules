from ansible.module_utils.basic import AnsibleModule
import logging
import netmiko

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
            output=connection.send_config_set(config_set,cmd_verify=True,error_pattern="% Invalid input")
            result['changed'] = True
            result['stdout']=output
            connection.save_config()
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
        ),
        supports_check_mode=True
    )
    install_config(module)

if __name__ == '__main__':
    main()    