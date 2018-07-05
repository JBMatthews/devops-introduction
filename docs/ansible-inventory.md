# Ansible Inventory

### Getting Started

In Lab 01, you put together a simple playbook and ran it against your Vagrant machine using the vagrant provision command. You can run that same playbook against any machine that also has a running SSH server by using the ansible-playbook command. First, however, you need an inventory file.

In this chapter, we’ll take a look at what an inventory file is, how to run `ansible-playbook` without Vagrant, and how to leverage the inventory file when you have a complex inventory of machines with which you need to interact.

----

#### Inventory File Introduction

By default, Ansible will read `/etc/ansible/hosts` as its default inventory file. Using this file is not recommended, though. You should maintain a different inventory file for each project that you have and pass it to both the ansible and `ansible-playbook` commands using the `–i` option. Here is an example of passing a custom inventory file to ansible before running the ping module:

```console
$ ansible all –i /path/to/inventory –m ping
```

The inventory file in Ansible can be either an INI file or a JSON file. Most examples that you’ll find will use an INI file, while JSON files are only used when the inventory is dynamically generated (covered shortly). Using the INI format means that inventory files are generally very simple. They can be as simple as a list of host names to run against.

The following is an example of a simple inventory file:

```yaml
host1.example.com
host2.example.com
host3.example.com
192.168.9.29
```

In this example, we define a list of hosts to run against. Ansible will run against each of them in turn, starting with `host1.example.com` and ending with `192.168.9.29`. This is the simplest kind of inventory file that you can have. There is no additional information for any of the hosts; it is simply a list of hosts to run Ansible against.

If you run SSHD on a non-standard port, you can specify this in your inventory file as well. To do this, add a colon followed by the port number to the end of your hostname, as follows:

```yaml
host1.example.com:50822
```

If you are working with a large number of servers that share a common naming scheme, Ansible may be able to help. Ansible supports ranges in the inventory file, so instead of listing out every host by hand, you can use its range expansion functionality to do it automatically, as shown here:

```yaml
host[1:3].example.com
```

This is functionally equivalent to the following:


```yaml
host1.example.com
host2.example.com
host3.example.com
```

Range expansion also supports leading zeros (`[01:03]`) and alphabetic ranges (`[a:z]`). Unfortunately, only the range a:z is supported; that is, you can’t specify a range such as `[aa:dz]`, as Ansible does not know how to cope with this. If you need to define a range like this, you need to use two ranges:

```yaml
host[a:d][a:z].example.com
```

If you’re familiar with Python’s slice syntax, this may look familiar to you. As with slice, you can specify an optional third parameter step:

```
host[min:max:step].example.com
```

Step allows you to specify the increment between each host. There aren’t many use cases for this, but the inventory file supports it nonetheless:

```yaml
host[1:6:2].example.com
```

is equivalent to:

```yaml
host1.example.com
host3.example.com
host5.example.com
```

#### Running Without Vagrant

To test running Ansible by hand, you’ll need to edit your vagrantfile and enable private networking so that you can SSH into the machine. This is done by opening up the `vagrantfile` in your editor and uncommenting line29 (`config.vm.network "private_ network"`). 

Save this file, then run `vagrant halt && vagrant up` to restart your machine and enable this network. 

>Note: We pretend that it is not a Vagrant-managed machine, but rather another computer accessible via the network against which you need to run Ansible. 

`ansible-playbook` supports lots of different parameters, but you only need to specify a few to run Ansible. You need to tell `ansible-playbook` which servers you want to run on via the inventory file, and which playbook to run:

```console
$ ansible-playbook –i <inventory_file> provisioning/playbook.yml
```

Here’s a sample inventory file you can use to test running Ansible by hand. It contains the IP address of the machine to connect to, which user to log in as, and the path to a private key file to use. The private key is like a password, but it contains a private cryptographic signature that is used to verify your identity:

```
192.168.33.10 ansible_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/default/virtualbox/private_key
```

