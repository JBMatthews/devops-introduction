# Ansible Playbook

### Environment Creation 

#### Testing Installation

1\. If everything went well, you should be able to run `VBoxManage --version` and `vagrant --version` and see output that looks something like the following:

```console
$ VBoxManage --version
```
Output:

```
5.2.6r120293
```

```console
$ vagrant --version
```
Output:

```
Vagrant 2.0.1
```

#### Bringing Vagrant Up

Now that you have all of your dependencies installed, it’s time to create the virtual machine on which you’re going to install packages and then configure with Ansible. 

1\. First, `cd` into your demo folder marked "ansible-playbook", then intialize Vagrant, like this: 

```console
$ cd ~/Desktop/ansible/ansible-students/ansible-playbook
$ vagrant init ubuntu/trusty64
```

2\. Once that file has been created, you can start your virtual machine by running `vagrant up`:

```console
$ vagrant up
```

3\. Your virtual machine is now created and running. You can check this by running vagrant status:

```console
$ vagrant status
```
Output:

```
Current machine states:

default                   running (virtualbox)

The VM is running. To stop this VM, you can run `vagrant halt` to
shut it down forcefully, or you can run `vagrant suspend` to simply suspend the virtual machine. In either case, to restart it again, simply run `vagrant up`.
```

#### Testing Vagrant's Configuration

1\. You can also log in to the virtual machine by running the `vagrant ssh` command.

2\. Once you’ve logged in, you can check that you have the correct machine by running `cat /etc/issue`:

