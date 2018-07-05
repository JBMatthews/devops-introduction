## Configure Jenkins Security

In this lab we will configure Jenkins to authenticate users against its internal user database, and enforce capability limitations on users.

At the end of this lab you will be able to:
1.	Enable security and select the internal user database
2.	Create users
3.	Assign global privileges to users
4.	Assign project-specific privileges to users.

----

###Part 1 Enable Jenkins Security

    1. Make sure Jenkins is started. Since we configured as windows service it will be started every time you start the machine.
    2. Go to the Jenkins console:

http://localhost:8080

    3. On the Menu click Manage Jenkins.


    4. Click Configure Global Security.
 
    5. Jenkins will display the Configure Global Security page.


    6. Under the Security Realm heading, select Jenkins own user database. Select
Allow users to sign up.


    7. Click the Save button at the bottom of the page.

At this point, we have enabled security, but we haven't created any users, nor have we actually applied an authorization requirement. Let's go ahead and add a couple of users.

Part 2 - Create an Administrative User
There are two ways to add users: We can do it through Jenkins' management console, or we can allow users to sign up themselves. Let's first use the management console to add an administrative user so we can lock down the security.
    1. In the “Manage Jenkins” page (the last part of the lab should have left you here), click on Manage Users.

    2. Click on Create User.

 
    3. The system displays the Sign Up page. Enter the following information in the appropriate fields:
Username:	admin
Password:	password Confirm Password:	password
Full name:	Administrative User
E-mail address:	admin@localhost.com
Note that the e-mail address is not actually verified to be a valid email address, but Jenkins will reject it unless it is in the usual email format.
    4. When the page looks like below, click on the Create User button.


    5. The system will display the list of current users, including the 'admin' user that you just created.


    6. Click on Manage Jenkins to return to the management console.
 
Part 3 - Enable Authentication
    1. Click on the link for Configure Global Security.

    2. Under the Authorization heading, select Project-based Matrix Authorization Strategy.

    3. When you click on the radio button above, Jenkins will display a list of global authorizations. We need to enter the 'admin' user here with full permissions, and then we'll add other users to individual projects. In the field labeled User/group to add:, enter admin, and then click Add.

    4. Jenkins displays the newly-added user in the list of users. Now we need to select all the permissions. You could click each permission box listed for 'admin' individually, but to save a little time, if you scroll the window horizontally all the way over to the right- hand side, you'll find a button that will select all the permissions in one operation . Find that button and click it.

    5. All check boxes will be selected. Click Save.
 
    6. Since we have altered the authorization strategy, Jenkins resets its security system, which requires us to log in again. You will see that wasadmin access has been denied. Click the log out link at the upper-right corner of Jenkins' home page..

    7. At the login screen, enter admin as the userid and password as the password, then click log in.


If for whatever reason, Jenkins doesn't let you log in, check with your instructor – you may need to reset the security system by editing the configuration file manually and then start over with the security setup.
    8. Do not save the password.
    9. Click the log out link at the upper-right corner of Jenkins' home page. Jenkins should display the login page again.

Part 4 - Create a Self-Signed-Up User
When we enabled Jenkins security, we left the checkbox selected for “Allow users to sign up”. As a result, there is a Create an Account link on the login page. Let's create a user that way, and then we'll go back and grant them privileges on a project.
    1. Click on Create an account in the login page.

 
    2. Jenkins will display the Sign up page. Enter the following information in the appropriate fields:
Username:	jane
Password:	password Confirm Password:	password
Full name:	Non-Administrative User
E-mail address:	jane@localhost.com
Note that the e-mail address is not actually verified to be a valid email address, but Jenkins will reject it unless it is in the usual email format.
    3. When the page looks like below, click on the Sign up button.


    4. Jenkins will display the Success window. Do not save the password.



    5. Click on the link to go to the top page.
    6. Since the new user has no permissions, access is denied.


    7. Click on the log out link, and then log back in using 'admin/password'.
 
    8. We should see the main dashboard page. Click on the SimpleGreeting job (we created this job in an earlier lab).
    9. Click Configure.
    10. In the configuration page, click on the checkbox marked Enable project-based security, to select it.

    11. When you select the checkbox, Jenkins will display a matrix of users and permissions. In the field marked User/group to add:, enter jane, and then click Add.

    12. In the row labeled jane, select the checkboxes for Discover , Read and
Workspace.

    13. Click Save.
    14. We also need to grant jane the 'overall read' permission. Click Back to Dashboard.
    15. Click the Manage Jenkins link, and then select Configure Global Security.
    16. Under the Authorization heading, in the field marked User/group to add: enter
jane and then click Add.


    17. In the row labeled jane, select the checkbox for Read.

    18. Click Save.
    19. Log out, and then log back in as 'jane/password'.
    20. Note that Jenkins only displays the 'SimpleGreeting' job. This is because Jane only
 
has read and discover access to this project.
    21. Click on the SimpleGreeting job.
    22. Notice that Jane doesn't have full privileges – there is no Build Now or Configure
option on the project.

    23. Log out of Jenkins.
    24. Close all.

### Conclusion

In this lab, we went through a series of steps to enable and configure Jenkins security. We saw how to create users administratively, and how to configure users who sign up using the self-sign-up screen.
