# Roles in Ansible

### Preparation and Setup

#### Environment Configuration
Like before, we need to setup a development environment before we do anything else. Make sure you are completely outside of any previous lab folders or any other projects. Be sure to stop any previous virtual machines that may still be running, as well.

----

1\. Make sure you've halted the previous VM from any previous lab attempts, then navigate to the "ansible-roles" folder:

```console
$ vagrant halt     // Done within the "ansible-wordpress" folder
$ cd ~/Desktop/ansible/ansible-students/ansible-roles
```

2\. Confirm that your Vagrantfile is present in your lab folder, and that it matches the following specs:

```vagrant
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

>Note: Private Network IP may very well differ from that stated above. Make sure you take notice and make a note. Notice this is a copy on the previous lab's Vagrantfile.

3\. Go ahead and create a basic playbook. Try to implement the playbook on your own, but if you are still catching up, following these commands:

```console
$ mkdir provisioning
$ cd provisioning
$ vi playbook.yml
```

4\. Again, try to implement your playbook based on what you've already learned. Once you've done your best, then check your code against the following:

```yaml
---
- hosts: all
  tasks:
    - name: Test Connect Ping
      ping:
```

5\. Great! Now, bring your new VM up using our ole' familiar `vagrant up`.

### Exploring Ansible Roles

#### Ansible Galaxy
Like we learned in the lecture, roles are a core concept in Ansible. They have their own repository and accompanying command-line tool.

1\. In case you haven't already, go ahead and explore Ansible's Role Repository: `https://galaxy.ansible.com/`

>Note: If you haven't already created an account, take this time to go ahead and do it.

#### Create a Role
For offical projects, Virtuant uses “virt” as an identifier. Meaning that a role that installs PHP, authored by Virtuant will be named `virt.php`. Let’s create that role now. 

1\. Run the following commands in the same folder as playbook.yml:

```console
$ mkdir -p provisioning/roles
$ cd provisioning/roles
$ ansible-galaxy init virt.php
```

2\. Now, create two new files alongside it in the main.yml folder and include those files in the `main.yml` itself. 

```console
$ touch extensions.yml
$ touch php.yml
```

>Note: Confirm that `extensions.yml` and `php.yml` exist at the same level as `main.yml`.

3\. Now you have a clean separation between the tasks that install the core PHP packages and the tasks that install any additional extensions. You need to tell Ansible that these files exist, which you do by editing `tasks/main.yml` so that it looks like the following:

```yaml
---
- include: 'php.yml'
- include: 'extensions.yml'
```

### Splitting Up Your WordPress Playbook

#### Intialize Roles and a Playbook

Let’s jump right into splitting up your monolithic playbook into some unique roles. You’ll start by creating the roles that you’re going to need. 

1\. Make sure that you’re in your roles directory, and then run the following commands to generate some empty roles:

```console
$ ansible-galaxy init virt.nginx
$ ansible-galaxy init virt.mysql
$ ansible-galaxy init virt.wordpress
```

2/. Once you’ve created these roles, update `playbook.yml` so that they are included. Remember to add your roles before the tasks. Also, be sure to include `become: true`. Try to product the playbook on your own; the following is how that code should look:

```yaml
---
- hosts: all
  become: true
  roles:
    - virt.php
    - virt.nginx
    - virt.mysql
    - virt.wordpress
  tasks:
    - name: Test Connect Ping
      ping:
```

3\. At this point, you should run `vagrant provision` to make sure that your playbook is still formatted correctly.

#### Configuring virt.php
Start by populating your virt.php role. 

1\. Take the four tasks that are related to installing PHP from the last lab's playbook, and copy them into `roles/virt.php/tasks/main.yml`. 

>Note: Do NOT move (mv) any code of files, just copy, as to keep all previous work intact. 

After doing this, `roles/virt.php/tasks/main.yml` will contain the following four tasks:

