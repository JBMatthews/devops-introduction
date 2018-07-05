## Configure Tools in Jenkins

In this lab you will verify that Jenkins Continuous Integration is already installed and you will configure it.


At the end of this lab you will be able to:
1.	Verify Jenkins is running
2.	Configure tools in Jenkins

----

### Configure Jenkins

After the Jenkins installation, you can configure few other settings to complete the installation before creating jobs.
You will be setting JDK HOME and Maven Installation directory.

1. To connect to Jenkins, open Firefox and enter the following URL .

	```url
	http://localhost:8080/
	```

2. Enter wasadmin as user and password and click Log in.
    
	![image001](https://user-images.githubusercontent.com/558905/37420219-aa9da114-278c-11e8-8c4b-19aa1663c437.png)

3. Don’t save the password if prompt or select Never Remember password for this site.

	![image003](https://user-images.githubusercontent.com/558905/37420222-aaf10e80-278c-11e8-965f-291d48230336.jpg)
 
5. Click Global Tool Configuration.

	![image006](https://user-images.githubusercontent.com/558905/37420228-acb41f0a-278c-11e8-824d-dcbef16e050d.jpg)

6. Scroll down and find the JDK section, Click Add JDK.

	![image007](https://user-images.githubusercontent.com/558905/37420229-acc1c524-278c-11e8-953e-40f15f0fd318.png)

7. Enter OracleJDK for JDK name.

8. Don't check the ‘Install automatically’ option. Uncheck if already checked.

9. Enter JAVA_HOME value as C:\Program Files\Java\jdk1.8.0_45

	> Note You may need to use another path if Java was installed in a different folder, contact your instructor or search for the right path and use it as JAVA_HOME.

	![image010](https://user-images.githubusercontent.com/558905/37420232-ace9bf2a-278c-11e8-9b9f-3e1c79ecdc87.jpg)

11. In the Maven section, click Add Maven.

	![image011](https://user-images.githubusercontent.com/558905/37420233-ad033176-278c-11e8-8ff8-74dee4b08a27.png)

12. Enter Maven for Maven name.

13. Uncheck the ‘Install automatically’ option.

14. Enter C:\Software\apache-maven-3.3.9 for MAVEN_HOME. Make sure this folder is correct.

15. Verify your settings look as below:

	![image013](https://user-images.githubusercontent.com/558905/37420235-ad2792a0-278c-11e8-814e-71c9df026ef2.png)

16. Scroll down and click Save.

### Conclusion

In this lab you configured the Jenkins Continuous Integration Server.
