# Writing Modules in Ansible

### Writing Your Own Ansible Modules

>Preparation: For this demo, you'll need to ensure `book.example.com` is up and running. We've gone ahead and provided the necessey files for you, if it isn't. Simply, issue the following commands:<br>

```console
$ vagrant status
$ vagrant up
```

Now, visit `http://book.example.com` to ensure it is up.

#### Environment Setup
Before you start writing your module, you need to perform a little bit of environment setup to allow you to test the module as you write it. This work is going to be totally separate from the work we’ve done in previous chapters, so let’s create a new folder to work in:

```console
$ cd ~/Desktop/ansible/ansible-students/ansible-modules
$ git clone git://github.com/ansible/ansible.git --recursive
$ source ansible/hacking/env-setup
$ chmod +x ansible/hacking/test-module
```

You may also need to install Ansible’s pyyaml and jinja2 dependencies. You can do this via pip, the Python package manager:

```console
$ pip install pyyaml jinja2
```

#### Writing Modules With Bash

If your module is simple, you might choose to write it in Bash. Most of the time, I wouldn’t recommend this, however it’s a good tool for writing a simple module. 

Let’s create a module that takes a file and converts it to uppercase.

1\. Create a file named `file_upper`, and then make it executable:

```console
$ touch file_upper
$ chmod +x file_upper
```

2\. Now, let’s create a module that just returns some data in order for you to get used to developing and running a module. Let’s write a module that returns a JSON-encoded string under the “content” key. Add the following to `file_upper`:

```bash
#!/bin/bash
cat <<EOF
{"content":"Hello World"}
EOF
```

3\. Now, save it and run `ansible/hacking/test-module -m file_upper` so as to run your module as Ansible would do. For now, this will output your return data to the screen:

```console
$ ansible/hacking/test-module -m file_upper
```

Output:

```json
* including generated source, if any, saving to: /Users/michael/.ansible_ module_generated
* this may offset any line numbers in tracebacks/debuggers! ***********************************
RAW OUTPUT
{"content":"Hello World"}
***********************************
PARSED OUTPUT
{
    "content": "Hello World"
}
```
** !! MUST CHANGE OUTPUT PATHS - DO not MISS THIS !!**

Great! You just wrote your first Ansible module and tested it with the built-in Ansible test-module script.

4\. Like we learned in the lecture, you can update your module to show the file that is provided by substituting `Hello World` with `$1` and running your module again. Your module should now look like the following:

```bash
#!/bin/bash
cat <<EOF
{"content":"$1"}
EOF
```

5\. Once you’ve made this change, you can run the `test-module` script again and inspect the module’s output. This time, when you run the `test-module` script, provide some arguments using the `–a` flag, like this:

```console
$ ansible/hacking/test-module -m file_upper -a foo=bar
```

Output:

```json
***********************************
PARSED OUTPUT
{
    "content": "<path-to-file>/.ansible_test_module_arguments"
}
```
>Note: This output will be specific to you and your machine. Copy it and prepare to paste it next.

Your module now outputs a path to a file, which is what you were expecting to see. This file contains the arguments passed to Ansible. 

6\. Examine this file to see which parameters were passed in:

```console
$ cat <path-to-file>/.ansible_test_module_arguments 
```
Output:

```console
foo=bar
```
As you can see, the parameters that you specified when calling `test-module` have been stored in this file. 

7\. In your module, you can use `source` to include this file, as the `key=value` format is what Bash uses to define variables. If you include your arguments file using `source`, the variable `$foo` will be available with the value `bar`. Your module should be updated to look like the following:

```bash
#!/bin/bash
source $1
cat <<EOF
{"content":"$foo"}
EOF
```

8\. Now, run your module again, and see your `foo` parameter being used in your module: 

```console
$ ansible/hacking/test-module -m file_upper -a foo=bar
```

Output:

```json
***********************************
PARSED OUTPUT
{
    "content": "bar"
}
```

>Note: Although this works, sourcing user-provided input is very **dangerous**. This is meant for learning purposes, it is not something that you should ever do.

The last thing left to do is to implement your actual module logic. The code in your module so far is just boilerplate to read variables in and output a result from your module.

9\. You need to make the module accept a filename as a parameter, then make all characters in that file uppercase. Once you’ve translated the characters, you can write the new content to the filename provided and return JSON for Ansible to work with. 

To do all of this, your script needs to look like the following:

```bash
#!/bin/bash 
source $1
content=$(cat $file | tr '[:lower:]' '[:upper:]')
echo $content > $file
cat <<EOF
{"content":"$content"}
EOF
```

