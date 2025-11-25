# 🚀 Quick Start Guide - AWS EC2 Deployment

## ⏱️ 5-Minute Quick Start

### Prerequisites
- AWS account
- SSH key pair downloaded
- Terminal/PowerShell access

---

## Quick Deployment Steps

### Step 1: Launch EC2 Instance (5 minutes)

```
1. Go to: https://console.aws.amazon.com/ec2/
2. Click "Launch Instances"
3. Select: Ubuntu Server 22.04 LTS
4. Choose: t3.medium (or t2.micro for free tier)
5. Add Storage: 30GB
6. Security Group: Allow SSH (22), HTTP (80), Custom TCP (8501)
7. Create Key Pair: Download .pem file
8. Launch!
```

**Copy your Public IP address**

---

### Step 2: Connect & Deploy (2 minutes)

#### Windows (PowerShell):
```powershell
cd "C:\path\to\key"
ssh -i attendance-key.pem ubuntu@YOUR_PUBLIC_IP

# Then run:
git clone https://github.com/Hariss22H/Attendance-Management-System.git
cd Attendance-Management-System
chmod +x scripts/docker-deploy.sh
./scripts/docker-deploy.sh
```

#### Linux/Mac:
```bash
ssh -i ~/path/to/attendance-key.pem ubuntu@YOUR_PUBLIC_IP

# Then run:
git clone https://github.com/Hariss22H/Attendance-Management-System.git
cd Attendance-Management-System
chmod +x scripts/docker-deploy.sh
./scripts/docker-deploy.sh
```

---

### Step 3: Access Application (1 minute)

Open your browser:
```
http://YOUR_PUBLIC_IP:8501
```

**Done! 🎉**

---

## 📋 Complete Deployment Options

### Option 1: Docker (Fastest & Easiest)
```bash
./scripts/docker-deploy.sh
```
✅ **Pros**: Easy, fast, isolated, scalable
❌ **Cons**: Requires Docker knowledge

---

### Option 2: Automated Setup (Recommended for Beginners)
```bash
./scripts/aws-setup.sh
```
✅ **Pros**: Everything automated, systemd integration
❌ **Cons**: Takes longer to setup

---

### Option 3: Manual Setup (Learning)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3.9 python3-pip python3-venv git libsm6 libxext6 libxrender-dev libgl1-mesa-glx -y

# Setup project
git clone https://github.com/Hariss22H/Attendance-Management-System.git
cd Attendance-Management-System

# Create environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🔍 Verify Deployment

### Check if running:
```bash
# Docker option
docker ps

# Systemd option
sudo systemctl status attendance

# Direct option
ps aux | grep streamlit
```

### View logs:
```bash
# Docker
docker-compose logs -f web

# Systemd
sudo journalctl -u attendance -f

# Direct
tail -f /var/log/attendance-app/app.log
```

### Test connection:
```bash
curl http://localhost:8501
```

---

## 🛠️ Troubleshooting

### Port 8501 already in use
```bash
lsof -i :8501
kill -9 <PID>
```

### Not enough memory
```bash
free -h
# If < 1GB free, stop other services
```

### Cannot connect from outside
1. Check Security Group inbound rules (8501 open?)
2. Check firewall: `sudo ufw status`
3. Verify instance running: AWS Console → Instances

### Application crashes
```bash
# Check logs
docker-compose logs web
# or
sudo journalctl -u attendance -n 100
```

---

## 💾 Backup & Restore

### Backup data
```bash
# Backup all data
tar -czf attendance-backup.tar.gz StudentDetails/ TrainingImage/ Attendance/ TrainingImageLabel/

# Download locally (from your computer)
scp -i attendance-key.pem ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/Attendance-Management-System/attendance-backup.tar.gz ./

# Upload to S3 (optional)
aws s3 cp attendance-backup.tar.gz s3://your-bucket/backups/
```

### Restore data
```bash
tar -xzf attendance-backup.tar.gz
```

---

## 🔐 Security

### Change SSH key permissions
```powershell
# Windows
icacls attendance-key.pem /grant:r "$($env:USERNAME):(F)"

# Linux/Mac
chmod 400 attendance-key.pem
```

### Restrict SSH access
In AWS Security Group:
- SSH source: Your IP only (not 0.0.0.0/0)

### Update database password
Edit `.env`:
```
DB_PASSWORD=YourNewSecurePassword123!
```

---

## 📈 Monitoring

### CPU & Memory
```bash
top
# or
htop  # (install if needed: sudo apt install htop)
```

### Disk space
```bash
df -h
```

### Network
```bash
# Check bandwidth usage
iftop
```

---

## 💰 Cost Estimation

**First 12 Months (Free Tier)**
- EC2 t2.micro: FREE
- 30GB Storage: FREE
- Total: $0 (mostly)

**After Free Tier (t3.medium)**
- EC2: ~$30-35/month
- Storage: ~$3/month
- Data transfer: ~$0-5/month
- **Total: ~$40-50/month**

**Cost Optimization**
- Use t2.micro for low traffic
- Stop instance when not in use
- Use Reserved Instances for discounts

---

## 🚀 Scaling (Future)

When you need more power:

1. **Add Database**: RDS PostgreSQL
2. **Object Storage**: AWS S3
3. **CDN**: CloudFront
4. **Load Balancing**: AWS ELB
5. **Auto Scaling**: Automatic scaling groups

See: `AWS_DEPLOYMENT_GUIDE.md` for details

---

## 📞 Support

- **Docs**: `AWS_DEPLOYMENT_GUIDE.md`
- **Issues**: Create GitHub issue
- **Community**: Check GitHub Discussions

---

## ✅ Checklist

- [ ] AWS account created
- [ ] EC2 instance running
- [ ] Security group configured
- [ ] Application deployed
- [ ] Accessible at `http://IP:8501`
- [ ] Students can register
- [ ] Attendance can be marked
- [ ] Data is being saved

---

## 🎓 Next Steps

1. **Register students** through web interface
2. **Upload training images** for each student
3. **Train the model** with collected images
4. **Start marking attendance** using face recognition
5. **View reports** and analytics

---

**You're all set! 🎉 Start using your attendance system!**

For detailed guide: See `AWS_DEPLOYMENT_GUIDE.md`
