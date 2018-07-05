# Parameterizing Playbooks

### Parameterizing Your Playbook 

Like we discussed in the lecture, we want to create Roles that are as simple and reusable, as possible. In the spirit of that same rule we want to take the roles you created in the last lab and make them dynamic, using variables. Right now our roles are static. If you want to change a configuration value, you have to edit the role directly. That sucks!

### WordPress Role

For this lab we've already provided the appropriate Vagrantfile, Playbook, and the other necessay files. That'll save you some time and help us get right down to it. So, get into the lab folder `ansible-parameterizing` and let's go:

----

1\. Okay, so go ahead and open up your playbook and confirm you have, this:

```yaml
---
- hosts: all
  become: true
  roles:
    - virt.wordpress
```

2\. Looks good? Let’s now update your playbook to specify some new variables. Any other values passed in at this time will be treated as variables that can be used in your tasks or templates:

```yaml
---
- hosts: all
  become: true
  roles:
    - role: virt.wordpress
      database_name: <your-database-name>
      database_user: <your-user-name>
      database_password: <your-password>
```

3\. Open up `roles/virt.wordpress/tasks/main.yml` and change any place that has the database name, user, or password hardcoded to use our new variables instead. I’ve highlighted the places and the changes to be made:

>Note: Ansible knows to look for variables that are wrapped in curly braces like so: `{{variable_name}}`.

<pre style="">
- name: Create WordPress MySQL database
  mysql_db: name="<b>{{database_name}}</b>" state=present

- name: Create WordPress MySQL user
  mysql_user: name="<b>{{database_user}}</b>" host=localhost password="<b>{{database_password}}</b>" priv="<b>{{database_name}}</b>.*:ALL" - name: 

- name: Does the database exist?
  command: mysql -u root <b>{{database_name}}</b> -e "SELECT ID FROM <b>{{database_ name}}</b>.wp_users  LIMIT 1;"
  register: db_exist
  ignore_errors: true
  changed_when: false

- name: Copy WordPress DB
  copy: src=files/wp-database.sql dest=/tmp/wp-database.sql
  when: db_exist.rc == 1
  
- name: Import WordPress DB
  mysql_db: target=/tmp/wp-database.sql state=import name="<b>{{database_name}}</b>"
  when: db_exist.rc == 1
</pre>

4\. You should run `vagrant provision` at this point to ensure that all of the new databases and users are being created.

5\. Once that’s completed successfully, you’ll need to update `wp-config.php` to use your variables as well. You use the same curly-brace syntax in a template as you do in a playbook:

```php
/** The name of the database for WordPress */
define('DB_NAME', '{{database_name}}');
/** MySQL database username */
define('DB_USER', '{{database_user}}');
/** MySQL database password */
define('DB_PASSWORD', '{{database_password}}');
```

6\. After making this change run `vagrant provision`, but that shouldn't be a surprise.

7\. You can  now log in using `vagrant ssh` and then run `cat /var/www/book.example.com/wp-config.php` to make sure that your new values are in the correct place. 

8\. Finally, log out of the virtual machine by running `exit`.

Great job! That one got a bit longer than most. Feel free to ask questions if you're lost, or you have any concerns.

### Customizing the Doman Name

Variables can be used for much more than just database names and passwords! Let’s update your WordPress role so that not only can you customize the database credentials, but you can also decide where on disk the application lives and what content the default post on the website will contain. 

1\. Let’s update the role so that instead of having a hardcoded domain, it accepts the domain as a variable. Edit `playbook.yml` and add another variable that tells Ansible the WordPress domain name. Call this one wp_domain and set it to `book.example.com`:

```yaml
- role: virt.wordpress
  database_name: <your-database-name>
  database_user: <your-user-name>
  database_password: <your-password>
  wp_domain: book.example.com
```

>Note: Take note of the login info you enter here and put it somewhere easliy accessible. 

Now that you have a variable to use, you need to update every place that contains the hardcoded location so it uses the variable instead. Searching for `/var/www/book.example.com` in the `roles` directory shows that it is used in three locations:

