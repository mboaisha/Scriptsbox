#!/bin/bash

# Stop all containers
echo "Stopping all Docker containers..."
docker stop $(docker ps -a -q)

# Remove all containers
echo "Removing all Docker containers..."
docker rm $(docker ps -a -q)

# Remove all Docker images
echo "Removing all Docker images..."
docker rmi $(docker images -q)

# Remove all Docker volumes
echo "Removing all Docker volumes..."
docker volume rm $(docker volume ls -q)

# Remove all Docker networks (except default ones)
echo "Pruning Docker networks..."
docker network prune -f

# Clean up any residual Docker resources
echo "Cleaning up residual Docker resources..."
docker system prune -a -f

# Docker Compose specific cleanup (Optional, uncomment if needed)
# echo "Stopping and removing Docker Compose services..."
# docker-compose down -v

echo "Docker has been reset to a near-fresh installation state."
