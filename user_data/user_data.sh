#!/bin/bash
# Install Apache Web Server and PHP
yum install -y httpd git
# Download Lab files
git clone https://github.com/ps-interactive/lab_aws_implement-auto-scaling-amazon-ecs
mv lab_aws_implement-auto-scaling-amazon-ecs/webapp/* /var/www/html/
# Turn on web server
chkconfig httpd on
service httpd start