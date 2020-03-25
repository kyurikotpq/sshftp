import os
from os import path
import sys
from .create_conf import create_conf
from .create_docker import create_docker


def create_user(PORT, group, username, password, subdomain):
    # Don't do anything if user already exists
    PARENT_DIR = f"/home/{username}"
    CHROOT_DIR = f"{PARENT_DIR}/ftp"

    if path.exists(PARENT_DIR):
        print(f"Username {username} already exists, please try another")
        return False
    else:
        # Create chroot parent dir
        os.system(f"sudo mkdir {PARENT_DIR}/")

        # create and add user to specified group and docker group
        # Creating and specifying home user dir will automatically create the dir
        os.system(
            f"sudo useradd -g {group} -m -d {CHROOT_DIR}/ -s /bin/bash -p $(openssl passwd -1 {password}) {username}")

        # Create other subdir
        os.system(f"sudo mkdir {CHROOT_DIR}/html/")

        # Copy over the requried scripts for shell to work
        os.system(f'sudo cp "$PWD"/default-files/forward.sh {CHROOT_DIR}/')

        # Create a folder where files will be deployed
        os.system(f"sudo mkdir -p /var/www/html/{subdomain}/public_html/")

        # Mount /html to /var/www/html
        os.system(
            f"sudo sed -i '$ a \/var\/www\/html\/{subdomain}\/public_html \/home\/{username}\/ftp\/html none bind 0 0' /etc/fstab")
        os.system(
            f"sudo mount --bind /var/www/html/{subdomain}/public_html {CHROOT_DIR}/html")

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
        create_docker(CHROOT_DIR, PORT, username, password)

        # Put a index.php file in html so that people know it works
        os.system(
            f"sudo echo '<?php echo \"{subdomain}\"; phpinfo(); ?>' > {CHROOT_DIR}/html/index.php ")

        # Create the Apache conf and enable it
        conf_text = create_conf(subdomain, PORT)
        os.system(
            f'echo \'{conf_text}\' | sudo tee /etc/apache2/sites-available/{subdomain}.conf')
        os.system(
            f'sudo ln -s /etc/apache2/sites-available/{subdomain}.conf /etc/apache2/sites-enabled/{subdomain}.conf')

        # Add to hosts file
        os.system(f"sudo sed -i '$ a 127.0.0.1 {subdomain}' /etc/hosts")

        # Restart Apache
        os.system("sudo systemctl restart apache2")

        print("---------------------------")
        print(f"Successfully setup FTP, SSH & Apache for user {username}")
        return True
