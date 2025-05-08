I wrote django application with 5 apis 3 of them is for authenticating and registering.(ignore get-ip and token/refresh )
swagger is not implemented instead I explain my apis here
	
Start-stop/:

Delete: deletes the question for the loggined user(authorization header must have the    token)
{“problem”:problem_number}
Response may have 400 or 200 status.if there was any errors it will return something like 
{“errors”:”error description”}
Post:
Creates the question for the loggined user(authorization header must have the token)
Request body:{“problem”:problem_number}
Response may have 400 or 200 status . if there was any errors it will return something like 
{“errors”:”error description”}
If everything goes as expected it will return something like 
{“address”:some-ip(or domain):port}


Register/ and token/:  
Request body for both:
{“username”:someusername,”password”:somepass}
They both return access and refresh token
{“access”:wededewdewdedewd,”refresh”:wdewdewdewdewdew}
In case of success register will return status code of 201 (CREATED) but token will return 200(OKAY)

Database schema:
cloud_team is an AbstractUser means that it has everything that a normal user would have.
Like username and password and email.

cloud_problem(name,number,description,image_name,port)
Name and number and description are obvious.
Image_name specifies the name of the image used for this problem.  You can create two problems with the image name mentioned in the homework document.
Port specifies the port in the container that the image uses and should be bound to the outside port on the host.
cloud_teamproblem(	team,problem,up,ip,port,container_id)
This table implements a many to many relationship betwean team and problem.
Team and problem are foreign keys.
Up is a boolean showing the status of the question container.
Ip is useless because I distinguish containers by their ports.
Port shows the port on host to access the container.
Container_id is what the name implies. It is used to stop that container if needed.


Setting up the application is rather easy .just look at .env files and configure them as you desire then just write docker compose up –build and hit enter.


