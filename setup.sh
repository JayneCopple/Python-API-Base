#!/bin/bash

# Exit script if any command fails
set -e

# Define Docker image, image version & Docker container name
export DOCKER_IMAGE=lbg
export IMAGE_VERSION=1.0
export DOCKER_CONTAINER=lbg-contain
export DOCKER_HUB=""
# export DOCKER_HUB="jaynecopple/"

# Define port variable
export PORT=5001

# Function to run to clean up ALL images & containers first
cleanup() {
    echo "Cleaning up previous build artifacts...removing previous containers & images"
    sleep 3

    # Add commands to clean up previous build artifacts - stop continers, remove containers, remove images
    docker stop $(docker ps -q) || true
    docker rm $(docker ps -aq) || true
    docker rmi $(docker images) || true

    echo "Cleanup complete. Ready to continue"
}

# Function to build the Docker image
build_docker() {
    echo "Building the Docker image..."
    sleep 3

    docker build -t $DOCKER_HUB$DOCKER_IMAGE:$IMAGE_VERSION --build-arg PORT=$PORT .
}

# Function to run the Docker container
run_docker() {
    echo "Running new Docker container..."
    sleep 3

    # REPLACED docker run -d -p 80:$PORT -e PORT=$PORT --name $DOCKER_CONTAINER $DOCKER_IMAGE
    docker run -d -p 80:$PORT -e PORT=$PORT --name $DOCKER_CONTAINER $DOCKER_HUB$DOCKER_IMAGE:$IMAGE_VERSION
}

# Main script execution - run each of the functions already defined

echo "Starting build process...fingers crossed!!"

sleep 3
cleanup
build_docker
run_docker

echo "Build process completed successfully."
echo "Application is now available from container"
