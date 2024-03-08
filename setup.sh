#!/bin/bash

# Exit script if any command fails

set -e

# Define Docker image & Docker container name

DOCKER_IMAGE="lbg"
DOCKER_HUB="jaynecopple/"
DOCKER_CONTAINER="lbg-contain"
HOST=localhost

cleanup() {

    echo "Cleaning up previous build artifacts...removing previous containers & images"

    sleep 3

    # Add commands to clean up previous build artifacts

    docker rm -f $(docker ps -aq) || true

    docker rmi -f $(docker images) || true

    echo "Cleanup complete. Ready to continue"

}

# Function to build the Docker image

build_docker() {

    echo "Building the Docker image..."

    sleep 3

    docker build -t $DOCKER_HUB$DOCKER_IMAGE .

}

# Function to modify the application

modify_app() {

    echo "Modifying the application..."

    sleep 3

   export PORT=5001

    echo "Modifications done. Port is now set to $PORT"

}

# Function to run the Docker container

run_docker() {

    echo "Running new Docker container..."

    sleep 3

    # REPLACED docker run -d -p 80:$PORT -e PORT=$PORT --name $DOCKER_CONTAINER $DOCKER_IMAGE
    docker run -d -p 80:$PORT -e PORT=$PORT --name $DOCKER_CONTAINER $DOCKER_HUB$DOCKER_IMAGE
    

}

# Main script execution

echo "Starting build process...fingers crossed!!"

sleep 3

cleanup

build_docker

modify_app

build_docker

run_docker

echo "Build process completed successfully."

echo "Application is now available at 'http://'$HOST:$PORT"
