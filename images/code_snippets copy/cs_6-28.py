#!/usr/bin/python
from ansible.module_utils.basic import * 
import xmlrpclib 

def main(): 
    module = AnsibleModule( 
            argument_spec = dict( 
                    url		= dict(required=True), 
                    username 		= dict(aliases=['name'], required=True), 
                    password 		= dict(required=False), 
                    display_name 	= dict(required=False) 
    
            ) 
    ) 
    params = module.params 
    
    server = xmlrpclib.ServerProxy('%s/xmlrpc.php' % params['url'], 
    use_datetime=True) 
    res = server.demo.sayHello() 

    module.exit_json(changed=True, name=res) 

if __name__ == '__main__': 
     main() 
