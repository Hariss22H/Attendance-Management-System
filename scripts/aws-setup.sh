#!/bin/bash

# AWS EC2 Setup Script for Attendance Management System
# This script installs all dependencies and sets up the application

set -e  # Exit on error

echo "=========================================="
echo "Face Recognition Attendance System"
echo "AWS EC2 Setup Script"
echo "=========================================="

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
echo "🐍 Installing Python and pip..."
sudo apt-get install -y \
    python3.9 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    nano \
    htop

# Install OpenCV dependencies
echo "📷 Installing OpenCV dependencies..."
sudo apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    build-essential

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
echo "🐳 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository (if not already cloned)
echo "📂 Cloning repository..."
if [ ! -d "Attendance-Management-System" ]; then
    git clone https://github.com/Hariss22H/Attendance-Management-System.git
fi

cd Attendance-Management-System

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install streamlit

# Create necessary directories
echo "📁 Creating application directories..."
mkdir -p TrainingImage
mkdir -p TrainingImageLabel
mkdir -p StudentDetails
mkdir -p Attendance
mkdir -p /var/log/attendance-app

# Set permissions
sudo chown -R ubuntu:ubuntu /var/log/attendance-app

# Create .env file from example
echo "⚙️  Creating .env configuration file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
    echo "   nano .env"
fi

# Create systemd service file for Streamlit
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/attendance.service > /dev/null <<EOF
[Unit]
Description=Face Recognition Attendance System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Attendance-Management-System
Environment="PATH=/home/ubuntu/Attendance-Management-System/venv/bin"
ExecStart=/home/ubuntu/Attendance-Management-System/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Create Nginx reverse proxy (optional)
echo "🌐 Installing Nginx..."
sudo apt-get install -y nginx

# Create Nginx config
sudo tee /etc/nginx/sites-available/attendance-system > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx config
sudo ln -sf /etc/nginx/sites-available/attendance-system /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
sudo nginx -t

# Start services
echo "🚀 Starting services..."
sudo systemctl start nginx
sudo systemctl enable nginx

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📝 Next Steps:"
echo "1. Edit configuration: nano .env"
echo "2. Start the application:"
echo "   Option A (Systemd): sudo systemctl start attendance"
echo "   Option B (Direct):  streamlit run app.py"
echo "   Option C (Docker):  docker-compose up -d"
echo ""
echo "3. Access the application:"
echo "   http://YOUR_EC2_PUBLIC_IP"
echo ""
echo "4. Check service status:"
echo "   sudo systemctl status attendance"
echo ""
echo "5. View logs:"
echo "   sudo journalctl -u attendance -f"
echo ""
echo "=========================================="