```yaml
---
- name: Add the ondrej PHP PPA
  apt_repository: repo='ppa:ondrej/php'
  
- name: Update the apt cache
  apt: update_cache=yes cache_valid_time=3600
  
- name: Install PHP
  apt: name={{item}} state=present
  with_items:
    - php
    - php-fpm
    - php-mysql
    - php-xml
    
- name: Remove apache2
  apt: name=apache2 state=absent
```

2\. Go ahead and run `vagrant provision`, keeping in mind you're not done.

#### Configuring virt.mysql

You'll have to do all of them like we just did, but MySQL looks to be the next easiest one, so get that one out of the way.

1\. Open `roles/virt.mysql/tasks/main.yml`. Now, move all of the MySQL-related tasks. You’ll need to move the tasks named `Install MySQL` and `Create my.cnf`, as well as all tasks in between them.

2\. Remember, MySQL tasks used a template to populate `my.cnf` in your last lab. You’ll need to move it so that it lives inside the new role. You can do this by running: 

```console
$ cd ~/Desktop/ansible/ansible-students/ansible-roles
$ mkdir provisioning/roles/virt.mysql/templates
$ cp ~/Desktop/ansible/ansible-students/ansible-wordpress/provisioning/templates/mysql/my.cnf provisioning/roles/virt.mysql/templates
``` 

>Note: You'll need to run this in the same directory as your vagrantfile. If

3\. Finally, you’ll need to make a small change to the template task in your `virt.mysql` role. The `src` parameter for the template task is not correct. Once you make that change, the final task in `roles/virt.mysql/tasks/main.yml` should look like the following:

<pre>
- name: Create my.cnf
<b>template: src=my.cnf dest=/root/.my.cnf</b>
  when: mysql_new_root_pass.changed
</pre>

4\. Run `vagrant provision` again to ensure that your new role works as intended. 

You’re halfway through the migration!

#### Configuring virt.nginx

1\. Move the three tasks relating to nginx, out of our previous playbook and into `roles/virt.nginx/tasks/main.yml`. 

2\. Just as you did with the MySQL role, you’ll need to move the template you used, so that it lives inside your new `virt.nginx` role, by running: 

```console
$ cd ~/Desktop/ansible/ansible-students/ansible-roles
$ mkdir provisioning/roles/virt.nginx/templates
$ cp ~/Desktop/ansible/ansible-students/ansible-wordpress/provisioning/templates/nginx/default provisioning/roles/virt.nginx/templates
``` 

>Note: Be sure to copy, not move. You can use a file explorer to copy and paste, if you aren't comfortible enough to use terminal.

3\. Now, edit the `Create nginx config` task so that the `src` field doesn’t contain any folders. It should just say `default`, like this:

```yaml
- name: Create nginx config
  template: src=default dest=/etc/nginx/sites-available/default
  notify: restart nginx
```

4\. Nginx's task also has a handler, so open up `roles/virt.nginx/handlers/main.yml` and move your handler from the previous wordpress playbook to your new handlers file. Once you’ve moved it, `handlers/main.yml` will look like the following:

```yaml
---
# handlers file for virt.nginx
- name: restart nginx
  service: name=nginx state=restarted
```

5\. Great job! Now, run `vagrant provision` to test your playbook. Keep in mind you are not yet done.

#### Configuring virt.wordpress
This is your most complicated role, with ten different tasks, but it’s nothing to be afraid of. You can approach it just like the previous three roles, taking it step by step until it is fully migrated. 

1\. The first task to move is the one named `Copy wordpress.zip into tmp`, and the last one is named `Import WordPress DB`. Move these two tasks (and everything between them) into `roles/virt.wordpress/tasks/main.yml`.

2\. You’ll need to move the `wp-config.php` file so that it lives inside your role. You can do this by running: 

