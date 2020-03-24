# Update the package repo list
sudo apt-get update

# Enable the firewall and add rules :)
sudo ufw enable
sudo ufw allow http
sudo ufw allow https
sudo ufw allow ssh # sudo ufw allow 22

# Install net-tools
sudo apt-get install net-tools

# Install Apache and enable Proxy-ing modules
sudo apt-get install -y apache2
sudo a2enmod proxy proxy_http
sudo systemctl restart apache2

# Install vsftpd
sudo apt-get install -y vsftpd

# Install SSH
sudo apt-get install -y openssh-server

# Install Docker and build the image
sudo apt-get install -y docker.io
cd ./docker && sudo docker build -t kyurikotpq/lampm2 .
