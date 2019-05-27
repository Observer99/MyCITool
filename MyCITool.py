#!/usr/bin/env python3

import argparse

parser=argparse.ArgumentParser(
description="""Build docker image, run docker container and create monitoring as a crontab task.

This script allows the user to build docker image from local folder or directly from Git and then run it as a container.
In addtition, it creates crontab file /etc/cron.d/Watcher_<container_name> for monitoring of the container.
The crontab file launches Watcher.sh script every minute with two parameters: <container_name> and <host_port>.

No need to run MyCITool.py script with parameters, just start it without parameters using sudo and follow the instruction.
The script will ask user to input all parameters interactively.
You can skip all parameters by pressing Enter. In this case the script will use default parameters.

Parameters:
    path_to_docker (str): Path to Dockerfile, can be path to Git or local folder (default is "https://github.com/Observer99/MyCITool.git#master:dockerWebApp")
    image_name (str): Name of the image to be built (default is "michaelh/my-hello")
    container_name (str): Name of the container to be created and run (default is "my-hello-1")
    container_port (int): Exposed TCP port of the container (default is 8080)
    host_port (int): TCP port of the host that mapped to container_port for connection from outside (default is 4001)
""", formatter_class=argparse.RawTextHelpFormatter)
args=parser.parse_args()

import os
import docker


path_to_docker_default = "https://github.com/Observer99/MyCITool.git#master:dockerWebApp"
image_name_default = "michaelh/my-hello"
container_name_default = "my-hello-1"
container_port_default = 8080
host_port_default = 4001

client = docker.from_env()

#Get string parameters from user or set default values:
path_to_docker = input('{} {} \n'.format('Please insert path to Github project or local folder that contains Dockerfile or press Enter for default value\n\
DEFAULT value is', path_to_docker_default)) or path_to_docker_default
print('===>\n', 'path_to_docker set to: ', path_to_docker, '\n<===\n')

image_name = input('{} {} \n'.format('Please insert image name or press Enter for default value\n\
DEFAULT value is', image_name_default)) or image_name_default
print('===>\n', 'image_name set to: ', image_name, '\n<===\n')

container_name = input('{} {} \n'.format('Please insert container name or press Enter for default value\n\
DEFAULT value is', container_name_default)) or container_name_default
print('===>\n', 'container_name set to: ', container_name, '\n<===\n')

#Get and verify integer parameters from user or set default values:
def set_container_port():
    container_port = input('{} {} \n'.format('Please insert container port or press Enter for default value\nDEFAULT value is', container_port_default)) or container_port_default
    while True:
        try:
    	    container_port = int(container_port)
        except ValueError:
            container_port = input('Container port should be an integer! You can press Enter for default value\n') or container_port_default
            continue
        else:
            break
    return container_port

container_port = set_container_port()
print('===>\n', 'container_port set to: ', container_port, '\n<===\n')

def set_host_port():
    host_port = input('{} {} \n'.format('Please insert host port (integer) or press Enter for default value\nDEFAULT value is', host_port_default)) or host_port_default
    while True:
        try:
    	    host_port = int(host_port)
        except ValueError:
            host_port = input('Host port should be an integer! You can press Enter for default value\n') or host_port_default
            continue
        else:
            break
    return host_port

host_port = set_host_port()
print('===>\n', 'host_port set to: ', host_port, '\n<===\n')

#Build docker image:
print('Building docker image...\nIt should take only few seconds, so please be patient...')
try:
    client.images.build(path=path_to_docker, tag=image_name, rm=True)
except Exception as e:
    print('ERROR! The image was not built successfully!')
    print(e)
    exit(1)
else:
    print('SUCCESS! The docker image was built successfully!\n')

#Run container:
print('Running docker conteiner...\nIt should take about one second, so please be patient even more...')
try:
    container = client.containers.run(image_name, ports={container_port: host_port}, name=container_name, detach=True)
except Exception as e:
    print('ERROR! The container was not run successfully!')
    print(e)
    exit(1)
else:
    print('SUCCESS! The docker container was run successfully!\n')
    print('Container name: ', container.name)
    print('Container image: ', container.image)
    print('Container labels: ', container.labels)
    print('Container ID: ', container.id)
    print('Container short_id: ', container.short_id)
    print('Container status: ', container.status, '\n')

#Create a crontab file for Watcher:
print('Creating Watcher_' + container_name + ' crontab file and putting it to /etc/cron.d/')
try:
    local_path = os.path.dirname(os.path.abspath(__file__))
    watcher_filename = '{}{}'.format('Watcher_', container_name)
    watcher_filepath = '{}/{}{}'.format('/etc/cron.d', 'Watcher_', container_name)
    logfile = '{}/{}{}{}'.format(local_path, 'Watcher_', container_name, '.log')
    file = open(watcher_filepath, 'w')
    file.write('{}{}{}{} {}{}{}{}{}{}'.format('*/1 * * * * root ', local_path, '/Watcher.sh ', container_name, host_port, ' >> ', local_path, '/Watcher_', container_name, '.log 2>&1\n'))
    file.close()
except Exception as e:
    print('ERROR! Failed create Watcher!')
    print(e)
    exit(1)
else:
    print('SUCCESS! The Watcher was created successfully!\nThe Watcher samples every minute and stores the resultes it the following log file:\n', logfile, '\n')