>Note: Notice we're using the `tr` command to translate.

10\. The next time that you run the module, the file that is specified will be converted to uppercase. (Make sure that the file exists first!)

```console
$ ansible/hacking/test-module -m file_upper -a file=example_file.txt
```

11\. Ansible modules should be idempotent. Modules report back whether any changes were made using the changed attribute in the returned JSON. You can support this in your module by checking to see if the content is the same both before and after you perform your transform:

```bash
#!/bin/bash

source $1

original=$(cat $file)
content=$(echo $original | tr '[:lower:]' '[:upper:]')

if [[ "$original" == "$content" ]]; then
    CHANGED="false"
else
    CHANGED="true"
    echo $content > $file
fi

cat <<EOF
{"changed":$CHANGED, "content":"$content"}
EOF
```

12\. This file now contains all of the information that Ansible requires in order to run as a standalone module. Give it a go with by running `example_file.txt`, or one of your own.

>Note: The first time that you run it, you’ll notice that changed is true. If you run the module again on the same file, your module will report that changed is false. Your module is now idempotent.

#### Writing Modules With Python

Like we already learned in our lecture, Ansible doesn’t care which language you use to create a module. Honestly, writing a module in Python can be very similar to writing a module in Bash. Ready? Let's go!

1\. Ansible ships with a library called `ansible.module_utils.basic` that provides all of the boilerplate that you’d otherwise have to write yourself in every module. 

Create a file called `wp_user` with the following contents:

```python
#!/usr/bin/python

from ansible.module_utils.basic import *

def main():
  module = AnsibleModule(
      argument_spec = dict(
          name  = dict(required=True)
      ) 
  )
  
  params = module.params
  
  module.exit_json(changed=True, name=params['name'])

if __name__ == '__main__':
    main()
```

This code provides you with a basic Ansible module that takes a single argument, name.

2\. Try to run the module without any arguments:

```console
$ ansible/hacking/test-module -m wp_user
```

Output:

```json
***********************************
PARSED OUTPUT
{
    "failed": true,
    "invocation": {
        "module_args": {}
    },
    "msg": "missing required arguments: name"
}
```

>Note: Notice the error message: "msg": "missing required arguments: name".

3\. Now, call the module with a `name` argument, you can see that both `changed` and `name` are returned, as well as information about how the module was invoked:

```console
$ ansible/hacking/test-module -m wp_user -a name="foo"
```

Output:

```json
***********************************
PARSED OUTPUT
{
    "changed": true,
    "invocation": {
        "module_args": {
            "name": "foo"
} },
    "name": "foo"
}
```

4\. At this point, you can start thinking about what parameters your `user-management` module for WordPress will need. You'll need to specify the URL of the WordPress installation, and your user’s username, password, and display name. 

Update your module definition to require these parameters:

```python
  module = AnsibleModule(
      argument_spec = dict(
          url          = dict(required=True),
          username     = dict(aliases=['name'], required=True),
          password     = dict(required=True),
          display_name = dict(required=False)
      )
)
```

5\. Make sure that all of that is working by running your module now, providing both the `name` and `password`, but without providing the `url` argument:

```console
$ ansible/hacking/test-module -m wp_user -a 'name="your-name" password="your-password"'
```

Output:

```json
PARSED OUTPUT
{
    "failed": true,
    "invocation": {
        "module_args": {
            "name": "foo",
            "username": "foo",
            "password": "pass"
        } 
    },
    "msg": "missing required arguments: url"
}
```

>Note: The error message returned from the `test-module` script tells you that you’re missing `url`, but not `display_name`, as only `url` is required. 

6\. If you run your module with all of the required fields, you should see the same output that contains invocation information and a name as you saw before:

```console
$ ansible/hacking/test-module -m wp_user -a 'name="your-name" password="your-password" url="http://book.example.com" display_name="your-name"'
```

Output:

```json
***********************************
PARSED OUTPUT
{
    "changed": true,
    "invocation": {
        "module_args": {
            "display_name": "your-name",
            "name": "your-name",
            "password": “your-password”,
            "url": "http://book.example.com",
            "username": "your-name"
        } 
    },
    "name": "your-name"
}
```

At this point, your module definition is done, and you can start implementing your module. WordPress automatically enables it’s XML-RPC API, so you can start working with it right away.

#### Working XWL-RPC API With XMLRPCLIB

To make a call to the RPC endpoint, you need to send a correctly formatted request to `http://book.example.com/xmlrpc.php`. To do this, you can use Python’s built-in `xmlrpclib` module. 

1\. When ready, import `xmlrpclib` at the top of your module's file, and you can then start using it. 

