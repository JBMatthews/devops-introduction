## Create a Jenkins Job

In this lab you will create and build a job in Jenkins. Jenkins supports several different types of build jobs. The two most commonly-used are the freestyle builds and the Maven 2/3 builds. The freestyle projects allow you to configure just about any sort of build job, they are highly flexible and very configurable. The Maven 2/3 builds understand the Maven project structure, and can use this to let you set up Maven build jobs with less effort and a few extra features.

At the end of this lab you will be able to:
1. Create a Jenkins Job that accesses a Git repository.

----

### Part 1 Enable Jenkins' Maven Plugin

1. Go to the Jenkins console:

	http://localhost:8080

2. Click on the Manage Jenkins link

	![image001](https://user-images.githubusercontent.com/558905/37422348-76c919a4-2791-11e8-9942-cce124055f09.jpg)

3. Click on Manage Plugins

	![image003](https://user-images.githubusercontent.com/558905/37422350-76f67fa2-2791-11e8-9f96-2b2825fe4027.png)

4. Click on the Available tab.

	![image005](https://user-images.githubusercontent.com/558905/37422352-77182b7a-2791-11e8-944e-4201b9d653c7.png)

5. In the filter box at the top-right of the window, enter 'maven'. Note: Don't hit Return!

	![image007](https://user-images.githubusercontent.com/558905/37422355-773eabf6-2791-11e8-8b00-877a95a9e53b.png)

6. Entering the filter text will narrow down the available plugins a little. Scroll down to find the 'Maven Integration Plugin' listing, and click on the checkbox next to it.

	![image009](https://user-images.githubusercontent.com/558905/37422357-775b69b2-2791-11e8-92ce-d019d2d9523a.png)

7. Click on Install Without Restart.

	![image011](https://user-images.githubusercontent.com/558905/37422359-777bc964-2791-11e8-9d05-6eba7d4acc12.png)

8. Click on Go back to the top page.

	![image013](https://user-images.githubusercontent.com/558905/37422361-779acbac-2791-11e8-8825-a33ca87c01e9.png)

### Part 2 - Create a Git Repository

As a distributed version control system, Git works by moving changes between different repositories. Any repository apart from the one you're currently working in is called a "remote" repository. Git doesn't differentiate between remote repositories that reside on different machines and remote repositories on the same machine. They're all remote repositories as far as Git is concerned. In this lab, we're going to start from a source tree, create a local repository in the source tree, and then clone it to a local repository. Then we'll create a Jenkins job that pulls the source files from that remote repository. Finally, we'll make some changes to the original files, commit them and push them to the repository, showing that Jenkins automatically picks up the changes.
 
2. Right click in the empty area and select Git Bash Here. The Git command prompt will open.

	![image015](https://user-images.githubusercontent.com/558905/37422363-77b63ec8-2791-11e8-866f-7984ad0c658f.png)

3. Enter the following command:

	```console
	ls
	```

	![image017](https://user-images.githubusercontent.com/558905/37422365-77ded9b4-2791-11e8-8ea9-737c75c92fe1.png)

	```console
	git config --global user.email "admin@engage.com" git config --global user.name "Bob Smith"
	```

	The lines above are actually part of the initial configuration of Git. Because of Git's distributed nature, the user's identity is included with every commit as part of the commit data. So we have to tell Git who we are before we'll be able to commit any code.

5. Enter the following lines to actually create the Git repository:

	```console
	git init git add .
	git commit -m "Initial Commit"
	```
	
	The above lines create a git repository in the current directory (which will be C:\LabFiles\Create a Jenkins Job\SimpleGreeting), add all the files to the current commit set (or 'index' in git parlance), then actually performs the commit.

6. Enter the following, to create a folder called repos under the C:\Software folder.

	```console
	mkdir /c/Software/repos
	```
	
7. Enter the following to clone the current Git repository into a new remote repository.

	```console
	git clone --bar . /c/Software/repos/SimpleGreeting.git
	```
	
	![image019](https://user-images.githubusercontent.com/558905/37422368-77fbcce0-2791-11e8-8ce7-a5f433cc769e.png)

	> Note C:\Software\repos\SimpleGreeting.git. Jenkins will be quite happy to pull the source files for a job from this repo.

### Part 3  Create the Jenkins Job

1. Go to the Jenkins console:

	```console
	http://localhost:8080
	```
	
2. Click on the New Item link.

	![image021](https://user-images.githubusercontent.com/558905/37422371-78187f48-2791-11e8-964d-1fc87349a14b.jpg)

3. Enter SimpleGreeting for the project name.

4. Select Maven Project as the project type.

	![image023](https://user-images.githubusercontent.com/558905/37422373-78430e5c-2791-11e8-8520-049501cf5a5a.png)

5. Click OK, to add a new job.

	After the job is created, you will be on the job configuration page.
	
	![image025](https://user-images.githubusercontent.com/558905/37422377-78677792-2791-11e8-8471-635510efbe8a.png)

7. Under Repositories, enter C:\Software\repos\SimpleGreeting.git

8. Click the Tab key in your keyboard.

	![image027](https://user-images.githubusercontent.com/558905/37422379-7882bb88-2791-11e8-8180-047dd12f098e.png)

9. Click Save.

10. You will see the Job screen. Click Workspace.

	![image029](https://user-images.githubusercontent.com/558905/37422381-78a3a884-2791-11e8-8a5f-f6e047581073.png)

	![image031](https://user-images.githubusercontent.com/558905/37422383-78c4959e-2791-11e8-98da-38616443c888.jpg)

	You should see the build in progress in the Build History area.

	![image033](https://user-images.githubusercontent.com/558905/37422385-78e91dba-2791-11e8-9c68-348f4a86ef4c.png)

12. After a few seconds the build will complete, the progress bar will stop. Click on Workspace.

	![image035](https://user-images.githubusercontent.com/558905/37422387-790adb9e-2791-11e8-95a3-ba480c04ba3a.jpg)

	![image037](https://user-images.githubusercontent.com/558905/37422389-792d96a2-2791-11e8-8027-db9bf3616c6f.png)

13. Find the Build History box, and click on the 'time' value for the most recent build. You should see that the build was successful.

	![image039](https://user-images.githubusercontent.com/558905/37422391-794e412c-2791-11e8-81b0-ff7661038398.png)

14. Click the Console Output from the left menu.

	![image041](https://user-images.githubusercontent.com/558905/37422394-799da9a6-2791-11e8-8548-37f4b9a7eeaa.png)

15. At the end of the console you will also see the build success and successful build:

	![image043](https://user-images.githubusercontent.com/558905/37422396-79bf0650-2791-11e8-9b2b-838f7220770b.png)

	You have created a project and built it successfully.

### Part 4 Enable Polling on the Repository

So far, we have created a Jenkins job that pulls a fresh copy of the source tree prior to building. But we triggered the build manually. In most cases, we would like to have the build triggered automatically whenever a developer makes changes to the source code in the version control system.

1. In the Jenkins web application, navigate to the SimpleGreeting project. You can probably find the project in the breadcrumb trail near the top of the window. Alternately, go to the Jenkins home page and then click on the project.

2. Click the Configure link.

3. Scroll down to find the Build Triggers section.

	![image045](https://user-images.githubusercontent.com/558905/37422398-79e04f2c-2791-11e8-9976-96e74afd3182.jpg)

4. Click on the checkbox next to Poll SCM, and then enter '* * * * *' into the Schedule text box. [Make sure there is an space between each *]

	> Note: The above schedule sets up a poll every minute. In a production scenario, that's a higher frequency than we need, and it can cause unnecessary load on the repository server and on the Jenkins server. You'll probably want to use a more reasonable schedule - perhaps every 15 minutes. That would be 'H/15 * * * *' in the schedule box.

5. Click Save.

### Part 5 Import the Project into Eclipse

In order to make changes to the source code, we'll clone a copy of the Git repository into an Eclipse project.

1. Start Eclipse by running C:\Software\eclipse\eclipse.exe and use C:\Workspace as Workspace.

2. Close the Welcome page.

3. From the main menu, select File → Import...

4. Select Git → Projects from Git.

	![image049](https://user-images.githubusercontent.com/558905/37422402-7a28ab8c-2791-11e8-8518-480d902da1cf.png)

5. Click Next.

6. Select Clone URI and then click Next.

	![image051](https://user-images.githubusercontent.com/558905/37422404-7a4815f8-2791-11e8-8f27-071478d7dae3.png)

	You might think that 'Existing local repository' would be the right choice, since we're cloning from a folder on the same machine. Eclipse, however, expects a "local repository" to be a working directory, not a bare repository. On the other hand, Jenkins will complain if we try to get source code from a repository with a working copy. So the correct thing is to have Jenkins pull from a bare repository, and use Clone URI to have Eclipse import the project from the bare repository.

7. Click on Local File... and then navigate to C:\Software\repos\SimpleGreeting.git

	![image053](https://user-images.githubusercontent.com/558905/37422406-7a6b0d2e-2791-11e8-9999-130285290c14.png)

8. Click OK.

9. Back in the Import Projects dialog, click Next.

	![image055](https://user-images.githubusercontent.com/558905/37422408-7a85f210-2791-11e8-9bc3-620a1565408d.png)

10. Click Next to accept the default 'master' branch.

	![image057](https://user-images.githubusercontent.com/558905/37422410-7aa6dcb4-2791-11e8-8e23-bb15ca120209.png)

	![image059](https://user-images.githubusercontent.com/558905/37422413-7ac655b2-2791-11e8-926e-a48c170ee25f.png)

12. Select Import as a General Project and click Next.

	![image061](https://user-images.githubusercontent.com/558905/37422415-7ae3e654-2791-11e8-87ba-984bfa25ca39.png)

13. Click Finish.

	![image063](https://user-images.githubusercontent.com/558905/37422417-7b04f07e-2791-11e8-8550-ba291f4c0bb7.png)

	At this point, we could go ahead and edit the files, but Eclipse doesn't understand the project's layout. Let's tell Eclipse what we know - that this project is built using Apache Maven.

	![image065](https://user-images.githubusercontent.com/558905/37422419-7b232df0-2791-11e8-95b2-4dfc1389aaef.png)

15. Right-click on the SimpleGreeting project in the Project Explorer, and then select Configure → Convert to Maven Project.

	![image067](https://user-images.githubusercontent.com/558905/37422421-7b4cc44e-2791-11e8-81ef-c4256695bfbf.png)

16. After few seconds, you should now see the project represented as a Maven project in the Project Explorer.

	![image069](https://user-images.githubusercontent.com/558905/37422423-7b772d56-2791-11e8-8710-db8eab6d7494.png)

### Part 6 Make Changes and Trigger a Build

The project that we used as a sample consists of a basic "Hello World" style application, and a unit test for that application. In this section, we'll alter the core application so it fails the test, and then we'll see how that failure appears in Jenkins.

1. In the Project Explorer, expand the src/main/java tree node.

	![image071](https://user-images.githubusercontent.com/558905/37422425-7b9e442c-2791-11e8-9c42-0ad13120e066.png)

3. Double-click on Greeting.java to open the file.

	![image073](https://user-images.githubusercontent.com/558905/37422427-7bc09b4e-2791-11e8-8f65-87cf348ef269.png)

4. Find the line that says 'return "GOOD";'. Edit the line to read 'return "BAD";'

	![image075](https://user-images.githubusercontent.com/558905/37422429-7be37d26-2791-11e8-9118-0896495d2b4a.png)

5. Save the file by pressing Ctrl-S or selecting File → Save.

	Now we've edited the local file. The way Git works is that we'll first 'commit' the file to the local workspace repository, and then we'll 'push' the changes to the upstream repository. That's the same repository that Jenkins is reading from. Eclipse has a short- cut button that will commit and push at the same time.

6. Right-click on SimpleGreeting in the Project Explorer and then select Team → Commit...

7. Enter a few words as a commit message, and then click Commit and Push.

	![image077](https://user-images.githubusercontent.com/558905/37422433-7c046388-2791-11e8-8ef9-d99ef24a1281.jpg)

9. Now, flip back to the web browser window that we had Jenkins running in. If you happen to have closed it, open a new browser window and navigate to http://localhost:8080/SimpleGreeting. After a few seconds, you should see a new build start up.

	![image079](https://user-images.githubusercontent.com/558905/37422437-7c25521e-2791-11e8-9a40-595aa7547f5c.png)

10. If you refresh the page, you should see that there is now a 'Test Result Trend' graph that shows we have a new test failure.

	![image081](https://user-images.githubusercontent.com/558905/37422441-7c76f09c-2791-11e8-872b-779cdeccde6a.png)

What happened is that we pushed the source code change to the Git repository that Jenkins is reading from. Jenkins is continually polling the repository to look for changes. When it saw that a new commit had been performed, Jenkins checked out a fresh copy of the source code and performed a build. Since Maven automatically runs the unit tests as part of a build, the unit test was run. It failed, and the failure results were logged.

### Part 7 Fix the Unit Test Failure

1. Back in eclipse , edit the file Greeting.java so that the class once again returns 'GOOD'.

	![image083](https://user-images.githubusercontent.com/558905/37422443-7ca46748-2791-11e8-972b-4352309bc14b.png)

2. As above, save, commit and push the change. Build start automatically, when the build is done then refresh the page:

	![image085](https://user-images.githubusercontent.com/558905/37422445-7cc69d36-2791-11e8-8ff9-f4890dcc6213.jpg)

### Conclusion

In this lab you learned
•	How to Set-up a set of distributed Git repositories
•	How to create a Jenkins Job that reads from a Git repository
•	How to configure Jenkins to build automatically on source code changes.
