import os
from os import path
import sys
from copy_commands import copy_commands
from create_conf import create_conf
from create_docker import create_docker

def create_user(group, username, password, subdomain, mysql_username, mysql_password):
    # Don't do anything if user already exists
    PARENT_DIR = f"/home/{username}"
    CHROOT_DIR = f"{PARENT_DIR}/ftp"

    if path.exists(PARENT_DIR):
        print("Username {username} already exists, please try another")
        return False
    else:
        # Create chroot parent dir
        os.system(f"sudo mkdir {PARENT_DIR}/")
        
        # create and add user to group
        # Creating and specifying home user dir will automatically create the dir
        os.system(f"sudo useradd -g {group} -m -d {CHROOT_DIR}/ -s /bin/bash -p $(openssl passwd -1 {password}) {username}")

        # Create other subdir
        os.system(f"sudo mkdir {CHROOT_DIR}/dev/")
        os.system(f"sudo mkdir {CHROOT_DIR}/html/")
        os.system(f"sudo mkdir {CHROOT_DIR}/etc/")
        os.system(f"sudo cp -vf /etc/passwd {CHROOT_DIR}/etc")
        os.system(f"sudo cp -vf /etc/group {CHROOT_DIR}/etc")

        # Populate the dev folder - thanks tecmint
        os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/null c 1 3")
        os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/tty c 5 0")
        os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/zero c 1 5")
        os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/random c 1 8")

        # Copy over the requried scripts for shell to work
        copy_commands(username)

        # Create a folder where files will be deployed
        os.system(f"sudo mkdir -p /var/www/html/{subdomain}/public_html/")

        # Mount /html to /var/www/html
        os.system(f"sudo sed -i '$ a \/var\/www\/html\/{subdomain}\/public_html \/home\/{username}\/ftp\/html none bind 0 0' /etc/fstab")
        os.system(f"sudo mount --bind /var/www/html/{subdomain}/public_html {CHROOT_DIR}/html")
    
        # Root owns the chroot jail
        os.system(f"sudo chown root:root {CHROOT_DIR}")

        # www-data:www-data owns the html folder
        # set permissions so user can put things into it
        os.system(f"sudo chown www-data:www-data {CHROOT_DIR}/html")
        os.system(f"sudo chmod -R 777 {CHROOT_DIR}/html")

        print("---------------------------")
        print(f"User {username} account setup successful.")
        print(f"Creating Docker container for {username}...")

        # Create a new Docker container,
        # Mapping the folders and ports appropriately
        create_docker(CHROOT_DIR, username, password)

        # Put a index.php file in html so that people know it works
        os.system(f"sudo echo '<?php echo \"{subdomain}\"; phpinfo(); ?>' > {CHROOT_DIR}/html/index.php ")
        
        # Create the Apache conf and enable it
        conf_text = create_conf(subdomain)
        os.system(f'sudo echo \'{conf_text}\' > /etc/apache2/sites-available/{subdomain}.conf')
        os.system(f'sudo ln -s /etc/apache2/sites-available/{subdomain}.conf /etc/apache2/sites-enabled/{subdomain}.conf')

        # Add to hosts file
        os.system(f"sudo sed -i '$ a 127.0.0.1 {subdomain}' /etc/hosts")
        
        # Restart Apache
        os.system("sudo systemctl restart apache2")

        print("---------------------------")
        print(f"Successfully setup FTP, SSH & Apache for user {username}")
        return True
