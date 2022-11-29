import os
from ansible.module_utils.basic import AnsibleModule
import logging
import netmiko
import time
import pdb


def execute_command(module: AnsibleModule):
    args = module.params
    jumphost_ = {
        'device_type':args['jumphost_type'],
        'username':args['jumphost_user'],
        'password':args['jumphost_password'],
        'host':args['jumphost_ip'],
        'port':args['jumphost_port']
    }
    device_ = {
    "username":args['device_user'],
    "password":args['device_password'],
    "device_type":args['device_type'],
    "host":args['device_ip'],
    'port':args['device_port']
    }
    kex_algorithms=args['KexAlgorithms']
    strict_host_key_checking=args['StrictHostKeyChecking']
    host_key_algorithms=args['HostKeyAlgorithms']
    commands=list(args['device_commands'])
    result={}
    output = ""
    with netmiko.ConnectHandler(**jumphost_) as ssh_connection:
        try:
            ssh_connection.write_channel("ssh -oKexAlgorithms={2} -oStrictHostKeyChecking={3} -oHostKeyAlgorithms={4} {0}@{1} \n".format(device_['username'],
                                                                                                                                         device_['host'],
                                                                                                                                         kex_algorithms,
                                                                                                                                         strict_host_key_checking,
                                                                                                                                         host_key_algorithms))
            time.sleep(2)
            ssh_connection.write_channel(device_['password']+"\n")
            time.sleep(2)
            netmiko.redispatch(ssh_connection,device_type=device_['device_type'])
            for command in commands:
                output+="+++++++++++++++++++++++++++++++++++++++++++ command: "+command+" +++++++++++++++++++++++++++++++++++++++++++\n"
                output+=ssh_connection.send_command(command)
            result['stdout']=output    
            result['ok']=True
        except Exception as e:
            result['failed']=True
            result['stdout']=e
    module.exit_json(**result)

def main():
    module = AnsibleModule(
        argument_spec=dict(
                    jumphost_ip=dict(required=True),
                    jumphost_port=dict(required=False),
                    jumphost_user=dict(required=True),
                    jumphost_password=dict(required=True),
                    jumphost_type=dict(required=False, default='linux_ssh'),
                    device_ip=dict(required=True),
                    device_port=dict(required=False),
                    device_user=dict(required=True),
                    device_password=dict(required=True),
                    device_type=dict(required=False, default='cisco_ios'),
                    device_commands=dict(type='list',elements='raw'),
                    KexAlgorithms=dict(required=False,default="diffie-hellman-group-exchange-sha1"),
                    StrictHostKeyChecking=dict(required=False,default="no"),
                    HostKeyAlgorithms=dict(required=False,default="ssh-rsa"),                  
        ),
        supports_check_mode=True
    )
    execute_command(module)


if __name__ == '__main__':
    # pdb.set_trace()
    main()
