# File Splitter - VPS Deployment Guide

A Flask web application for splitting CSV, TXT, and Excel files by column with user authentication and usage limits.

**Domain:** https://filesplitter.floweasy.app

## 🚀 Quick Deployment

### Prerequisites
- Ubuntu/Debian VPS
- Domain name (optional but recommended)
- Root or sudo access

### One-Command Deployment
```bash
# Make script executable and run
chmod +x deploy.sh
sudo ./deploy.sh
```

## 📋 Manual Deployment Steps

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx
```

### 2. Application Setup
```bash
# Create application directory
sudo mkdir -p /var/www/filesplitter
sudo chown -R $USER:$USER /var/www/filesplitter

# Upload your application files to /var/www/filesplitter/
# You can use scp, rsync, or git clone
```

### 3. Python Environment
```bash
cd /var/www/filesplitter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

### 5. Database Initialization
```bash
# Initialize database
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 6. Systemd Service
```bash
# Copy service file
sudo cp filesplitter.service /etc/systemd/system/

# Update paths in service file
sudo sed -i 's|/path/to/your/app|/var/www/filesplitter|g' /etc/systemd/system/filesplitter.service
sudo sed -i 's|/path/to/your/venv|/var/www/filesplitter/venv|g' /etc/systemd/system/filesplitter.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable filesplitter
sudo systemctl start filesplitter
```

### 7. Nginx Configuration
```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/filesplitter

# Update domain and paths
sudo sed -i 's|your-domain.com|your-actual-domain.com|g' /etc/nginx/sites-available/filesplitter
sudo sed -i 's|/path/to/your/app|/var/www/filesplitter|g' /etc/nginx/sites-available/filesplitter

# Enable site
sudo ln -s /etc/nginx/sites-available/filesplitter /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### 8. SSL Certificate (Optional)
```bash
# Get free SSL certificate
sudo certbot --nginx -d filesplitter.floweasy.app -d www.filesplitter.floweasy.app
```

### 9. Firewall Setup
```bash
# Configure firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

## 🔧 Configuration Files

### Environment Variables (.env)
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=sqlite:///filesplitter.db
HOST=0.0.0.0
PORT=8000
UPLOAD_FOLDER=uploads
DOWNLOAD_FOLDER=downloads
MAX_CONTENT_LENGTH=104857600
```

### Important Paths to Update
- `/path/to/your/app` → `/var/www/filesplitter`
- `/path/to/your/venv` → `/var/www/filesplitter/venv`
- `your-domain.com` → `filesplitter.floweasy.app`

## 📊 Monitoring & Maintenance

### Check Application Status
```bash
sudo systemctl status filesplitter
```

### View Application Logs
```bash
sudo journalctl -u filesplitter -f
```

### View Nginx Logs
```bash
sudo tail -f /var/log/nginx/filesplitter_access.log
sudo tail -f /var/log/nginx/filesplitter_error.log
```

### Restart Services
```bash
sudo systemctl restart filesplitter
sudo systemctl reload nginx
```

## 🔒 Security Considerations

1. **File Permissions**: Keep sensitive files secure
2. **Firewall**: Only open necessary ports
3. **SSL**: Use HTTPS in production
4. **Updates**: Keep system and dependencies updated
5. **Backups**: Regular database backups

## 🚨 Troubleshooting

### Application Won't Start
```bash
# Check logs
sudo journalctl -u filesplitter -n 50

# Check if port is in use
sudo netstat -tlnp | grep :8000
```

### Nginx Errors
```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/filesplitter
sudo chmod -R 755 /var/www/filesplitter
```

## 📈 Production Optimizations

1. **Use PostgreSQL** instead of SQLite for better performance
2. **Enable gzip compression** in Nginx
3. **Set up monitoring** with tools like Prometheus
4. **Configure log rotation**
5. **Set up backups** for database and user files

## 🌐 Domain Setup

1. Point your domain A record to your VPS IP
2. Update nginx.conf with your domain
3. Run certbot for SSL
4. Update DNS records if needed

## 📞 Support

If you encounter issues:
1. Check the logs using the commands above
2. Verify all paths in configuration files
3. Ensure all dependencies are installed
4. Check file permissions

Your File Splitter application should now be running at https://filesplitter.floweasy.app!