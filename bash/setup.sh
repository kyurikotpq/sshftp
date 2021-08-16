# Update the package repo list
sudo apt-get update

# Enable the firewall and add rules :)
sudo ufw enable
sudo ufw allow http
sudo ufw allow https
sudo ufw allow ssh # sudo ufw allow 22
sudo ufw allow 21 # Allow FTP
sudo ufw allow 2222 # Allow SFTP configured on port 2222

# Install net-tools
sudo apt-get install net-tools

# Install Apache and enable Proxy-ing modules
sudo apt-get install -y apache2
sudo a2enmod proxy proxy_http

# Install SSH
sudo apt-get install -y openssh-server

# Switch to Python 3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Install Docker and build the image
sudo apt-get install -y docker.io
cd ./docker && sudo docker build -t $USER/alpine-lamp .

# Restart services that I've configured
sudo systemctl restart apache2

# Enable services at startup
sudo systemctl enable apache2
sudo systemctl enable ssh
sudo systemctl enable docker