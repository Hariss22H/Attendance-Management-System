# 📚 AWS EC2 Deployment - Command Reference Guide

## 🚀 Quick Command Reference

### Connection Commands

```bash
# Windows PowerShell
ssh -i attendance-key.pem ubuntu@YOUR_PUBLIC_IP

# Linux/Mac
ssh -i ~/path/to/attendance-key.pem ubuntu@YOUR_PUBLIC_IP

# Copy files to/from EC2
scp -i key.pem local-file ubuntu@IP:/home/ubuntu/
scp -i key.pem ubuntu@IP:/home/ubuntu/file local-destination
```

---

## 🐳 Docker Commands

### Build & Deploy

```bash
# Build image
docker build -t attendance-system:latest .

# Run container
docker run -p 8501:8501 attendance-system:latest

# Docker Compose (Recommended)
docker-compose up -d          # Start all services
docker-compose down           # Stop all services
docker-compose restart        # Restart services
docker-compose logs -f web    # View logs
```

### Container Management

```bash
# List containers
docker ps                     # Running containers
docker ps -a                  # All containers

# View logs
docker logs container-id
docker logs -f container-id   # Follow logs

# Execute command in container
docker exec -it container-id bash

# Stop/Start container
docker stop container-id
docker start container-id
docker restart container-id

# Remove container
docker rm container-id
```

---

## 🔧 Systemd Service Commands

```bash
# Start service
sudo systemctl start attendance

# Stop service
sudo systemctl stop attendance

# Restart service
sudo systemctl restart attendance

# Check status
sudo systemctl status attendance

# Enable on boot
sudo systemctl enable attendance

# Disable on boot
sudo systemctl disable attendance

# View logs
sudo journalctl -u attendance -n 50        # Last 50 lines
sudo journalctl -u attendance -f           # Follow logs
sudo journalctl -u attendance --since "1 hour ago"  # Last hour
```

---

## 📂 File Management

### Directory Navigation

```bash
# Change directory
cd /home/ubuntu/Attendance-Management-System

# List files
ls -la
ls -lh                       # Human readable sizes
tree                         # Tree view (if installed)

# Create directory
mkdir -p data/backup

# Remove directory
rm -rf directory-name

# Show disk usage
df -h                        # Disk space
du -sh directory-name        # Directory size
```

### File Operations

```bash
# View file
cat filename
less filename                 # Page through file
head -n 20 filename           # First 20 lines
tail -n 20 filename           # Last 20 lines
tail -f filename              # Follow file

# Edit file
nano filename
vi filename

# Copy file
cp source destination
cp -r source-dir dest-dir

# Move/Rename
mv oldname newname
mv file /new/location/

# Create file
touch filename
echo "content" > filename
```

---

## 📦 Package Management

```bash
# Update packages
sudo apt update              # Refresh package list
sudo apt upgrade -y          # Upgrade installed packages
sudo apt full-upgrade -y     # Full upgrade

# Install package
sudo apt install package-name

# Remove package
sudo apt remove package-name
sudo apt purge package-name   # With config files

# Search package
apt search package-name

# Show package info
apt show package-name

# Clean cache
sudo apt clean
sudo apt autoclean
```

---

## 🌐 Network & Connectivity

```bash
# Check connectivity
ping 8.8.8.8
curl https://google.com

# Port usage
lsof -i :8501               # What's using port 8501
netstat -tuln               # All listening ports
ss -tuln                    # Modern alternative

# Check public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4
curl ifconfig.me
curl ipinfo.io

# DNS lookup
nslookup domain.com
dig domain.com

# Network interface
ip addr                     # IP addresses
ip route                    # Routing table
```

---

## 💾 Backup & Restore

```bash
# Create backup
tar -czf backup.tar.gz directory/

# Extract backup
tar -xzf backup.tar.gz

# Upload to S3
aws s3 cp file s3://bucket/path/

# Download from S3
aws s3 cp s3://bucket/file .

# Backup database
pg_dump database_name > backup.sql

# Restore database
psql database_name < backup.sql
```

---

## 🔍 Monitoring & Logging

```bash
# System resources
top                         # Real-time processes
htop                        # Enhanced top
ps aux                      # All processes
ps aux | grep streamlit     # Search processes

# Memory usage
free -h                     # Memory info
free -h -s 1                # Continuous monitoring

# CPU usage
uptime                      # Load average
mpstat                      # CPU statistics

# Disk usage
df -h                       # Disk space
du -sh *                    # Directory sizes

# Log monitoring
tail -f /var/log/syslog
dmesg | tail -20
journalctl -xe              # System journal
```

---

## 🚀 Application Startup Variations

### Option 1: Streamlit Direct

```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# With additional options
streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --logger.level info \
  --client.showErrorDetails true
```

### Option 2: Systemd Service

```bash
sudo systemctl start attendance
sudo systemctl status attendance
sudo journalctl -u attendance -f
```

### Option 3: Docker

```bash
docker-compose up -d
docker-compose logs -f web
docker-compose restart web
```

### Option 4: Background Process

