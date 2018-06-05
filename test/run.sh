#!/bin/bash
################################################################################
# Docker Helper Script                                                         #
# -------------------------                                                    #
# This is an all purpose script which would allow you to do the following -    #
# 1) Create a clone of callerid_test repo                                      #
# 2) Build a Docker Image                                                      #
# 3) Spin a Docker Container                                                   #
# 4) Execute Test inside Container                                             #
################################################################################

echo "-----------------------------------"
echo "| Welcome to Docker Helper Script |"
echo "-----------------------------------"

# Check if user has docker and git
echo "This script assumes you have Git and Docker installed on your system!"
echo "If you wish to install Git and Docker, use these commands - "
echo ""
echo "-------------------------------------------------------------------------"
echo "For Git (Ubuntu) - sudo apt-get install git"
echo "For Git (RHEL and Flavors) - sudo yum install git"
echo "-------------------------------------------------------------------------"
echo ""
echo "-------------------------------------------------------------------------"
echo "For Docker (Ubuntu) - sudo apt-get install docker-ce"
echo "For Docker (RHEL and Flavors) - sudo yum install docker-ce"
echo "-------------------------------------------------------------------------"

# Should you proceed with the script
while true; do
    echo "Do you wish to proceed?"
    read -p "Enter (y/n) - " yn
    case "$yn" in
        [Yy]* )
            break ;;
        [Nn]* )
            return ;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Local Repo Directory
repodir=/tmp/callerid_test

# Find current directory
cwd="$pwd"

# User wants to create a local repo clone
while true; do
    echo "Do you wish to create a local repository?"
    read -p "Enter (y/n) - " yn
    case "$yn" in
        [Yy]* )
            echo "Where do you wish to create a local repository? [Example - /tmp/callerid_test]"
            echo "Ensure you have permissions rightfully set as the script will NOT change permissions!"
            read -p "Repository : " repodir
            mkdir -p "$repodir"
            git clone https://github.com/mokbat/callerid_test.git "$repodir"
            repodir="$repodir"
            break;;
        [Nn]* )
            echo "Assuming you already have a local repo. [Example /tmp/callerid_test]"
            echo "If you wish to manually clone - "
            echo "git clone https://github.com/mokbat/callerid_test.git <base_directory>"
            echo "Please provide your local repository path?"
            read -p "Repo Path : " repodir
            break;;
        * ) echo "Please answer yes or no.";;
    esac
done
echo "-----------------------------------------------------------------------------------------"
echo "Your local repository can be accessed at - $repodir"
echo "-----------------------------------------------------------------------------------------"

# Check if the user wishes to build the container
echo "Do you wish to build the Caller ID App?"
read -p "Enter (y/n) - " yn
case "$yn" in
    [Yy]* )
        # Build the image
        echo "-----------------------------------------------------------------------------------------"
        echo "Building Docker Container with Tag Name - app"
        echo "-----------------------------------------------------------------------------------------"
        cd $repodir/callerid
        # Push the current host information
        host_ip="127.0.0.1"
        host_port="9090"
        docker build -t "app" .
        docker run -p 127.0.0.1:9090:8080 -d -t "app"
        cd ..
        echo "" ;;
    [Nn]* )
        echo "Please build and run your docker image manually!"
        echo "-----------------------------------------------------------------------------------------"
        echo "Example command - docker build -t app ."
        echo "Example command - docker run -p 9090:8080 -dt app"
        echo "-----------------------------------------------------------------------------------------"
        echo "" ;;
    * ) echo "Please answer yes or no.";;
esac


