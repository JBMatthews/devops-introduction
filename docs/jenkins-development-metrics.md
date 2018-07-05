## Add Development Metrics

We are going to integrate code coverage metrics using the Cobertura plugin.
Code coverage is an indication of how much of your application code is actually executed during your tests—it can be a useful tool in particular for finding areas of code that have not been tested by your test suites. It can also give some indication as to how well a team is applying good testing practices such as Test-Driven Development or Behavior-Driven Development.

At the end of this lab you will be able to:
1.	Install the Jenkins Cobertura Plugin
2.	Configuring build tools
3.	Run the code coverage without Jenkins

----

### Part 1 Install the Jenkins Cobertura Plugin

1. Make sure Jenkins is started. Since we configured as windows service it will be started every time you start the machine.

2. Go to the Jenkins console at:

http://localhost:8080


3. To install a new plugin, click Manage Jenkins on the left.

4. Click on the Manage Plugins entry.

![image001](https://user-images.githubusercontent.com/558905/37434281-85a2ef1c-27b5-11e8-9f2e-8dbeb9d029db.png)

5. Click on Available tab.
 
![image003](https://user-images.githubusercontent.com/558905/37434283-85c62342-27b5-11e8-8042-5bcc519415e2.png)

6. Type cobertura in the Filter and then check the check-box next to Cobertura Plugin.

![image005](https://user-images.githubusercontent.com/558905/37434285-86196ee4-27b5-11e8-9b2e-39ee5465c748.jpg)

7. Click on the Download now and Install after restart button at the bottom of the screen.

![image006](https://user-images.githubusercontent.com/558905/37434286-862f4bc4-27b5-11e8-972c-2c21f06c2196.png)

8. Select the checkbox for Restart Jenkins....

![image007](https://user-images.githubusercontent.com/558905/37434287-8642954e-27b5-11e8-928a-9bd3ce2119ce.png)

At this point, Jenkins should restart itself. If it doesn't return to the main screen within a few minutes, you may need to use the 'Services' portion of the Windows Control Panel to restart the service manually. Consult your instructor in case of difficulty.

9. If ask to login use wasadmin for user and password.

10. Click Back to Dashboard.

### Part 2 Enable Jenkins Reporting

In this section, we'll configure Jenkins to publish the Cobertura coverage report, and then we'll add coverage testing to the project itself.

1. Click on the job we created for SimpleGreeting.

![image009](https://user-images.githubusercontent.com/558905/37434290-86655aca-27b5-11e8-94d1-6a4459647b9f.jpg)

2. On the left-hand menu, click Configure.

3. Scroll down to the Post-Build Actions section.

![image010](https://user-images.githubusercontent.com/558905/37434291-86768e3a-27b5-11e8-97b5-fd4a505afbec.png)
![image011](https://user-images.githubusercontent.com/558905/37434292-868765a2-27b5-11e8-87fc-5ac2c37531f2.jpg)
![image012](https://user-images.githubusercontent.com/558905/37434293-869a4834-27b5-11e8-80c1-94b6d95896cd.png)
![image013](https://user-images.githubusercontent.com/558905/37434294-86b06b6e-27b5-11e8-86d7-a073a881e8a1.jpg)
![image014](https://user-images.githubusercontent.com/558905/37434295-86c0e2c8-27b5-11e8-946f-b2472b79f8ce.jpg)
![image015](https://user-images.githubusercontent.com/558905/37434296-86cab5aa-27b5-11e8-9361-77b5564b46af.jpg)
![image016](https://user-images.githubusercontent.com/558905/37434297-86dbeb4a-27b5-11e8-9f25-d420080f6aa3.png)
![image017](https://user-images.githubusercontent.com/558905/37434298-86eb46c6-27b5-11e8-9a6a-6e75e013905a.jpg)
![image018](https://user-images.githubusercontent.com/558905/37434299-87070712-27b5-11e8-8366-27bbde780bfe.jpg)
![image019](https://user-images.githubusercontent.com/558905/37434300-8714aeee-27b5-11e8-9e36-bfb9389b932c.png)
![image020](https://user-images.githubusercontent.com/558905/37434301-874e62a6-27b5-11e8-8be5-b90f0652411b.jpg)
![image021](https://user-images.githubusercontent.com/558905/37434302-8763c236-27b5-11e8-8ce4-435efabbd94a.png)
![image022](https://user-images.githubusercontent.com/558905/37434303-877a83a4-27b5-11e8-8655-7cfd3422eb94.png)
![image023](https://user-images.githubusercontent.com/558905/37434304-87925236-27b5-11e8-9ef6-36d4f363a755.jpg) 

4. Click on the Add post-build action button and then select Publish Cobertura Coverage Report.

5. Enter the following for the Cobertura XML Report Pattern

**/target/site/cobertura/coverage.xml


6. Scroll up to find the Build section.



7. In the Goals and Options text box, enter the following:

clean install cobertura:cobertura


8. Click Save.

You will see the project screen view and Coverage Report is activated shown as below:

Now lets update the SimpleGreeting Project pom file in Git to handle report metrics.

9. Open Eclipse.

10. In the Project Explorer, navigate to the SimpleGreeting project.

11. Double-click on the file pom.xml to open it.

12. On the lower edge of the editor panel, click on pom.xml to select the XML view of the file.

 

...
<build>
<plugins>

<plugin>
<groupId>org.codehaus.mojo</groupId>
<artifactId>cobertura-maven-plugin</artifactId>
<version>2.5</version>
<configuration>
<formats>
<format>html</format>
<format>xml</format>
</formats>
</configuration>
</plugin>

<plugin>
<groupId>org.apache.maven.plugins</groupId>
<artifactId>maven-compiler-plugin</artifactId>
<version>2.3.2</version>
<configuration>
<source>1.7</source>
<target>1.7</target>
</configuration>
</plugin>
</plugins>
</build>

<reporting>
<plugins>
<plugin>
<groupId>org.codehaus.mojo</groupId>
<artifactId>cobertura-maven-plugin</artifactId>
</plugin>
</plugins>
</reporting>

</project>


14. Save and close the file.

Next you will Commit and push the changes using the procedure in the previous lab.

15. Right-click on SimpleGreeting in the Project Explorer and then select Team → Commit...

16. Enter a few words as a commit message, and click Commit and Push. Then click OK.
 
If you don't see an automatic build, click the Build Now to kick off a manual build.


18. Once the build is completed, move the mouse over the build number window and make check that it is successful:

Note, Build # may vary depending on how many times you build.

19. Now let's click on the Coverage Report.

### Conclusion

In this lab:
•	Learned how to configure a Maven build to report code coverage
•	Learned how to report and track that coverage in a Jenkins job.
