#!/bin/bash

# File Splitter Deployment Script
# Run this script on your VPS

set -e

echo "🚀 Starting File Splitter deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/filesplitter
sudo chown -R $USER:$USER /var/www/filesplitter

# Copy application files (replace with your actual deployment method)
echo "📋 Copying application files..."
# scp -r ./* user@your-vps:/var/www/filesplitter/

# Setup Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd /var/www/filesplitter
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads downloads
chmod 755 uploads downloads

# Setup environment file
echo "🔧 Setting up environment configuration..."
cp .env.example .env
# Edit .env file with your actual values
nano .env

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Setup systemd service
echo "⚙️ Setting up systemd service..."
sudo cp filesplitter.service /etc/systemd/system/
sudo sed -i 's|/path/to/your/app|/var/www/filesplitter|g' /etc/systemd/system/filesplitter.service
sudo sed -i 's|/path/to/your/venv|/var/www/filesplitter/venv|g' /etc/systemd/system/filesplitter.service
sudo systemctl daemon-reload
sudo systemctl enable filesplitter
sudo systemctl start filesplitter

# Setup Nginx
echo "🌐 Setting up Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/filesplitter
sudo sed -i 's|your-domain.com|filesplitter.floweasy.app|g' /etc/nginx/sites-available/filesplitter
sudo sed -i 's|/path/to/your/app|/var/www/filesplitter|g' /etc/nginx/sites-available/filesplitter
sudo ln -s /etc/nginx/sites-available/filesplitter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup firewall
echo "🔥 Setting up firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Setup SSL (optional)
echo "🔒 Setting up SSL certificate..."
# sudo certbot --nginx -d filesplitter.floweasy.app -d www.filesplitter.floweasy.app

echo "✅ Deployment completed!"
echo ""
echo "🌐 Your application should be available at:"
echo "   HTTP:  http://your-vps-ip"
echo "   HTTPS: https://filesplitter.floweasy.app (after SSL setup)"
echo ""
echo "🔧 Useful commands:"
echo "   Check status: sudo systemctl status filesplitter"
echo "   View logs: sudo journalctl -u filesplitter -f"
echo "   Restart app: sudo systemctl restart filesplitter"
echo "   Reload nginx: sudo systemctl reload nginx"