# Docker Image Details
while true; do

    # Get to the right  directory
    echo "Getting into $repodir/test"
    cd $repodir/test || echo "Unable to change directory to $repodir/test"

    echo "# Mention the host ip and port on which caller_id app is running" >> $repodir/Dockerfile
    echo "ENV HOST_IP=$host_ip" >> $repodir/test/Dockerfile
    echo "ENV HOST_PORT=$host_port" >> $repodir/test/Dockerfile

    # Tag for the name of the image
    TAG="$(date +%m_%d_%Y):$(git log -n 1 origin/master --format="%h")"
    echo "TAG has been set with value $TAG"

    # Check if the user wishes to build the container
    echo "Do you wish to build a docker image for rest api testing?"
    read -p "Enter (y/n) - " yn
    case "$yn" in
        [Yy]* )
            # Build the image
            echo "-----------------------------------------------------------------------------------------"
            echo "Building Docker Container with Tag Name - $TAG"
            echo "-----------------------------------------------------------------------------------------"
            docker build -t "$TAG" .
            break ;;
        [Nn]* )
            echo "Please build your docker image manually!"
            echo "-----------------------------------------------------------------------------------------"
            echo "Example command - docker build -t $TAG ."
            echo "-----------------------------------------------------------------------------------------"
            break ;;
        * ) echo "Please answer yes or no.";;
    esac
done

# User wants to access the container and run functional test
while true; do
    echo "Do you wish to run functional test or load test?"
    read -p "Enter (F/L) - " test_type
    case "$test_type" in
        [Ff]* )
            echo "Functional Test is selected!"
            functional="True"
            load="False"
            echo ""
            break ;;
        [Ll]* )
            echo "Load Test is selected!"
            functional="False"
            load="True"
            echo ""
            break ;;
        * ) echo "Please answer F/f for functional test or L/l for load test.";;
    esac
done

# User wants to access the container and run functional test
while $functional; do
    echo "Do you wish to access the container and run functional test?"
    read -p "Enter (y/n) - " access
    case "$access" in
        [Yy]* )
            echo "Using the current image built!"
            echo "-----------------------------------------------------------------------------------------"
            echo "Redirecting output to your container"
            echo "-----------------------------------------------------------------------------------------"
            echo ""
            docker run -t "$TAG" python3 test_functional.py
            echo ""
            break ;;
        [Nn]* )
            break ;;
        * ) echo "Please answer yes or no.";;
    esac
done

# User wants to access the container and run load test
while $load; do
    echo "Do you wish to access the container and run load test?"
    read -p "Enter (y/n) - " access
    case "$access" in
        [Yy]* )
            echo "Using the current image built!"
            echo "-----------------------------------------------------------------------------------------"
            echo "Redirecting output to your container"
            echo "-----------------------------------------------------------------------------------------"
            echo ""
            docker run -t "$TAG" locust --host=http://localhost:8089 -f test_load.py
            echo "Use the web browser - http://localhost:8089                                             "
            echo "Start the test by specifying number of users to simulate and users/sec                  "
            echo ""
            break ;;
        [Nn]* )
            break ;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Back to the same directory
cd "$cwd" || echo "Unable to bring you back to the working directory $cwd"

echo "========================================================================================"
echo "                                   Summary                                              "
echo "========================================================================================"
echo "                                                                                        "
echo "----------------------------------------------------------------------------------------"
echo "Your local clone is located at - $repodir                                               "
echo "----------------------------------------------------------------------------------------"
echo "Docker Tag - $TAG                                                                       "
echo "----------------------------------------------------------------------------------------"
echo "                                                                                        "
echo "For access to the test, use this command below                                          "
echo "----------------------------------------------------------------------------------------"
echo "Functional Test                                                                         "
echo "----------------------------------------------------------------------------------------"
echo "docker run -t $TAG python3 test_functional.py                                           "
echo "----------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------------------------------"
echo "Load Test                                                                               "
echo "----------------------------------------------------------------------------------------"
echo "docker run -t $TAG locust --host=http://localhost:8089 -f test_load.py                  "
echo "Use the web browser - http://localhost:8089                                             "
echo "Start the test by specifying number of users to simulate and users/sec                  "
echo "----------------------------------------------------------------------------------------"
echo "                                                                                        "
echo "Thank you for using  Helper Function!                                                   "
echo "========================================================================================"