```console
$ cd ~/Desktop/ansible/ansible-students/ansible-roles
$ mkdir -p ~/Desktop/ansible/ansible-students/ansible-roles/provisioning/roles/virt.wordpress/templates
$ cp ~/Desktop/ansible/ansible-students/ansible-wordpress/provisioning/templates/wordpress/wp-config.php provisioning/roles/virt.wordpress/templates
```

3\. Don’t forget to update your `template` task too—its `src` parameter should only contain `wp-config.php` now:

```yaml
- name: Create wp-config
  template: src=wp-config.php dest=/var/www/book.example.com/wp-config.php
```

4\. There are no handlers in this role, however, you’ll need to copy the files relating to the `copy` module. The first thing to do is to move those files so that they live inside the `virt.wordpress` role:

Just as you moved the files relating to the template module, you’ll also need to move the files relating to the copy module. Files that the copy module uses live in the `files` directory. The first thing to do is to move those files so that they live inside the `virt.wordpress` role:

```console
$ cd ~/Desktop/ansible/ansible-students/ansible-roles
$ mkdir provisioning/roles/virt.wordpress/files
$ cp ~/Desktop/ansible/ansible-students/ansible-wordpress/provisioning/files/wordpress.zip provisioning/roles/virt.wordpress/files
$ cp ~/Desktop/ansible/ansible-students/ansible-wordpress/provisioning/files/wp-database.sql provisioning/roles/virt.wordpress/files
```

5\. Next, you’ll need to update your `copy` tasks to remove the `files/` section from the `src` parameter. Once you’ve done this, the tasks should look like the following:

```yaml
- name: Copy wordpress.zip into tmp
  copy: src=wordpress.zip dest=/tmp/wordpress.zip
- name: Copy WordPress DB
  copy: src=wp-database.sql dest=/tmp/wp-database.sql
  when: db_exist.rc > 0
```

>Note: If you provision your changes now, it will fail, because you've not installed the `unzip` tool. 

#### Configuring virt.common
At this point there are only two tasks remaining, and only one of them matters. Instead of adding it directy to the virt.wordpress role, you'll create another role for it and any future common package installations.

1\. Now, create a new role called virt.common, for our common package installations:

```console
$ ansible-galaxy init virt.common
```

>Note: Be sure to run the latter command in the roles folder. 

2\. Move the task that installs your common packages into `tasks/main.yml` in your new role, especially the `unzip` part!

3\. Once complete, add `virt.common` to the list of roles in your current playbook.

4\. Go ahead and delete the `ping` module from early, if you haven't already. Furthermore, delete the entire tasks section now that's it's empty.

Your playbook is looking a lot slimmer already!

```yaml
---
- hosts: all
  become: true
  roles:
    - virt.common
    - virt.php
    - virt.nginx
    - virt.mysql
    - virt.wordpress
```

5\. Make sure to run `vagrant provision` once more to ensure that things are still working.

#### Configuring Role Dependencies

1\. Open `roles/virt.wordpress/meta/main.yml` and delete it all. All of the information is optional so just delete it.

>Note: Notice that this is in the `meta` sub-folder, not the tasks' main folder.

2/. Great! Now, populate the file with only the required information. Add the following content to the file:

```yaml
dependencies:
  - virt.common
  - virt.php
  - virt.mysql
  - virt.nginx
```

3\. Next, edit your current `playbook.yml` so that only `virt.wordpress` is in your list of roles.

4\. As always, go ahead and see what happens when you provision these changes. Make sure it runs successfully.

5. Ready for the big reveal? Well, go ahead and navigate your broswer to `book.example.com` and confirm that your wordpress blog site is up and functional, just like before.

#### Conclusion

Can you believe all you've learned, and do you realize it's potential? Ansible roles are one of the most powerful parts of Ansible. They help keep your playbooks clean and readable. Remember, when creating a role, try to make sure that it is usable out of the box. Going forward, we’ll be using the roles that we created in this chapter to deploy multiple instances of WordPress in the same playbook.