Save this as inventory (this should all be on a single line), and then run the following command. You should see the same output that you saw after running `vagrant provision`:

```console
$ ansible-playbook –i inventory provisioning/playbook.yml
```

#### Configuration Options in the Inventory

** THIS SECTION MOST LIKELY WON'T BE USED - DELETE AFTER TESTING THO **

When you were running Ansible against your Vagrant instance, you had to `set ansible_user` and `ansible_ssh_private_key_file` so that the correct credentials were used. The first set of options listed in Table 2-1 are related to the SSH connection that Ansible uses to push commands to remote servers. For most servers, you will only need to set `ansible_user` and `ansible_ssh_private_key_file`.

Table 2-1

Here’s an example inventory file that uses some of these options:

```
alpha.example.com ansible_user=bob ansible_port=50022
bravo.example.com ansible_user=mary ansible_ssh_private_key_file=/path/to/mary.key
frontend.example.com ansible_port=50022
yellow.example.com ansible_host=192.168.33.10
```

This sets an alternative port for alpha and frontend and different usernames with which to log in for alpha and bravo, specifies the key file for bravo, and says that yellow. example.com is actually just the IP address `192.168.33.10`. That’s a lot of additional information for such a small inventory file! It doesn’t stop there, though. There are even more options available to you.

Table 2-2 lists privilege-escalation options. We’ll cover privilege escalation a little later on when you’ll need to write some files to a location to which only the admin user has access (see Chapter 3), but these are the relevant settings that you can use in your inventory file.

Table2-2

These `privilege-escalation` options can be set in the inventory file, but they won’t actually be used unless you set `become: true` in your playbooks.
Given the following inventory file, alpha and bravo will both use the automation user when `become: true` is set in a playbook. frontend will use the ansible user, and yellow will use root, which is the default:

```
alpha.example.com ansible_become_user=automation
bravo.example.com ansible_become_user=automation
frontend.example.com ansible_become_user=ansible
yellow.example.com
```

