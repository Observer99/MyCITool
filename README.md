# This project contains MyCITool.py, Watcher.sh and dockerWebApp that contains Dockerfile and simple "Hello World" Python web application.

## MyCITool.py
This script allows the user to build docker image from local folder or directly from Git and then run it as a container.
In addtition, it creates crontab file /etc/cron.d/Watcher_<container_name> for monitoring of the container.
The crontab file launches Watcher.sh script every minute with two parameters: <container_name> and <host_port> and redirects stdout and stderr to the log file ./Watcher_<container_name>.log>

No need to run MyCITool.py script with parameters, just start it without parameters using sudo and follow the instruction (Although you can run ./MyCITool.py -h or --help in order to get help information).
The script will ask user to input all parameters interactively.
You can skip all parameters by pressing Enter. In this case the script will use default parameters.

###### Parameters:
   - path_to_docker (str): Path to Dockerfile, can be path to Git or local folder (default is "https://github.com/Observer99/MyCITool.git#master:dockerWebApp").
   - image_name (str): Name of the image to be built (default is "michaelh/my-hello").
   - container_name (str): Name of the container to be created and run (default is "my-hello-1").
   - container_port (int): Exposed TCP port of the container (default is 8080).
   - host_port (int): TCP port of the host that mapped to container_port for connection from outside (default is 4001).

## Watcher.sh
Watcher.sh performs the following checks:
   - Check container status and start it if it not running.
   - Check dockerWebApp API and restart container in case of failure.
   - Check CPU usage (<90% - INFO, 90%-95% - WARNING, >95% - ERROR).
   - Check Memory usage (<90% - INFO, 90%-95% - WARNING, >95% - ERROR).
###### message levels:
   - INFO - everything is OK.
   - WARNING - non critical issues (high CPU or Memory).
   - ERROR - critical issues (container is not running, web application is not responding, very high CPU or Memory, failure to start or restart container).
   - SUCCESS - successfull action (start or restart of container).
    