<pre>
#!/usr/bin/python
from ansible.module_utils.basic import * 
<b>import xmlrpclib</b>
...                                  # More code than shown
</pre>

2\. At the top of your module is the module definition, unchanged. Below that though, you can see that you you will be connecting to your RPC server and making a request to an example endpoint to make sure that everything is working as intended. We've boldfaced the lines in the following code you will add:

<pre>
#!/usr/bin/python
from ansible.module_utils.basic import * 
import xmlrpclib

def main():
  module = AnsibleModule(
      argument_spec = dict(
          url           = dict
          username
          password
          display_name  = dict(required=False)
      ) 
  )
  
  <b>
  params = module.params
  
  server = xmlrpclib.ServerProxy('%s/xmlrpc.php' % params['url'], use_datetime=True)
  res = server.demo.sayHello()
  
  module.exit_json(changed=True, name=res)
  </b>

if __name__ == '__main__':
    main()
</pre>

You’ve made a request to the `demo.sayHello` endpoint in WordPress’s RPC API.
All this endpoint does is to return the string “Hello!”, which means that you can use it to test your connectivity.

3\. Well, go ahead and run it, and confirm your output matches the following:
If you run your module with the preceding code, you can see that things are working as intended:

```json
***********************************
PARSED OUTPUT
{
    "changed": true,
    "invocation": {
        "module_args": {
            ...
} },
    "name": "Hello!"
}
```

4\. Like we learned, you can set a user’s `first_name`, `last_name`, `url`, `display_name`, `nickname`, `nicename`, and `bio` via the endpoint. 

Now, update your module definition to support all of these parameters:


```python
module = AnsibleModule(
    argument_spec = dict(
        url          = dict(required=True),
        username     = dict(aliases=['name'], required=True),
        password     = dict(required=False),
        first_name   = dict(required=False),
        last_name    = dict(required=False),
        user_url     = dict(required=False),
        display_name = dict(required=False),
        nickname     = dict(required=False),
        nicename     = dict(required=False),
        bio          = dict(required=False)
    ) 
)
```

5\. Next, you iterate over all of the parameters provided, skipping `username`, `password`, and `url`. You must also rename the `user_url` key to `url`, as that is what WordPress will be expecting. Finally, you make the request by replacing `res = server.demo.sayHello()` with the following:

```python
details = {}
  skip_fields = ['username','name','password','url']
  mappings = {"user_url": "url"}
  for k, v in params.iteritems():
    if k in skip_fields:
      continue
    if v:
      if k in mappings:
        k = mappings[k]
      details[k] = v
  res = server.wp.editProfile(1, params['username'], params['password'], details)
```

>Note: The scope of this course only requires that you understand basically what this code is doing, not how to write it yourself.


6\. You can see that the profile has been updated if you run this code using the following command, and then log in to your WordPress install’s admin area, located at `http://book.example.com/wpadmin/profile.php`:

```console
$ ansible/hacking/test-module -m wp_user -a 'name="your-name" url="http://book.example.com" password="your-password" first_name="<your-name>" last_name="<your-name>" user_url="http://<your-url>.com"'
```

#### Making It Idempotent

To make your module idempotent, you need to fetch the user’s details and determine whether the values that you’re providing are different from the values currently on record.

1\. Add the code to search the existing users between the line that starts `server = xmlrpclib` and the one that contains `details = {}`:

```python
server = xmlrpclib.ServerProxy('%s/xmlrpc.php' % params['url'], use_datetime=True)
existing_users = server.wp.getUsers(1, params['username'], params['password'])
  current_user = None
  for u in existing_users:
    if u['username'] == params['username']:
      current_user = u
      break
```

2\. You do know that the user will exist, as you’re logging in as the user, so you can just search until you find a username that matches the one that you’re using to log in. You save this user as current_user for use later. Then, just before you make a call to `wp.editProfile`, you iterate over all of the keys in detail and compare them with the current values. If any values don’t match, you update the user details to the new values and mark the user as changed. If the user has changed, you can make a request to WordPress; otherwise, you don’t need to make the request:

```python
is_changed=False
for k,v in details.iteritems():
  if current_user[k] != details[k]:
    current_user[k] = details[k]
    is_changed = True
  if is_changed:
    server.wp.editProfile(1, params['username'], params['password'], details)
```

3\. The next step is to return `is_changed` in your call to `module.exit_json` so that any handlers will be triggered correctly. You should also return the user so that the details are available if anyone wants to register a variable and use them later:

```python
module.exit_json(changed=is_changed, user=dict(current_user))
```

