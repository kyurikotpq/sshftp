# Update the package repo list
sudo apt-get update

# Enable the firewall and add rules :)
sudo ufw enable
sudo ufw allow http
sudo ufw allow https
sudo ufw allow ssh # sudo ufw allow 22

# Install net-tools
sudo apt-get install net-tools

# Install Apache
sudo apt-get install apache2

# Install vsftpd
sudo apt-get install vsftpd

# Install SSH
sudo apt-get install openssh-server

# Install Docker and build the image
sudo apt-get install docker.io
cd ./docker && sudo docker build -t $USER/alpine-lamp .