1. `roles/virt.nginx/templates/default`
2. `roles/virt.wordpress/files/wp-database.sql`
3. `roles/virt.wordpress/tasks/main.yml`

2\. Let’s edit the nginx configuration first. Open up `roles/virt.nginx/templates/default` to get us going. 

3\. Now, edit lines 6 and 7 so that they use the `wp_domain` variable, as follows: 

```nginx
server_name {{wp_domain}};
root /var/www/{{wp_domain}};
```

4\. The next file in the list is `wp-database.sql`. This is quite a large one, so you want to perform a find and replace, replacing `book.example.com` with `{{wp_domain}}`. 

>Note: There should be 5 changes to make in this file total.

5\. Finally, you need to update your wordpress tasks file. Again, exchange any occurrences of `book.example.com` with `{{wp_domain}}`. 

>Note: There should be 4 changes to make in this file.

6\. Once you’ve saved all of these changes, run `vagrant provision` again. It should complete successfully without any tasks reporting that they changed anything. 

7\. Finally, you come to specifying the default post title and content. Once again, you’ll need to edit `playbook.yml` and add some new variables:

```yaml
- role: virt.wordpress
  database_name: michaelwp
  database_user: michaelwp
  database_password: bananas18374
  wp_domain: book.example.com
  initial_post_title: Hey There
  initial_post_content: >
  This is an example post. Change me to say something interesting.
```

8\. Let’s open up `wp-database.sql` and make it use the variables that you defined instead of hardcoded values. The default post title is “Hello world!” Search `wp-database.sql` for this string and change it to use `{{initial_post_title}}` instead. 

>Note: Remember, the default post title and content are controlled by the database file that you import.

9\. Next, look at the field just before the title (the one that starts with “Welcome to WordPress”). This is the default post that will be imported. Delete everything between the single quotes and replace it with `{{initial_post_content}}`.

You’re almost done! 

10\. Before, you used the `copy` module to get the `wp-database.sql` file onto the VM. You’ll need to use the `template` module here. 

To do this, edit `roles/virt.wordpress/tasks/main.yml` and change the word “copy” to “template” for the "Copy WordPress DB" task:

```yaml
- name: Copy WordPress DB
  template: src=wp-database.sql dest=/tmp/wp-database.sql
  when: db_exist.rc > 0
```

11\. As you’re now using the `template` module, you also need to change where `wp-database.sql` lives. Move it out of the files directory and into the `templates` directory with the following command:

```console
$ mv ~/Desktop/ansible/ansible-students/ansible-roles/provisioning/roles/virt.wordpress/files/wp-database.sql ~/Desktop/ansible/ansible-students/ansible-parameterizing/provisioning/roles/virt.wordpress/templates
```

12\. Run `vagrant destroy` followed by `vagrant up` in your terminal in the same directory as your vagrantfile. 

### The Big Reveal

Ready to taste the fruits of your labor? Look over the last few steps taken and make sure you understand how you got here. Once you feel comfortable with what you've learned in this lab, continue on to the following steps to conclude this demo.

1\. Once you've got your instance back up, go ahead and provision:

```console
$ vagrant provision
```

2\. Now, visist your URL (`book.example.com`) in your browser to confirm functionality. 

3\. Notice that the initial post content and title have changed, as you directed. Just for fun, go ahead and change the varilble values again in your playbook. Put whatever you'd like, just make sure it's memorable.

4\. Now, destroy, reconfigure and provisiong these changes, like you've done so many times before:

```console
$ vagrant destroy
$ vagrant up
$ vagrant up provision
```

5\. Revisit and refresh your previously designated URL (`book.example.com`), to confirm the changes you made.

Do you see it? Pretty awesome, huh? You did that!

#### Conclusion

Wow! Great job. Can you believe how much you've learned? I hope you are proud of yourself. Now you know how to parameterize your playbook, making funcitonality more easily repeatible and customizible. Variables are at the very core of getting the most out of Ansible. Being able to perform actions that are conditionally dependent on your environment and user-specified inputs means that you can write your playbooks in such a way that they always do the correct thing, no matter which environment they’re being run in. 
