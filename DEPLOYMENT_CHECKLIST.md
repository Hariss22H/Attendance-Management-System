# ✅ AWS EC2 Deployment Checklist

## 📋 Pre-Deployment Checklist

### AWS Account Setup
- [ ] AWS account created at https://aws.amazon.com/
- [ ] Email verified
- [ ] Payment method added
- [ ] Free tier eligibility confirmed

### Local Machine Preparation
- [ ] Git installed
- [ ] SSH client available (built-in on Linux/Mac, PuTTY on Windows)
- [ ] Attendance-Management-System repository cloned locally
- [ ] All documentation files reviewed

---

## 🚀 Deployment Checklist

### Step 1: Create EC2 Instance
- [ ] Navigate to AWS EC2 Console
- [ ] Click "Launch Instances"
- [ ] Selected: Ubuntu Server 22.04 LTS
- [ ] Instance type chosen: t3.medium (or t2.micro for free tier)
- [ ] Storage: 30 GB allocated
- [ ] Security group created with inbound rules:
  - [ ] SSH (22) - Your IP
  - [ ] HTTP (80) - 0.0.0.0/0
  - [ ] HTTPS (443) - 0.0.0.0/0
  - [ ] Custom TCP (8501) - 0.0.0.0/0
- [ ] Key pair created and downloaded
- [ ] Instance launched successfully

### Step 2: Secure Your Key
- [ ] Key file saved in secure location
- [ ] Key permissions set (chmod 400 on Linux/Mac)
- [ ] Key backed up
- [ ] Key path noted for reference

### Step 3: Connect to Instance
- [ ] Public IP address copied from AWS Console
- [ ] SSH connection established successfully
- [ ] SSH prompt shows "ubuntu@ip-xxx-xxx-xxx-xxx:~$"

### Step 4: Deploy Application

**Choose ONE deployment method:**

#### Option A: Docker Deployment
- [ ] Navigated to project directory
- [ ] Made script executable: `chmod +x scripts/docker-deploy.sh`
- [ ] Ran deployment: `./scripts/docker-deploy.sh`
- [ ] Docker containers created
- [ ] Application accessible at `http://IP:8501`

#### Option B: Automated Setup
- [ ] Navigated to project directory
- [ ] Made script executable: `chmod +x scripts/aws-setup.sh`
- [ ] Ran setup: `./scripts/aws-setup.sh`
- [ ] All dependencies installed
- [ ] Application configured
- [ ] Systemd service created

#### Option C: Manual Setup
- [ ] System packages updated: `sudo apt update && sudo apt upgrade -y`
- [ ] Python 3.9 installed
- [ ] OpenCV dependencies installed
- [ ] Virtual environment created
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Application started: `streamlit run app.py`

---

## 🔍 Post-Deployment Verification

### Application Access
- [ ] Application accessible at `http://YOUR_IP:8501` (Docker/Streamlit)
- [ ] Application accessible at `http://YOUR_IP` (Systemd with Nginx)
- [ ] Web interface loads without errors
- [ ] No 404 or connection refused errors

### Functionality Tests
- [ ] Student registration page loads
- [ ] Can enter enrollment number and name
- [ ] Can navigate to different sections
- [ ] Attendance section accessible
- [ ] View attendance section works
- [ ] No console errors in browser

### Service Status
- [ ] Application running continuously
- [ ] No crashes in first 5 minutes
- [ ] Logs show no critical errors
- [ ] CPU usage reasonable (< 50%)
- [ ] Memory usage acceptable (< 1 GB for Streamlit)

### Data Persistence
- [ ] Register a student and verify saved
- [ ] Exit and restart application
- [ ] Student data still exists after restart
- [ ] No data loss occurred

---

## 🔐 Security Configuration

### Security Best Practices
- [ ] SSH key securely stored
- [ ] SSH key permissions set to 400
- [ ] Security group rules restricted appropriately
- [ ] Database password set to strong value
- [ ] Environment variables configured (.env file)
- [ ] Sensitive information not in logs
- [ ] No hardcoded credentials in code

### Optional: SSL/HTTPS
- [ ] (Optional) SSL certificate obtained from Let's Encrypt
- [ ] (Optional) Certificate configured in Nginx/application
- [ ] (Optional) HTTP redirects to HTTPS

---

## 📊 Monitoring Setup

### Logging & Alerts
- [ ] Application logging working
- [ ] Logs accessible via `journalctl` or `docker logs`
- [ ] Error messages clear and actionable
- [ ] Log rotation configured (if applicable)

### (Optional) CloudWatch
- [ ] (Optional) CloudWatch alarm for CPU > 80%
- [ ] (Optional) CloudWatch alarm for memory > 80%
- [ ] (Optional) CloudWatch alarm for disk > 80%
- [ ] (Optional) SNS notifications configured

---

## 💾 Backup & Recovery

### Backup Strategy
- [ ] Backup script created
- [ ] Regular backup schedule established
- [ ] First backup completed
- [ ] Backup verified (can be restored)
- [ ] Backup location documented
- [ ] Backup retention policy set

### (Optional) AWS S3 Backups
- [ ] S3 bucket created (if using cloud backups)
- [ ] S3 backup script created
- [ ] Backups automatically uploaded to S3
- [ ] S3 lifecycle policy set (30 days retention)

---

## 📈 Performance Optimization

### Initial Optimization
- [ ] Instance type appropriate for workload
- [ ] EBS volume optimized
- [ ] Security group not overly permissive
- [ ] Database queries optimized (if using DB)