```bash
# Run in background
nohup streamlit run app.py &

# Or with screen
screen -S attendance
streamlit run app.py

# Detach: Ctrl+A then D
# Reattach: screen -r attendance
```

---

## 🛠️ Troubleshooting Commands

### Debug Connectivity

```bash
# Test port
nc -zv localhost 8501
curl http://localhost:8501

# From another machine
curl http://YOUR_IP:8501

# Check firewall
sudo ufw status
sudo ufw allow 8501
```

### Debug Application

```bash
# Check if running
pgrep streamlit

# Find process ID
ps aux | grep streamlit

# Kill process
kill -9 PID
pkill -f streamlit

# Check resource usage
ps aux | grep streamlit | awk '{print $2, $3, $4, $5, $6}'
```

### Debug Database

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Connect to database
psql -U attendance_user -d attendance_db -h localhost

# From PostgreSQL prompt
\dt                         # List tables
\q                          # Quit

# Check database size
du -sh /var/lib/postgresql/
```

---

## 📊 Performance Commands

```bash
# Watch system in real-time
watch -n 1 free -h
watch -n 1 df -h

# Network bandwidth
iftop
nethogs

# I/O performance
iostat 1 10

# Application performance
time streamlit run app.py

# Memory profiler
python -m memory_profiler app.py
```

---

## 🔐 Security Commands

```bash
# SSH key permissions
chmod 400 key.pem

# File permissions
chmod 644 file                  # Read for all, write for owner
chmod 755 directory            # Execute for directories
chmod 600 sensitive-file        # Only owner can access

# User management
sudo useradd username
sudo passwd username
sudo usermod -aG sudo username
sudo userdel username

# Firewall
sudo ufw enable
sudo ufw disable
sudo ufw allow 22
sudo ufw allow 8501
sudo ufw status
```

---

## 🐍 Python Commands

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# Install requirements
pip install -r requirements.txt

# List installed packages
pip list
pip list | grep opencv

# Show package info
pip show package-name

# Freeze environment
pip freeze > requirements.txt

# Uninstall package
pip uninstall package-name
```

---

## 🔄 Git Commands (On EC2)

```bash
# Clone repository
git clone https://github.com/username/repo.git

# Pull updates
git pull origin main

# Check status
git status

# View logs
git log --oneline -n 10

# Switch branch
git checkout -b new-branch

# Commit changes
git add .
git commit -m "message"
git push origin main
```

---

## 📝 Text Editing Cheat Sheet

### Nano
```
Ctrl+X  = Exit
Ctrl+S  = Save
Ctrl+O  = Open file
Ctrl+W  = Search
```

### Vi/Vim
```
i       = Insert mode
:w      = Write/save
:q      = Quit
:wq     = Write and quit
:q!     = Quit without saving
dd      = Delete line
yy      = Copy line
p       = Paste
```

---

## 🎯 Common Tasks Workflow

### Deploy New Version

```bash
cd /home/ubuntu/Attendance-Management-System

# Stop current service
sudo systemctl stop attendance

# Pull latest code
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl start attendance

# Check status
sudo systemctl status attendance
```

### Backup Data

```bash
# Create backup
tar -czf ~/backups/attendance-$(date +%Y-%m-%d).tar.gz StudentDetails/ TrainingImage/ Attendance/

# Upload to S3
aws s3 cp ~/backups/attendance-*.tar.gz s3://my-bucket/backups/

# List backups
ls -lh ~/backups/
```

### Monitor Application

```bash
# Check if running
sudo systemctl status attendance

# View last 50 lines of logs
sudo journalctl -u attendance -n 50

# Continuous logs
sudo journalctl -u attendance -f

# Check resource usage
top -p $(pgrep -f streamlit)
```

---

## 🆘 Emergency Commands

### Emergency Restart

```bash
# Force restart service
sudo systemctl restart attendance

# Force kill process
pkill -9 -f streamlit

# Restart everything
sudo systemctl reboot
```

### Emergency Restore

```bash
# From backup
tar -xzf backup.tar.gz

# Stop app
sudo systemctl stop attendance

# Restore files
cp -r StudentDetails/ TrainingImage/ Attendance/ /app/

# Restart
sudo systemctl start attendance
```

### Emergency Cleanup

```bash
# Remove old logs
sudo journalctl --vacuum=time:1d

# Clean apt cache
sudo apt clean

# Remove old files
find . -type f -atime +30 -delete
```

---

## 📌 Keep This Handy

### Save to reference file
```bash
cat > ~/commands-reference.txt << 'EOF'
[Paste this entire document]
EOF
```

### Quick search in terminal
```bash
grep -n "Docker Commands" ~/commands-reference.txt
```

---

## 🎓 Learning Resources

- **AWS CLI Docs**: https://docs.aws.amazon.com/cli/latest/userguide/
- **Linux Commands**: https://linux.die.net/man/
- **Docker Docs**: https://docs.docker.com/
- **Git Docs**: https://git-scm.com/doc

---

**Save this file for quick reference!** 💾
