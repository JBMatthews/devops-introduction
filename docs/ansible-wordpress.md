# Ansible and WordPress

### Establishing Development Environement

#### Environment Configuration
In this lab, we’ll install all of the required dependencies, fetch the WordPress source files from their release page, and automatically install a new instance.
Before we get started, we need an environment in which to build this playbook. As we did previously, we’ll be using Vagrant for this job. 

----
1\. Create a new Vagrant machine so that we’re starting with a clean slate. Run the following commands in your terminal:

```console
$ cd ~/Desktop/ansible/ansible-students/ansible-wordpress
$ vagrant init ubuntu/trusty64
```

2\. In addition to setting up networking, you’ll also need to allocate slightly more memory to the VM, like we did in the first demo. Once you’ve made these changes, your vagrantfile should look like this:

```ruby
Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
	config.vm.network "private_network", ip: "192.168.33.20"
	config.vm.provider "virtualbox" do |vb|
        vb.memory = "1024"
    end
    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "provisioning/playbook.yml"
	end
end

```

>Note: Private Network IP may very well differ from that stated above. Make sure you take notice and make a note.

3\. Go ahead and run `vagrant up`, to confirm a successful implementation.


#### Installing Dependencies
1\. Like we've already seen, you start by creating a simple playbook that shows that Ansible can run against your Vagrant machine:

```console
$ mkdir provisioning
$ vi provisioning/playbook.yml
```

2\. In `provisioning/playbook.yml`, we specify on which hosts the playbook should run as well as a set of tasks to run. Just implement the `ping` module for now, like before:

```yml
---
- hosts: all
  become: true
  tasks:
    - name: Make sure we can connect
      ping:
```

3\. At this point, you should run `vagrant provision` again to prove that you can connect to it.

### Installation

#### Installing PHP

1\. Now that you know Ansible will run, let’s install PHP. Add the following to your playbook in the tasks section:

```yml
# PHP
- name: Add the ondrej PHP PPA
  apt_repository: repo='ppa:ondrej/php'
```

>Note: Remmeber, PPA stands for Personal Package Archive and it's what's used to assist the installation process.

2\. Once that’s installed, the next step is to install PHP. As you’ve added a PPA, you’ll want to update the apt package cache:

```yml
- name: Update the apt cache
  apt: update_cache=yes cache_valid_time=3600
  
- name: Install PHP
  apt: name=php state=present
```

3\. Run `vagrant provision` again after adding these tasks, make sure it is completed successfully. 

4\. To make sure that things are working correctly, you can run `vagrant ssh` and log in to the machine, like you've done before.

5\. Once you’re logged in, run `which php` and make sure that it yields something similar to the following:

```console
$ which php
```

Output:

```console
/usr/bin/php
```

>Note: Once that runs, go ahead and exit out of the VM.

6\. That looks good, so let’s continue and install all of the other PHP packages that you’ll need. Let’s use `with_items` to make the playbook easier to read.

```yml
- name: Install PHP
  apt: name={{item}} state=installed
  with_items:
    - php
    - php-fpm
    - php-mysql
    - php-xml
```

>Note: You're only to change the "Install PHP" section.

7\. Unfortunately, installing PHP also installs Apache2. You don’t want to use that in this exercise. There’s no way around this, but you can remove it as soon as it’s installed by adding the following task to your playbook:

```yml
- name: Remove apache2
  apt: name=apache2 state=absent
```

8\. Run `vagrant provision` to check functionality.

Great job!

#### Installing MySQL
1\. Once you have PHP installed (and Apache removed), you can move on to the next dependency, MySQL. Add the following to your playbook:

```yml
# MySQL
- name: Install MySQL
  apt: name={{item}} state=present
  with_items:
    - mysql-server-5.6
    - python-mysqldb
```

2\. Now, you should run `vagrant provision` now to install all of the PHP and MySQL packages. It may take a few minutes, but it should complete successfully.

#### [Optional] MySQL Security  
Ansible installs MySQL with an empty root password and leaves some of the test databases accessible to anonymous users. 

1\. To change the default password, you need to generate a password to use. To do this, you can use the `openssl` utility to generate a 15-character password. Add the following to your playbook:

```yml
- name: Generate new root password
  command: openssl rand -hex 7
  register: mysql_new_root_pass
```

> Note: Remember, the register keyword lets you save the return value of commands as a variable for use later in a playbook.

2\. The next thing to do is to remove the anonymous users and test databases. This is very straightforward, thanks to the `mysql_db` and `mysql_user` modules. You need to do this before you change the root password so that Ansible can make the changes. Again, you need to add some tasks to your playbook:

```yml
- name: Remove anonymous users
  mysql_user: name="" state=absent

- name: Remove test database
  mysql_db: name=test state=absent
```

3\. To change the root password and output it to the screen, use the special `ansible_hostname` variable that evaluates to the current machine’s hostname and then set the password for the three different formats used to denote localhost:

```yml
- name: Update root password
  mysql_user: name=root host={{item}} password={{mysql_new_root_pass.stdout}}
  with_items:
    - "{{ ansible_hostname }}"
    - 127.0.0.1
    - ::1
    - localhost
    
- name: Output new root password
  debug: msg="New root password is {{mysql_new_root_pass.stdout}}"
```

Great job! You're halfway there.

#### Creating a New Config File
This is actually quite a lot of work! At this point, your installation is secure, but you’re not quite done. Like we learned, Ansible expects to be able to run database commands without a password, which was fine when you didn’t have a root password, but will fail now that you do. You need to write out a new config file (located at `/root/.my.cnf`) containing the new root password so that the root user can run MySQL commands automatically.

1\. First, you need to create a folder to hold your template and create the file that you are going to copy over. Run these commands from your terminal, in the same directory as your vagrantfile, to create the required folders and files:

```console
$ mkdir -p provisioning/templates/mysql
$ vi provisioning/templates/mysql/my.cnf
```

2\. Once you’ve created `my.cnf`, edit it and make sure that it has the following contents:

```cnf
[client]
user=root
password={{ mysql_new_root_pass.stdout }}
```

3\. You also need to tell Ansible to copy this template into your environment; this is done using the template module, as discussed in the lecture. Add the following task to your playbook: 

```yml
- name: Create my.cnf
  template: src=templates/mysql/my.cnf dest=/root/.my.cnf
```

This file will contain the username and password for the root MySQL user. 

4\. While it’s not a bad thing to rotate root passwords frequently, this may not be the behavior that you are seeking. To disable this behavior, you can tell Ansible not to run certain commands if a specific file exists. Ansible has a special creates option that determines if a file exists before executing a module:

```yml
- name: Generate new root password
  command: openssl rand -hex 7 creates=/root/.my.cnf
  register: mysql_new_root_pass
```

If the file `/root/.my.cnf` does not exist, `mysql_new_root_pass.changed` will be true, and if it does exist, it'll be set to false.

5\. Here’s a small set of example tasks that show the new root password if `.my.cnf` does not exist and show a message if it already exists:

```yml
- name: Generate new root password
  command: openssl rand -hex 7 creates=/root/.my.cnf
  register: mysql_new_root_pass
# If /root/.my.cnf doesn't exist and the command is run
- debug: msg="New root password is {{ mysql_new_root_pass.stdout }}"
  when: mysql_new_root_pass.changed
# If /root/.my.cnf exists and the command is not run
- debug: msg="No change to root password"
  when: not mysql_new_root_pass.changed
```

6\. Once you make the change to add `creates=/root/.my.cnf`, you should add a `when` argument to all of the relevant operations. After making these changes, the MySQL section of your playbook should look like this:

>Note: Make sure you are able to spot the changes we are making and that you understand why they are being made.

```yml
# MySQL
- name: Install MySQL
  apt: name={{item}}
  with_items:
    - mysql-server
    - python-mysqldb
- name: Generate new root password
  command: openssl rand -hex 7 creates=/root/.my.cnf 
  register: mysql_new_root_pass
- name: Remove anonymous users 
  mysql_user: name="" state=absent 
  when: mysql_new_root_pass.changed
- name: Remove test database 
  mysql_db: name=test state=absent 
  when: mysql_new_root_pass.changed
- name: Output new root password
  debug: msg="New root password is  {{mysql_new_root_pass.stdout}}" 
  when: mysql_new_root_pass.changed
- name: Update root password
  mysql_user: name=root host={{item}} password={{mysql_new_root_pass.stdout}} 
  with_items:
    - "{{ ansible_hostname }}"
    - 127.0.0.1
    - ::1
    - localhost
  when: mysql_new_root_pass.changed
- name: Create my.cnf
  template: src=templates/mysql/my.cnf dest=/root/.my.cnf 
  when: mysql_new_root_pass.changed
```