### (Optional) Advanced Optimization
- [ ] (Optional) CloudFront CDN configured
- [ ] (Optional) RDS database performance tuned
- [ ] (Optional) S3 cache configured
- [ ] (Optional) Auto Scaling group created

---

## 👥 Team Access & Documentation

### Documentation
- [ ] All deployment documentation reviewed
- [ ] Team members have access to README.md
- [ ] Troubleshooting guide shared
- [ ] Command reference guide provided
- [ ] Architecture diagram reviewed

### Team Setup
- [ ] SSH access provided to team members
- [ ] IAM users created for team (if applicable)
- [ ] Access credentials securely shared
- [ ] Team trained on basic operations
- [ ] Emergency contact information shared

---

## 🧪 Testing Checklist

### Functional Testing
- [ ] Student registration: ✅ Works
- [ ] Image upload: ✅ Works
- [ ] Model training: ✅ Works (desktop) or ⏭️ Future (web)
- [ ] Face recognition: ✅ Works (desktop) or ⏭️ Future (web)
- [ ] Attendance marking: ✅ Works
- [ ] Report generation: ✅ Works

### Load Testing (Optional)
- [ ] Application handles concurrent users
- [ ] Database can handle load
- [ ] No memory leaks detected
- [ ] Response time acceptable

### Edge Case Testing
- [ ] Large file uploads handled
- [ ] Invalid input rejected gracefully
- [ ] Network interruption recovery
- [ ] Database failure recovery

---

## 🎯 Go-Live Criteria

### All of these must be true:
- [ ] Application is stable (running 24 hours without crash)
- [ ] All team members trained
- [ ] Backup system verified working
- [ ] Monitoring in place
- [ ] Emergency procedures documented
- [ ] Security review completed
- [ ] Performance acceptable
- [ ] Data loss scenario tested and recovery verified

---

## 📋 Ongoing Maintenance Checklist

### Daily
- [ ] Application running and accessible
- [ ] No critical error logs
- [ ] Disk space adequate (> 20% free)

### Weekly
- [ ] Database backup completed successfully
- [ ] Check monitoring alerts
- [ ] Review application logs for issues
- [ ] Verify attendance data integrity

### Monthly
- [ ] Update security patches: `sudo apt update && sudo apt upgrade -y`
- [ ] Review and optimize database
- [ ] Check cost/usage in AWS Console
- [ ] Archive old attendance records
- [ ] Test backup restoration
- [ ] Review and update documentation

### Quarterly
- [ ] Security audit
- [ ] Performance review
- [ ] Capacity planning
- [ ] Update dependencies
- [ ] Team training refresher

---

## 🆘 Emergency Procedures

### Application Crash
- [ ] Check service status: `sudo systemctl status attendance`
- [ ] View logs for errors: `sudo journalctl -u attendance -n 100`
- [ ] Restart service: `sudo systemctl restart attendance`
- [ ] If still fails, check disk space: `df -h`
- [ ] Restore from backup if necessary

### Database Issues
- [ ] Check database status: `sudo systemctl status postgresql`
- [ ] Verify database connection in logs
- [ ] Restart database: `sudo systemctl restart postgresql`
- [ ] Restore database from backup if corrupted

### Server Unavailable
- [ ] Check EC2 instance status in AWS Console
- [ ] If stopped, start instance
- [ ] Check security group inbound rules
- [ ] Verify network connectivity
- [ ] Reboot instance if necessary

### Data Loss
- [ ] Stop application immediately
- [ ] Restore from most recent backup
- [ ] Verify data integrity
- [ ] Document incident
- [ ] Review backup procedures

---

## ✨ Final Verification

### Before Declaring "Done"
- [ ] All checkboxes above are checked
- [ ] Team has been trained
- [ ] Documentation is complete
- [ ] Backups are verified
- [ ] Monitoring is active
- [ ] You can access the system at: `http://YOUR_IP:8501`
- [ ] Application functions as expected
- [ ] You're ready to celebrate! 🎉

---

## 📞 Support & Resources

### Documentation Files in Repository
- `README.md` - Project overview
- `QUICK_START.md` - 5-minute quick start
- `AWS_DEPLOYMENT_GUIDE.md` - Complete deployment guide (50+ pages)
- `DEPLOYMENT_SUMMARY.md` - Summary of what was prepared
- `COMMAND_REFERENCE.md` - Useful commands
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Multi-container setup

### External Resources
- AWS EC2 Docs: https://docs.aws.amazon.com/ec2/
- Streamlit Docs: https://docs.streamlit.io/
- Ubuntu Help: https://help.ubuntu.com/
- Docker Docs: https://docs.docker.com/

### Getting Help
- GitHub Issues: https://github.com/Hariss22H/Attendance-Management-System/issues
- AWS Support: https://aws.amazon.com/support/
- Stack Overflow: https://stackoverflow.com/ (tag with `aws-ec2`, `streamlit`, `docker`)

---

## 🎉 Congratulations!

You have successfully deployed the Face Recognition Attendance System on AWS EC2!

**Next Steps:**
1. Register students through the web interface
2. Upload training images (via file system or admin interface)
3. Train the model
4. Start marking attendance
5. View attendance reports

**Questions?**
Check the documentation files listed above or create an issue on GitHub.

---

**Deployment Completed**: _________________ (Date)  
**Deployed By**: _________________ (Name)  
**Environment**: _________________ (Production/Staging/Development)  
**Instance IP**: _________________ (Your Public IP)  
**Notes**: _________________________________________________________________

---

**Last Updated**: November 25, 2025
**Status**: ✅ Production Ready
