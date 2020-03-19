import os
from os import path
import sys
from getpass import getpass
from copy_commands import copy_commands
from create_conf import create_conf

# check if params are given
if len(sys.argv) < 5:
    sys.exit("Usage: `python ./scripts/create-user.py <domain> <group> <username> <password>` (navigate to root directory first)")

# Ask for MYSQL credentials
mysql_username = input("MySQL username: ")
mysql_password = getpass("MySQL password: ")

# Extract params
domain = sys.argv[1]
group = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
subdomain = username + "." + domain

# Don't do anything if user already exists
if path.exists(f"/home/{username}"):
    print(f"Username {username} already exists, please try another")
else:
    PARENT_DIR = f"/home/{username}"
    CHROOT_DIR = f"{PARENT_DIR}/ftp"
    
    # Create chroot parent dir
    os.system(f"sudo mkdir {PARENT_DIR}/")
    
    # create and add user to group
    # Creating and specifying home user dir will automatically create the dir
    os.system(f"sudo useradd -G {group} -m -d {CHROOT_DIR}/ -s /bin/bash -p $(openssl passwd -1 {password}) {username}")

    # Create other subdir
    os.system(f"sudo mkdir {CHROOT_DIR}/dev/")
    os.system(f"sudo mkdir {CHROOT_DIR}/html/")
    os.system(f"sudo mkdir {CHROOT_DIR}/etc/")
    os.system(f"sudo cp -vf /etc/passwd {CHROOT_DIR}/etc")
    os.system(f"sudo cp -vf /etc/group {CHROOT_DIR}/etc")

    # Create the conf and enable it
    conf_text = create_conf(subdomain)
    os.system(f"sudo echo '{conf_text}' > ./httpd/{subdomain}.conf")
    os.system(f"sudo ln -s ./httpd/{subdomain}.conf /etc/apache2/sites-enabled/{subdomain}.conf")
    # os.system(f"sudo a2ensite {subdomain}")

    # Add to hosts file
    # hosts_command = f"echo '127.0.0.1 {subdomain}' >> /etc/hosts"
    # os.system(f"sudo -- sh -c -e '{hosts_command}'")
    os.system(f"sudo sed -i '$ a 127.0.0.1 {subdomain}' /etc/hosts")

    # Populate the dev folder - thanks tecmint
    os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/null c 1 3")
    os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/tty c 5 0")
    os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/zero c 1 5")
    os.system(f"sudo mknod -m 666 {CHROOT_DIR}/dev/random c 1 8")

    # Copy over the requried scripts for shell to work
    copy_commands(username)

    # Handle the Apache side of things
    os.system(f"sudo mkdir /var/www/html/{subdomain}/")
    os.system(f"sudo mkdir /var/www/html/{subdomain}/public_html/")

    # Mount /html to /var/www/html
    os.system(f"sudo sed -i '$ a \/var\/www\/html\/{subdomain}\/public_html \/home\/{username}\/ftp\/html none bind 0 0' /etc/fstab")
    os.system(f"sudo mount --bind /var/www/html/{subdomain}/public_html {CHROOT_DIR}/html")
   
    # Root owns the chroot jail
    os.system(f"sudo chown root:root {CHROOT_DIR}")

    # www-data:www-data owns the html folder
    # set permissions so user can put things into it
    os.system(f"sudo chown www-data:www-data {CHROOT_DIR}/html")
    os.system(f"sudo chmod -R 777 {CHROOT_DIR}/html")

    # Put a index.php file in html so that people know it works
    os.system(f"sudo echo '<?php php_info(); echo \"{subdomain}\"; ?>' > {CHROOT_DIR}/html/index.php ")

    print("---------------------------")
    print(f"User {username} account setup successful.")
    print("Creating MySQL account...")

    # Create mysql user
    user_creation_command = [
        f"DROP USER IF EXISTS '{username}'@'%';",
        "FLUSH PRIVILEGES;",
        f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}';",
        f"GRANT USAGE ON *.* TO '{username}'@'%' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;",
        f"CREATE DATABASE {username}_test;"
    ]
    delimiter = "\n"
    user_creation_sql = f'mysql -u {mysql_username} -p{mysql_password} -e "{delimiter.join(user_creation_command)}"'
    os.system(user_creation_sql)
    
    print("---------------------------")
    print("Granting suitable privileges...")
    
    db_prefix = username + r'\_%'
    
    # need to escape the backticks or the shell will interpret them!
    # It's not a 'raw' issue on Python's part
    # https://stackoverflow.com/questions/39389231/backtick-is-not-working-to-run-mysql-queries-in-shell-script
    grant_prefix_command = f"GRANT ALL PRIVILEGES ON \`{db_prefix}\`.* TO '{username}'@'%';"
    grant_prefix_sql = f'mysql -u {mysql_username} -p{mysql_password} -e "{grant_prefix_command}"'
    os.system(grant_prefix_sql)

    # Restart Apache
    os.system("sudo systemctl restart apache2")

    print("---------------------------")
    print(f"Successfully setup MySQL, FTP, SSH & virtual host for user {username}")
