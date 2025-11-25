#!/bin/bash

# Docker Deployment Script for AWS EC2
# Builds and runs the application in Docker containers

set -e

echo "=========================================="
echo "Docker Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please run: curl -fsSL https://get.docker.com | sh"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Please install Docker Compose first"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Build Docker image
echo -e "\n${YELLOW}📦 Building Docker image...${NC}"
docker build -t attendance-system:latest .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build Docker image${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update .env with your configuration${NC}"
fi

# Start containers with Docker Compose
echo -e "\n${YELLOW}🚀 Starting containers with Docker Compose...${NC}"
docker-compose up -d

# Wait for service to be ready
echo -e "${YELLOW}⏳ Waiting for service to be ready...${NC}"
sleep 10

# Check if container is running
if docker ps | grep -q "attendance-app"; then
    echo -e "${GREEN}✅ Application container is running${NC}"
else
    echo -e "${RED}❌ Application container failed to start${NC}"
    docker-compose logs web
    exit 1
fi

if docker ps | grep -q "attendance-db"; then
    echo -e "${GREEN}✅ Database container is running${NC}"
else
    echo -e "${YELLOW}⚠️  Database container is not running${NC}"
fi

echo -e "\n=========================================="
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo -e "=========================================="
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. Access the application:"
echo "   http://YOUR_EC2_PUBLIC_IP:8501"
echo ""
echo "2. View running containers:"
echo "   docker ps"
echo ""
echo "3. View logs:"
echo "   docker-compose logs -f web"
echo ""
echo "4. Stop the application:"
echo "   docker-compose down"
echo ""
echo "5. Restart the application:"
echo "   docker-compose restart"
echo ""
echo -e "=========================================="