7\. Run vagrant provision now to generate a new root password and clean up your MySQL installation. If you run `vagrant provision` again, you should see that all of these steps are skipped:

```console
TASK [Remove anonymous users]
**************************************************
skipping: [default]
```

#### Installing Nginx

1\. Now, let’s install nginx by adding the following to the end of playbook.yml:

```yml
# nginx
- name: Install nginx
  apt: name=nginx state=present
  
- name: Start nginx
  service: name=nginx state=started
```

2\. Run `vagrant provision` again to install nginx and start it running.

3\. Now, visit `192.168.33.20` in your web browser, you will see the “Welcome to nginx” page.

>Note: This IP is the one you've established in your Vagrantfile. It may vary from the one above, check your Vagrantfile, if needed.

![image](https://user-images.githubusercontent.com/21102559/32392705-0895e2d2-c0ad-11e7-8d23-1bdcf4f379b0.png)

#### Nginx Forwarding Fixes

Pretty cool, huh? But, this isn’t what you want your users to see. You want them to see WordPress!

1\. So, you need to change the default nginx virtual host to receive requests and forward them. Run the following commands in the same directory as your Vagrantfile to create a template file that you’ll use to configure nginx:

```console
$ mkdir provisioning/templates/nginx
$ touch provisioning/templates/nginx/default 
```

2\. You’ll also need to copy this file onto your remote machine using the template module. Let’s add a task to your playbook to do this:

```yml
- name: Create nginx config
  template: src=templates/nginx/default dest=/etc/nginx/sites-available/default
```

3\. Edit `provisioning/templates/nginx/default` and make sure that it contains the following content:

```txt
server {
        server_name book.example.com;
        root /var/www/book.example.com;

        index index.php;
        
        location = /favicon.ico {
                log_not_found off;
                access_log off;
	      }
        location = /robots.txt {
                allow all;
                log_not_found off;
                access_log off;
	      }
        
	      location ~ /\. {
                deny all;
	      }	
 	      location ~* /(?:uploads|files)/.*\.php$ {
                deny all;
	      }	
        
	      location / {
                try_files $uri $uri/ /index.php?$args;
	      }
        rewrite /wp-admin$ $scheme://$host$uri/ permanent;

        location ~*
^.+\.(ogg|ogv|svg|svgz|eot|otf|woff|mp4|ttf|rss|atom|jpg|jpeg|gif|png|ico|zip|tgz|gz|rar|bz2|doc|xls|exe|ppt|tar|mid|midi|wav|bmp|rtf)$ {
                access_log off;
                log_not_found off;
	               expires max;
	      }	

	      location ~ [^/]\.php(/|$) {
                 fastcgi_split_path_info ^(.+?\.php)(/.*)$;
                 if (!-f $document_root$fastcgi_script_name) {
			                   return 404; 
		             }
		             include fastcgi_params;
		             fastcgi_index index.php;
		             fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
		             fastcgi_pass php;
	      }
}

```

#### Adding Nginx Upstream

1\. Now, you need to create an upstream definition in the configuration file so that nginx knows where to pass the request on to. Add the following at the **top** of your template before the opening server { line }:

```txt
        upstream php {
                server unix:/run/php/php7.2-fpm.sock;
}
```

>Note: Understand that php7.2 made not be right and you'll only know that by doing the next step.

2\. [Important] Remember from the lecture, you'll need to confirm which socket your PHP-FPM pool is listening on. If the results are differ from the code sample above, you will have to update the code. Go ahead an ssh into your machine and run the following commands:

```console
$ vagrant ssh
# ls /etc/php/
# cat /etc/php/7.X/fpm/pool.d/www.conf  | grep "listen ="
# exit
```

>Note: Remember, pay close attention to whether ($) or (#) are used, because they indicate where the code is to be run.

3\. Make sure that you run `vagrant provision` to bring everything up to date.

### Tasks & Handlers

We learned in the lecture that we face a unquie challenge here. Nginx needs to be restarted in order to pick-up changes, but we don't want Nignx to restart everytime we run our playbook. The best way to "handle" things that need to be restarted, only when things change, is to use a *handler*. 

#### Handler Configuration

1/. Add the following lines of code to your playbook, putting them on the same level and indentation as `tasks`:

```yml
handlers:
    - name: restart nginx
      service: name=nginx state=restarted
```

2\. You can trigger it whenever your `config` file changes, by updating the "Create nginx config" task, to look like this:

<pre>
- name: Create nginx config
  template: src=templates/nginx/default dest=/etc/nginx/sites-available/default
  <b>notify: restart nginx</b>
</pre>

3\. Be sure to save it! But, this feels like a good opportunity to run `vagrant destroy`, followed by `vagrant up` to confirm that everything is installed and configured correctly.

#### Handler and Configuration Testing

After running vagrant up, your new config should rollout and nginx should be restarted. 

1\. To test this, include the IP address and domain that you’ve been using to the bottom of the `/etc/hosts` file, on your host machine (not your VM):

```txt
192.168.33.20 book.example.com
```

2\. Now, as before, log in to the virtual machine with `vagrant ssh`.

3\. Once you've successfully logged in, run the following commands to formulate the test display:

```console
# sudo mkdir -p /var/www/book.example.com
# echo "<?php echo date('H:i:s'); " | sudo tee /var/www/book.example.com/index.php
```

4\. Always remember to exit out of your instances, before running further commands!

```
# exit
```

5\. Finally, visit `http://book.example.com` in your browser. You should see the current time. 

Now, that is pretty cool, huh? I hope you're proud of yourself.

### WordPress: Download, Install and Configure

#### Manual Download and Placement

1\. You can download the latest release with a command-line HTTP client named curl:

```console
$ mkdir -p provisioning/files
$ curl https://wordpress.org/latest.zip > provisioning/files/wordpress.zip
```

2\. You’ll copy it into the `/tmp` directory by adding the following to your playbook under the tasks section:

```yml
# Wordpress
- name: Copy wordpress.zip into tmp
  copy: src=files/wordpress.zip dest=/tmp/wordpress.zip
```

#### WordPress Install Configuration

1\. The first thing that you’ll need to do is to extract `wordpress.zip`. Ansible ships with a module named unarchive that knows how to extract several different archive formats:

```yml
- name: Unzip WordPress
  unarchive: src=files/wordpress.zip dest=/tmp copy=no creates=/tmp/wordpress/wp-settings.php
```

2\. Remember from the lecture, unzip doesn't come installed, so add this to your playbook (before you install PHP) to make sure it is:

```yml
- name: Install required tools
  apt: name={{item}} state=present
  with_items:
    - unzip
```

3\. You will also need to add a `creates` argument so that the command is idempotent:

```yml
- name: Create project folder
  file: dest=/var/www/book.example.com state=directory
  
- name: Copy WordPress files
  command: cp -a /tmp/wordpress/. /var/www/book.example.com creates=/var/www/book.example.com/wp-settings.php
```

4\. Once this has run, visit http://book.example.com in your web browser; you should see a WordPress installation screen.

![image](https://user-images.githubusercontent.com/21102559/32393162-e089e0ca-c0ae-11e7-9cbb-42e37535620e.png)

#### Create MySQL User Credentials

1\. You will not want to give WordPress root access to your database, so let’s create a dedicated MySQL user to use by adding the following tasks to your playbook:

```yml
- name: Create WordPress MySQL database
  mysql_db: name=wordpress state=present
  
- name: Create WordPress MySQL user
  mysql_user: name=wordpress host=localhost password=bananas priv=wordpress.*:ALL
```

Like we learned in the lecture, this will create a database called wordpress and a user called wordpress, with the password bananas.

>Note: Okay, so your password doesn't have to be "bananas" but you get the point!

2\. After running Ansible to create the database and user, go back to your web browser and continue the installation process from the GUI.

3\. Create `provisioning/templates/wordpress/wp-config.php` and paste your config file into it. 

4\. Once that’s done, add a task in your playbook to copy this file into the correct place:

```yml
- name: Create wp-config
  template: src=templates/wordpress/wp-config.php dest=/var/www/book.example.com/wp-config.php
```

5\. After adding this task, run Ansible again by running the `vagrant provision` command in your terminal. And voilà! 

>Note: Wait, no voilà? When you run Ansible, you may get an error message similar to the following:
`AnsibleError: ERROR! template error while templating string`<br>
If you get this error message, take a look at the contents your wp-config.php file. Do you see any place that has either `{{ or }}` in a string? Unfortunately, WordPress can generate this string as part of its secret keys. However, as you’re using Ansible’s template module, those characters have a special meaning. If your `wp-config` file contains them, feel free to edit the file and change them to any other character.

6\. Once Ansible has run successfully, go back to your web browser and click “Run the install.” It will ask you a few questions. Answer these questions and click on “Install WordPress.” 

7\. If you visit http://book.example.com now in your browser, you should see a WordPress install up and running with a “Hello World” post waiting to greet you. 

>Note: If your browser shows an error message relating to timeouts, make sure that you have added book.example.com to your hosts file, as discussed earlier in this chapter.

Okay, now voilà? Great job! We are almost there, so let's finish strong.

#### Making a Backup

Now, you'll need to make a backup, so that if you were to destroy this instance you could bring it back up at 100%. As it is right now, you would be 90 percent of the way to a WordPress install. You would end up at that final screen where you need to provide details about your website. All of that information is stored in the database, so let’s make a backup and have Ansible automatically import it.

1\. Log in to the environment with `vagrant ssh` and continue on to the next step.

2\. Run the following commands to create a backup SQL file to be used by your playbook:

```console
# sudo su -
# mysqldump wordpress > /vagrant/provisioning/files/wp-database.sql
# exit
# exit
```

>Note: Again, note that we've used (#) here, because these commands are to be run inside our machine.

3\. We’re going to use a new feature we discussed in the lecture, `ignore_errors`. Like we learned, when a command fails with a non-zero exit code, Ansible throws the error back to you. Using `ignore_ errors` on a command tells Ansible that it’s OK for that command to fail:

```yml
- name: Does the database exist?
  command: mysql -u root wordpress -e "SELECT ID FROM wordpress.wp_users LIMIT 1;"
  register: db_exist
  ignore_errors: true
```

4\. If you need to import the database, you’ll need to copy your database to the remote environment before you import it, so you will need two tasks to perform the import:

```yml
- name: Copy WordPress DB
  copy: src=files/wp-database.sql dest=/tmp/wp-database.sql
  when: db_exist.rc > 0
  
- name: Import WordPress DB
  mysql_db: target=/tmp/wp-database.sql state=import name=wordpress
  when: db_exist.rc > 0
```

5\. Make sure to add the above lines of code to your playbook, but once you're done, run `vagrant provision` to finialize our changes. Pay close attention to which tasks are skipped!


#### Making It Idempotent

1\. Go ahead and run `vagrant provision`, again.

Like we learned in the lecture, it isn't ideal to have a task that states *changed* every time Ansible runs. It could cause real trouble! Do you remember which task is causing this issue?

2\. Here’s a simple example of how you can use `changed_when`. List out the contents of the `/tmp` directory and if see the word "wordpress" occurs anywhere in the output. If so, Ansible will report that the task changed something.

```yml
- name: Example changed_when
  command: ls /tmp
  register: demo
  changed_when: '"wordpress" in demo.stdout'
```  

3\. If you edit the task that checks the database so that it looks like the following, your playbook will be fully idempotent again:

```yml
- name: Does the database exist?
  command: mysql -u root wordpress -e "SELECT ID FROM wordpress.wp_users
  LIMIT 1;"
  register: db_exist
  ignore_errors: true
  changed_when: false
```
#### Conclusion

At this point, you can run `vagrant destroy` and then `vagrant up` to destroy your environment and spin it up as an empty box. Ansible will run and automatically provision your WordPress install for you. It may take a few minutes, as it’s installing all of your dependencies as well as configuring WordPress.