It is important to note that this is not the user that was used to log in to the machine. (We use `ansible_user` for that. It is the user that you will change to when using `become: true`. You need to make sure that whichever user you change to has the permissions to perform the task you’re telling them to do.

        ------------------------

#### Inventory Variable Registration

In addition to setting the special Ansible variables in the inventory, such as `ansible_user` and `ansible_become_user`, you can set any variables that you may want to use later in a playbook or template. However, adding variables to the inventory file is generally notthe correct solution. There are several other places where you can define variables in a playbook, most of which are a better fit for this information. If you find that you are adding variables to an inventory file, think about whether this information really should be in the inventory. Is it a default value? Is it something related to a specific class of servers or a specific application? Chances are that there’s a better place for it to live. You will learn more about the different options for variable placement in Chapter 5.

If you decide that the inventory file is the correct place to add your variable, it’s very easy to do. 

For example, if you want a variable named vhost to be accessible in your playbooks, you could define a host as follows:

```yaml
host1.example.com vhost=staging.example.com
```

This can be useful in certain situations, such as when you run your staging and production websites from the same host and need to differentiate which one you’re working with via the inventory file. Imagine that you perform database changes as part of your playbook, but you don’t want to impact the live deployment when testing on staging. 

You can use the following inventory files to specify explicitly which database you want to work with:

```console
$ cat staging-inventory
```

Output:

```
alpha.example.com database_name=staging_db
```

Then,

```console
$ cat production-inventory
```

Output:

```
alpha.example.com database_name=prod
```

Here, the variable `database_name` will be available in your playbook so that you can perform any actions that you need to on the correct database. All you need to do is to provide the correct inventory file when you run Ansible. 

For example:

```console
$ ansible-playbook –i production-inventory playbook.yml
```

#### Inventory Groups

So far, we’ve worked with a simple list of hosts against which we will run Ansible. This doesn’t match up to the real world, however, where we have web servers, databases, load balancers, and more as targets. Being able to group these servers together and target them as a single entity is important. Ansible supports this use case through the use of inventory groups.

As your inventory files are in the INI file format, you can use the normal INI section- heading syntax to define a group of servers, as follows:

```yaml
[web]
host1.example.com
host2.example.com
[database]
db.example.com
```

In this inventory file, we have two hosts denoted as web servers and one as a database server. Square brackets are used as section markers in the INI format, so the group name is set to whatever appears in the square brackets.

When we run Ansible, we specify on which host groups our command should run. So far, we’ve used the special group all to say “run on all hosts listed.” We could say web or database to instruct Ansible to run only on that group of servers. The following command will run the ping module on the web group only:

```console
$ ansible web –i /path/to/inventory –m ping
```

You can also set this up in a playbook by changing the hosts: value at the top of your YAML file, as follows:

```yaml
- hosts: web
  tasks:
- ping:
```

Just as you can set variables for specific hosts, you can set variables for groups of hosts as well. To do this, use a special header in your inventory file:

```yaml
[web:vars]
apache_version=2.4
engage_flibbit=true
```

These variables will be available in the Ansible run for any hosts in the web group.

You can even create groups of groups! Imagine that you have a set of servers in production that are a mixture of CentOS 5 and CentOS 6 machines. Perhaps your inventory file would look like the following:

```yaml
[web_centos5]
host1.example.com
host2.example.com
[web_centos6]
shinynewthing.example.com
[database_centos5]
database.example.com
[reporting_centos6]
reporting.example.com
```

If you wanted to run something on just the CentOS 5 servers, you’d usually have to specify both `web_centos5` and `database_centos5`. Instead, you can create a group of groups using the `:children` suffix in your group name:

```yaml
[centos5:children]
web_centos5
database_centos5
[centos6:children]
web_centos6
reporting_centos6
```

Now, you just have to target centos5 hosts if you only want to run a command on the CentOS 5 servers. Moreover, you can set variables for this new group as well. It’s just a group, after all:

```yaml
[centos5:vars]
apache_version=2.2
[centos6:vars]
apache_version=2.4
```

Groups are very powerful and will be quite useful later on once we start defining variables outside of our inventory file.

#### An Example Inventory

It’s time to recap some of the things you’ve learned so far in this chapter. Here’s an inventory file for a fictional deployment containing a web server, a database, and a load balancer.

The environment was created over a period of time, which means that there are various operating systems involved with different users and methods of accessing the machines:

```
[web_centos5]
fe1.example.com ansible_user=michael ansible_ssh_private_key_file=michael.key
fe2.example.com ansible_user=michael ansible_ssh_private_key_file=michael.key

[web_centos6]
web[1:3].example.com ansible_user=automation ansible_port=50022 ansible_ssh_private_key_file=/path/to/auto.key

[database_centos6]
db.example.com ansible_user=michael ansible_ssh_private_key_file=/path/to/db.key

[loadbalancer_centos6]
lb.example.com ansible_user=automation ansible_port=50022 ansible_ssh_private_key_file=/path/to/lb.key

[web:children]
web_centos5
web_centos6

[database:children]
database_centos6

[loadbalancer:children]
loadbalancer_centos6
```

The oldest machines are running CentOS 5, and they use my personal account as the Ansible login. Newer machines have dedicated automation users with their own private keys. The database machine uses my personal account, but it has a different SSH key. Finally, the load balancer uses an automation user, but it doesn’t use the automation key—it has its own special load balancer key.

Finally, you group them all together. You want to be able to target web servers or database servers as a group, no matter whether they’re CentOS 5 or CentOS 6. Although the database group only has one child group in it for now, you may add CentOS 7 servers in the future. Having a group ready to use will save you lots of time.

Just by looking at this inventory file, you can see that there are seven machines in this deployment (fe1, fe2, web1, web2, web3, db, and lb). You know which user Ansible will log in as and which key it will use to do so. You even know which port the SSH daemon is running on.

A well-written inventory file isn’t just something for Ansible to use; it’s documentation about your deployment for new employees, contractors, and even for yourself when you need to refer back to it.







```

```
