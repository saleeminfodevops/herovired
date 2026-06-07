#!/bin/bash
# Update the package index
apt-get update -y

# Install Apache2
apt-get install apache2 -y

# Start Apache and ensure it runs on boot
systemctl start apache2
systemctl enable apache2

# Optional: Create a custom landing page
echo "<h1>Hello, World! Herovired skiltest task1</h1>" > /var/www/html/index.html