```console
# cat /etc/issue
```
>Note: The (#) has been used here, rather than the ($) because this command is to be run inside our VM.

Output:

```
Ubuntu 14.04.5 LTS \n \l
```

3\. Once you've confirmed this, exit out of your machine:

```console
$ exit
```

Congratulations! You’ve just created and started a virtual machine with Vagrant. 

#### Vagrant Destruction and Re-Configuration 

1\. As you don’t need this virtual machine quite yet, let’s destroy it by running `vagrant destroy`, just like this:

```console
$ vagrant destroy
```

Output:

```
 default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
```

>Note: Notice, you do have to indicate yes by typeing 'y' and then pressing 'Enter'.

Once you run vagrant destroy, that machine is totally gone. Just like that! Pretty cool, huh?

2\. Open the Vagrantfile in your editor and add the following to the end of the file, just before the word end.

```vagrant
config.vm.provider "virtualbox" do |vb|
 vb.memory = "1024"
end
```

>Note: Remember from the lecture, this tells Vagrant that it needs to create a virtual machine with 1024mb of memory.

3\. Right at the bottom and before the word `end`, add the following contents to the file:

```vagrant
config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
end
```

This tells Vagrant to use Ansible to run the playbook named `playbook.yml` inside a folder named provisioning in the current directory.

4\. If you try to run `vagrant up` now, you’ll get an error, because that file doesn’t exist:

```console
$ vagrant up
```

Output:

```
...
==> default: Running provisioner: ansible...
`playbook` does not exist on the host: /path/to/playbook
...

<!--- So actually the error when I tested this lab came back as:
There is a syntax error in the following Vagrantfile. The syntax error
message is reproduced below for convenience:
.../Vagrantfile:74: syntax error, unexpected end-of-input, expecting keyword_end
```

5\. To correct this, create a folder named `provisioning` and a file inside it named `playbook.yml`, and that'll get us started.

```console
$ mkdir provisioning
$ vi provisioning/playbook.yml
```

>Note: Keep Vim open as you move to the next section.

### Writing Your First Playbook

#### Bare Essentials Playbook

1\. Now, tell Ansible to run on all available hosts by adding `- hosts: all` to our new playbook. After adding these lines, your playbook should now look like this:

```yaml
---
- hosts: all
```

2\. You'll need to add a section named `tasks`. Try to remember how from the lecture, but if you need help, peek ahead.

3\. Inside tasks, you are going to tell Ansible to just ping your machines to make sure that you can connect to them:

```yaml
---
- hosts: all
  tasks:
    - ping:
```

4\. Now, "provision" your newest changes to Ansible on the machine by executing: 

```console
$ vagrant provision
```

You should see output that looks like the following:

```console
==> default: Running provisioner: ansible...

PLAY [all]
********************************************************************

GATHERING FACTS
***************************************************************
ok: [default]

TASK: [ping ]
*****************************************************************
ok: [default]

PLAY RECAP
********************************************************************

default         : ok=2    changed=0    unreachable=0    failed=0
```

5\. Thankfully, Ansible lets you add a name to each task to explain its purpose. Let’s do that to our `ping` action now:

```yaml
---
- hosts: all
  tasks:
    - name: "Your Text Description Here"
      ping:
```

6. Run it! It will no longer say `TASK: [ping ]`. Instead, it will show the description that you provided.

#### Installation Additions

1\. Let’s add PHP by adding another module entry, like `ping:` to the `playbook.yml` file, so that it looks like the following:

```yaml
---
- hosts: all
  tasks:
    - name: Make sure that we can connect to the machine
      ping:
    - name: Install PHP
      apt: name=php5-cli state=present update_cache=yes
```

Previously, you used the `ping` module to connect to your machine. This time, you’ll be using the `apt` module.

2\. If you run `vagrant provision` again, it should attempt to install the `php5` package. Unfortunately, it will fail, giving a message such as the following:

```
$ vagrant provision
```

Output:

```console
...

TASK [Make sure that we can connect to the machine] ****************************
ok: [default]

TASK [Install PHP] *************************************************************
fatal: [default]: FAILED! => {"changed": false, "failed": true, "msg": "Failed to lock apt for exclusive operation"}
	to retry, use: --limit @path/to/playbook.retry

PLAY RECAP *********************************************************************
default                    : ok=2    changed=0    unreachable=0    failed=1   

Ansible failed to complete successfully. Any error output should be
visible above. Please fix these errors and try again.
```

3\. Ansible basically needs to sudo this command! However, let's add it to the playbook in such a way that the permission granted, can be reused by other commands. You'll do that by adding `become: true` to our playbook, like this:

```yaml
---
- hosts: all
  become: true
  tasks:
    - name: Make sure that we can connect to the machine
      ping:
    - name: Install PHP
      apt: name=php5-cli state=present update_cache=yes
```

4\. Once you’ve saved this change, run `vagrant provision` again. Ansible should tell you that PHP was installed successfully:

```console
$ vagrant provision
```

5\. You can add more steps to install nginx and mySQL by adding more calls to the `apt` module saying that you expect nginx and `mysql-server-5.6` to be present.

```yaml
---
- hosts: all
  become: true
  tasks:
    - name: Make sure that we can connect to the machine
      ping:
    - name: Install PHP
      apt: name=php5-cli state=present update_cache=yes
    - name: Install nginx
      apt: name=nginx state=present
    - name: Install mySQL
      apt: name=mysql-server-5.6 state=present
```

6\. As with the `php5-cli` package, this should show up in your Ansible output when you run `vagrant provision` again:

```console
$ vagrant provision
```

Output:

```console
...

TASK [Install PHP] *************************************************************
ok: [default]

TASK [Install nginx] ***********************************************************
changed: [default]

TASK [Install mySQL] ***********************************************************
changed: [default]

PLAY RECAP *********************************************************************
default        : ok=5    changed=2    unreachable=0    failed=0
```

#### Testing Installed Additions

At this point, you can log in to your virtual machine to make sure that everything is installed as you would expect it to be. 

1\. Like before, to do this, you run `vagrant ssh` to log in. Then, you can run a few commands to check whether certain programs are installed:

```console
# which php
```

Output:

```console
/usr/bin/php
```

```console
# which nginx
```

Output:

```console
/usr/sbin/nginx
```

```console
# which mysqld
```

Output:

```console
/usr/sbin/mysqld
```

2\. Before moving forward, be sure to exit the instance by typing `exit`

#### Playbook Simplification
1\. Go ahead and open up your playbook. The first thing to do is to delete the `ping` task.

2\. Now, let's pull out our `with_items` construct and combine it with the special `{{item}}` notation, so can compress our `apt` module installs. Try to put this into place without looking down at the code snippet, but the following is the end result of this emplementation:

```yaml
---
- hosts: all
  become: true
  tasks:
    - name: Install required packages
      apt: name={{item}} state=present update_cache=yes
      with_items:
        - php5-cli
        - nginx
        - mysql-server-5.6
```

3\. Run `vagrant provision` again, see that it will collapse all output for that one task into one block.

```console
$ vagrant provision
```

Output:

```console
==> default: Running provisioner: ansible...
PLAY [all]
********************************************************************

GATHERING FACTS
***************************************************************
ok: [default]

TASK: [Install required packages]
*********************************************
ok: [default] => (item=php5-cli,nginx,mysql-server-5.6)

PLAY RECAP
********************************************************************

default                    : ok=2    changed=0    unreachable=0    failed=0
```

#### Conclusion
Congratulations! You just put together your first playbook.
