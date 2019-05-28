#!/bin/bash

#This script requires two parameters - <container_name> and <host_port>

echo "===================================================="
echo `date`
echo "===================================================="

#Check container status:
state=$(docker inspect -f '{{.State.Running}}' $1)
if [ $state = true ]
then
   echo "INFO: The container $1 is running"
else
   echo "ERROR: The container $1 is not running! Trying to start the container $1"
   docker start $1
   if [ $? ]
   then
      echo "SUCCESS: The container $1 was started successfully"
          sleep 5
   else
      echo "ERROR: The start of container $1 failed!"
   fi
fi

#Check dockerWebApp API:
response=$(curl --max-time 5 -s http://localhost:$2)
if [ "$response" = 'Hello world!' ]
then
   echo "INFO: The dockerWebApp is up and listening on port $2"
else
   echo "ERROR: The dockerWebApp is not working! Trying to restart container $1"
   docker restart $1
   if [ $? ]
   then
      echo "SUCCESS: The container $1 was restarted successfully"
   else
      echo "ERROR: The restart of container $1 failed!"
   fi
fi

#Check host CPU usage (not in use anymore):
#CPU_USAGE=$(sar 1 3 | grep Average | awk '{ print $8 }')

#Check container CPU usage:
CPU_USAGE=$(docker stats $1 --no-stream --format "{{.CPUPerc}}")
#Remove '%'
CPU_USAGE=$(echo $CPU_USAGE | sed s/%//)
#Convert to integer:
CPU_USAGE=$(printf %.0f "$CPU_USAGE")

if [ $CPU_USAGE -lt 90 ]
then
   echo "INFO: The CPU usage is $CPU_USAGE%"
elif [ $CPU_USAGE -lt 96 ]
then
   echo "WARNING: CPU usage is $CPU_USAGE%"
else
   echo "ERROR: CPU usage is $CPU_USAGE%"
fi

#Check host Memory usage (not in use anymore):
#TOTAL_MEMORY=$(free -m | awk 'NR==2{printf "%s\n", $2 }')
#AVAILABLE_MEMORY=$(free -m | awk 'NR==2{printf "%s\n", $7 }')
#MEMORY_USAGE=$(((TOTAL_MEMORY - AVAILABLE_MEMORY) *100 / TOTAL_MEMORY))

#Check container Memory usage:
MEMORY_USAGE=$(docker stats $1 --no-stream --format "{{.MemPerc}}")
#Remove '%'
MEMORY_USAGE=$(echo $MEMORY_USAGE | sed s/%//)
#Convert to integer:
MEMORY_USAGE=$(printf %.0f "$MEMORY_USAGE")

if [ $MEMORY_USAGE -lt 90 ]
then
   echo "INFO: The Memory usage is $MEMORY_USAGE%"
elif [ $MEMORY_USAGE -lt 96 ]
then
   echo "WARNING: Memory usage is $MEMORY_USAGE%"
else
   echo "ERROR: Memory usage is $MEMORY_USAGE%"
fi

echo ""

