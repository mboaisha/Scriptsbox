#!/bin/bash

# Function to check if a command exists
command_exists() {
    type "$1" &> /dev/null
}

# Check Docker installation
echo "Checking for Docker..."
if command_exists docker; then
    echo "Docker is installed."
    echo "Docker version: $(docker --version)"
else
    echo "Docker is not installed."
    exit 1
fi

# Check Docker Compose installation
echo "Checking for Docker Compose..."
if command_exists docker-compose; then
    echo "Docker Compose is installed."
    echo "Docker Compose version: $(docker-compose --version)"
else
    echo "Docker Compose is not installed."
    # Not exiting here because Docker Compose might be optional
fi

# Check for Docker containers
container_count=$(docker ps -a -q | wc -l)
if [ $container_count -eq 0 ]; then
    echo "No Docker containers found. (Good for a fresh-install state)"
else
    echo "Warning: There are $container_count Docker containers present."
fi

# Check for Docker images
image_count=$(docker images -q | wc -l)
if [ $image_count -eq 0 ]; then
    echo "No Docker images found. (Good for a fresh-install state)"
else
    echo "Warning: There are $image_count Docker images present."
fi

# Check for Docker volumes
volume_count=$(docker volume ls -q | wc -l)
if [ $volume_count -eq 0 ]; then
    echo "No Docker volumes found. (Good for a fresh-install state)"
else
    echo "Warning: There are $volume_count Docker volumes present."
fi

# Check for Docker networks
network_count=$(docker network ls -q | grep -v "bridge\|host\|none" | wc -l)
if [ $network_count -eq 0 ]; then
    echo "No custom Docker networks found. (Good for a fresh-install state)"
else
    echo "Warning: There are $network_count custom Docker networks present."
fi

echo "Docker environment check completed."
