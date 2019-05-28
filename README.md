### MyCITool.py builds docker image from Git (default is dockerWebApp), runs container and configures Watcher.sh


### Usage
Clone this project to your host. Actually you need only MyCITool.py and Watcher.sh available in your working directory. The dockerWebApp will be downloaded and built automatically by MyCITool.py script.

### MyCITool.py
This script allows the user to build docker image from local folder or directly from Git and then run it as a container.
In addtition, it creates crontab file /etc/cron.d/Watcher_<container_name> for monitoring of the container.
The crontab file launches Watcher.sh script every minute with two parameters: <container_name> and <host_port> and redirects stdout and stderr to the log file ./Watcher_<container_name>.log>

No need to run MyCITool.py script with parameters, just start it without parameters using sudo and follow the instruction (Although you can run ./MyCITool.py -h or --help in order to get help information).
The script will ask user to input all parameters interactively.
You can skip all parameters by pressing Enter. In this case the script will use default parameters.

##### Parameters
   - path_to_docker (str): Path to Dockerfile, can be path to Git or local folder (default is "https://github.com/Observer99/MyCITool.git#master:dockerWebApp").
   - image_name (str): Name of the image to be built (default is "michaelh/my-hello").
   - container_name (str): Name of the container to be created and run (default is "my-hello-1").
   - container_port (int): Exposed TCP port of the container (default is 8080).
   - host_port (int): TCP port of the host that mapped to container_port for connection from outside (default is 4001).

### Watcher.sh
Watcher.sh performs the following checks:
   - Check container status and start if it is not running.
   - Check dockerWebApp API and restart container in case of failure.
   - Check CPU usage (<90% - INFO, 90%-95% - WARNING, >95% - ERROR).
   - Check Memory usage (<90% - INFO, 90%-95% - WARNING, >95% - ERROR).
##### Message levels
   - INFO - everything is OK.
   - WARNING - non critical issues (high CPU or Memory).
   - ERROR - critical issues (container is not running, web application is not responding, very high CPU or Memory, failure to start or restart container).
   - SUCCESS - successfull action (start or restart of container).

### dockerWebApp
The dockerWebApp is a simple "Hello World" Python web application with Dockerfile.

### Requirements
The following components should be available in order to run MyCITool.py:
   - Python 3 with docker module installed (pip install docker)
   - Docker deamon running
   - Git client
   - sar command (part of sysstat package). Sar command is used by Watcher.sh

This solution was tested on CentOS 7 and Ubuntu 18.04, but should work on other distributions as well.
