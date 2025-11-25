# AWS EC2 Deployment Guide for Attendance Management System

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Create AWS Account](#step-1-create-aws-account)
3. [Step 2: Launch EC2 Instance](#step-2-launch-ec2-instance)
4. [Step 3: Configure Security Group](#step-3-configure-security-group)
5. [Step 4: Connect to Instance](#step-4-connect-to-instance)
6. [Step 5: Deploy Application](#step-5-deploy-application)
7. [Step 6: Access Application](#step-6-access-application)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:
- AWS account (https://aws.amazon.com/)
- SSH client (built-in on Linux/Mac, PuTTY on Windows)
- Git installed locally
- Code editor (VS Code, etc.)

---

## Step 1: Create AWS Account

1. Go to https://aws.amazon.com/
2. Click **"Create an AWS Account"**
3. Fill in your email, password, and account name
4. Complete the verification process
5. Add billing information
6. Wait for account activation (usually instant)

---

## Step 2: Launch EC2 Instance

### 2.1 Open AWS Console

1. Log in to AWS Console: https://console.aws.amazon.com/
2. Search for "EC2" in the search bar
3. Click on **EC2** service
4. Click **"Instances"** in the left sidebar
5. Click **"Launch Instances"** button

### 2.2 Choose AMI (Machine Image)

- Search for: **Ubuntu Server 22.04 LTS**
- Click **"Select"**

### 2.3 Choose Instance Type

- **Free Tier**: `t2.micro` (1 GB RAM, limited performance)
- **Recommended**: `t3.medium` (4 GB RAM, better performance) - ~$30-35/month
- Click **"Next: Configure Instance Details"**

### 2.4 Configure Instance

- **Number of instances**: 1
- **Network**: Default VPC
- **Auto-assign Public IP**: Enable
- Click **"Next: Add Storage"**

### 2.5 Add Storage

- **Size**: 30 GB (Free tier includes 30 GB)
- **Volume Type**: General Purpose (gp3)
- Click **"Next: Add Tags"**

### 2.6 Add Tags

- **Key**: Name
- **Value**: Attendance-System
- Click **"Next: Configure Security Group"**

---

## Step 3: Configure Security Group

### Create New Security Group

1. **Security group name**: attendance-system-sg
2. **Description**: Security group for attendance system

### Add Inbound Rules

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | Your IP (0.0.0.0/0 for anywhere) |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |
| Custom TCP | TCP | 8501 | 0.0.0.0/0 |
| Custom TCP | TCP | 5432 | 0.0.0.0/0 (or restrict to your VPC) |

3. Click **"Review and Launch"**

---

## Step 4: Create Key Pair

1. Click **"Create a new key pair"**
2. **Key pair name**: attendance-key
3. **Key pair type**: RSA
4. Click **"Create key pair"**
5. **DOWNLOAD THE .PEM FILE** - Save it safely!

### Set Key Permissions (Windows)

```powershell
# Change to directory with .pem file
cd "C:\path\to\your\key"

# Set permissions
icacls attendance-key.pem /grant:r "$($env:USERNAME):(F)"
icacls attendance-key.pem /inheritance:r
```

### Set Key Permissions (Linux/Mac)

```bash
chmod 400 attendance-key.pem
```

---

## Step 5: Launch & Connect

### 5.1 Get Your Public IP

1. Go to **EC2 Dashboard → Instances**
2. Find your instance
3. Copy the **Public IPv4 address**

### 5.2 Connect via SSH (Windows PowerShell)

```powershell
# Navigate to key directory
cd "C:\path\to\your\key"

# Connect
ssh -i attendance-key.pem ubuntu@YOUR_PUBLIC_IP

# Example: ssh -i attendance-key.pem ubuntu@54.123.45.67
```

### 5.2 Connect via SSH (Linux/Mac)

```bash
ssh -i ~/path/to/attendance-key.pem ubuntu@YOUR_PUBLIC_IP
```

---

## Step 5: Deploy Application

### Option A: Automated Setup (Recommended)

Once connected to your EC2 instance:

```bash
# Clone the repository
git clone https://github.com/Hariss22H/Attendance-Management-System.git
cd Attendance-Management-System

# Make setup script executable
chmod +x scripts/aws-setup.sh

# Run the setup script
./scripts/aws-setup.sh

# Edit configuration
nano .env

# Start the application
sudo systemctl start attendance
sudo systemctl enable attendance
```

### Option B: Docker Deployment (Even Simpler)

```bash
# Clone the repository
git clone https://github.com/Hariss22H/Attendance-Management-System.git
cd Attendance-Management-System

# Make deploy script executable
chmod +x scripts/docker-deploy.sh

# Run Docker deployment
./scripts/docker-deploy.sh
```

### Option C: Manual Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.9 python3-pip python3-venv git -y

# Install OpenCV dependencies
sudo apt install libsm6 libxext6 libxrender-dev libgl1-mesa-glx -y

# Clone repository
git clone https://github.com/Hariss22H/Attendance-Management-System.git
cd Attendance-Management-System

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install streamlit

# Create necessary directories
mkdir -p TrainingImage TrainingImageLabel StudentDetails Attendance

# Run application
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## Step 6: Access Application

### 6.1 Get Your IP Address

In your EC2 instance terminal:
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

Or from AWS Console → Instances → Copy Public IPv4 address

### 6.2 Open in Browser

```
http://YOUR_EC2_PUBLIC_IP:8501
```

Example:
```
http://54.123.45.67:8501
```

---

## 📊 Monitoring & Maintenance

### Check Service Status

```bash
# Check if service is running
sudo systemctl status attendance

# View recent logs
sudo journalctl -u attendance -n 50

# Continuous logs
sudo journalctl -u attendance -f
```

### Docker Monitoring

```bash
# List running containers
docker ps

# View logs
docker-compose logs -f web

# Restart containers
docker-compose restart

# Stop containers
docker-compose down

# Start containers
docker-compose up -d
```

### Check EC2 Instance Health

1. Go to **EC2 Dashboard**
2. Click your instance
3. Check **Instance State** (should be "running")
4. Check **Status Checks** (should be "2/2 passed")

---

## 💰 Cost Optimization

### Free Tier (First 12 Months)
- EC2 t2.micro: FREE (1 GB RAM)
- 30 GB EBS storage: FREE
- Data transfer: FREE

### Estimated Monthly Costs (After Free Tier)
- EC2 t3.medium: $25-35
- 30 GB Storage: $3
- Data transfer: $0-5
- **Total**: ~$30-45/month

### Cost-Saving Tips
1. Use t2.micro for low traffic (Free Tier)
2. Use Auto Scaling for variable load
3. Set CloudWatch alarms to stop idle instances
4. Use Reserved Instances for long-term

---

## 🔒 Security Best Practices

### 1. Restrict SSH Access

```bash
# Allow only your IP
# In Security Group: SSH source = YOUR_IP/32
```

### 2. Keep System Updated

```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Use Strong Database Passwords

In `.env`:
```
DB_PASSWORD=VeryStr0ng!P@ssw0rd#2024
```

### 4. Enable SSL/HTTPS

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get free SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Update Nginx config with SSL
```

### 5. Enable CloudWatch Monitoring

In AWS Console:
- Go to CloudWatch
- Create alarms for CPU, disk, memory
- Set up SNS notifications

---

## 🐛 Troubleshooting

### Issue: Connection Refused

```bash
# Check if service is running
sudo systemctl status attendance

# Restart service
sudo systemctl restart attendance

# Check logs
sudo journalctl -u attendance -n 50
```

### Issue: Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

### Issue: Out of Memory

```bash
# Check memory usage
free -h

# Check running processes
ps aux --sort=-%mem | head -20

# Stop application and restart
sudo systemctl restart attendance
```

### Issue: Cannot Connect from Outside

1. Check Security Group rules (must allow inbound on 8501)
2. Check if instance is running
3. Check if service is running: `sudo systemctl status attendance`
4. Check firewall: `sudo ufw status`

### Issue: Database Connection Error

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Check logs
sudo tail -f /var/log/postgresql/postgresql.log
```

---

## 📚 Useful Commands

```bash
# View instance info
aws ec2 describe-instances --instance-ids i-1234567890abcdef0

# Stop instance (save costs)
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Terminate instance (DELETE - be careful!)
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# View EC2 instance logs
aws ec2 get-console-output --instance-id i-1234567890abcdef0
```

---

## 📞 Support & Resources

- AWS Documentation: https://docs.aws.amazon.com/ec2/
- Streamlit Documentation: https://docs.streamlit.io/
- OpenCV Documentation: https://docs.opencv.org/
- GitHub Repository: https://github.com/Hariss22H/Attendance-Management-System

---

## ✅ Deployment Checklist

- [ ] AWS account created and verified
- [ ] EC2 instance launched
- [ ] Security group configured
- [ ] Key pair created and saved
- [ ] SSH connection established
- [ ] Application deployed
- [ ] Application accessible at `http://IP:8501`
- [ ] Database running (if using PostgreSQL)
- [ ] Backups configured
- [ ] Monitoring set up
- [ ] SSL certificate obtained (optional)
- [ ] Domain name configured (optional)

---

## 🎉 You're Done!

Your Face Recognition Attendance System is now running on AWS EC2!

**Next Steps:**
1. Register students through the web interface
2. Upload training images
3. Train the model
4. Start marking attendance
5. View attendance reports

**For scaling:**
1. Add RDS database for production
2. Use S3 for image storage
3. Set up Auto Scaling
4. Use CloudFront CDN
5. Enable CloudWatch monitoring

---

**Last Updated**: November 25, 2025
**Status**: ✅ Production Ready