4\. At this point, you have only one last thing to implement: check mode. You have to tell Ansible explicitly that your module supports check mode by adding `supports_check_mode=True` to your module definition:

```python
module = AnsibleModule(
    argument_spec = dict(...),
    supports_check_mode=True
)
```

5\. Once you’ve done this, you need to make sure that the call that makes the change isn’t actually executed. You already check to see if anything has changed before making the request, so you can reuse that same if statement for check mode as well:

```python
if is_changed and not module.check_mode:
    server.wp.editProfile(1, params['username'], params['password'], details)
```

6\. As Ansible provides an additional parameter of `_ansible_check_mode`, which we’re not interested in when updating a user, add this to `skip_fields` to make sure that you don’t accidentally try to use it:

```python
skip_fields = ['_ansible_check_mode', 'username','name','password','url']
```

Now your module is idempotent!


#### [Optional] Providing Facts via Modules

In this section, you’re going to update your module to provide a new fact, wp_ current_users. This will contain the list of users in your WordPress installation.

1\. To be able to display this variable, you will write a playbook that uses your new module. Create a file called `play.yml` in the same folder as `wp_user`, with the following contents:

```yaml
---
- hosts: all
  gather_facts: false
  tasks:
    - name: Update User
      wp_user: username=<your-name> password=your-password url="http://book.example.com" first_name="<your-name>"
    
    - debug: var=wp_existing_users
```

2\. Now, let’s update your module to return some facts. At the bottom of your module, update the `module.exit_json` line to return another key, `ansible_facts`:

```python
facts = {}
module.exit_json(changed=is_changed, user=dict(current_user), ansible_facts=facts)
```

3\. Finally, you need to update your module to populate this new facts variable. As you still have your list of `existing_users` from your earlier call to `wp.getUsers`, you can reuse that value and return it as a fact, naming it `wp_existing_users`:

```python
facts = {
  "wp_existing_users": existing_users
}
```

4\. Once you’ve done this, save the module and run `ansible-playbook` again. This time,
your `debug` call should output a list of users that exist in your WordPress install: 

```console
$ ansible-playbook -i 'localhost,' -M . -c local play.yml
```

Output:

```console
PLAY
***************************************************************************

TASK [Update User]
*************************************************************
ok: [localhost]

TASK [debug]
*******************************************************************
ok: [localhost] => {
    "wp_existing_users": [
        {
            "bio": "",
            "display_name": "michael",
            "email": "m@michaelheap.com",
            "first_name": "Michael",
            "last_name": "Heap",
            "nicename": "michael",
            "nickname": "michael",
            "registered": "2016-03-07T20:29:20",
            "roles": [
                "administrator"
            ],
            "url": "http://michaelheap.com",
            "user_id": "1",
            "username": "michael"
        } 
    ]
}
```

Anything returned under `ansible_facts` is now available, as with any other variable.

#### Conclusion

Wow! That was another bruiser, but you made it. You've learned a lot at this point. Now, one thing we can't teach you is how to decide whether to create a role of write a module, that's not an easy choice. But, at least you know how to do both. Next, you'll be working with Ansible in the Cloud! 

Here's the entire module, for the python section, for reference:

```python
#!/usr/bin/python
import xmlrpclib
from ansible.module_utils.basic import *
def main():
  module = AnsibleModule(
    argument_spec = dict(
      url = dict(required=True),
      username = dict(aliases=['name'], required=True),
      password = dict(required=False),
      first_name = dict(required=False),
      last_name = dict(required=False),
      user_url = dict(required=False),
      display_name = dict(required=False),
      nickname = dict(required=False),
      nicename = dict(required=False),
      bio = dict(required=False)
    ),
    supports_check_mode=True
  )
  params = module.params
  server = xmlrpclib.ServerProxy('%s/xmlrpc.php' % params['url'], use_datetime=True)
  existing_users = server.wp.getUsers(1, params['username'], params['password'])  
  current_user = None
  for u in existing_users:
   if u['username'] == params['username']:
      current_user = u
      break
  
  details = {}
  skip_fields = ['_ansible_check_mode', 'username','name','password','url']
  mappings = {"user_url": "url"}
  for k, v in params.iteritems():
   if k in skip_fields:
      continue
   if v:
      if k in mappings:
         k = mappings[k]
      details[k] = v
      
  is_changed=False
  for k,v in details.iteritems():
   if current_user[k] != details[k]:
      current_user[k] = details[k]
      is_changed = True
   if is_changed and not module.check_mode:
      server.wp.editProfile(1, params['username'], params['password'], details)

   module.exit_json(changed=is_changed, user=dict(current_user))

if __name__ == '__main__':
   main()
```  
