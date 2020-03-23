import os
import sys
import time
from getpass import getpass

# check if params are given
if len(sys.argv) < 3:
    sys.exit("Usage: `python ./scripts/remove-user.py <domain> <username>` (navigate to root directory first)")

# Extract params
domain = sys.argv[1]
username = sys.argv[2]
subdomain = username + "." + domain

# remove domain from hosts
# backup first!
os.system(f'sudo cp /etc/hosts "$PWD"/backup/hosts/hosts_{time.time()}')
os.system(f"sudo sed -i '/127.0.0.1 {subdomain}/d' /etc/hosts")

# umount from fstab and actual unmounting
os.system(f"sudo sed -i '/\/var\/www\/html\/{subdomain}\/public_html \/home\/{username}\/ftp\/html none bind 0 0/d' /etc/fstab")
os.system(f"sudo umount /home/{username}/ftp/html")

# remove conf and folder
os.system(f"sudo unlink /etc/apache2/sites-enabled/{subdomain}.conf")
os.system(f'sudo rm /etc/apache2/sites-available/{subdomain}.conf')
os.system(f"sudo rm -rf /home/{username}")
os.system(f"sudo rm -rf /var/www/html/{subdomain}")
os.system(f"sudo userdel {username}")

# Remove Docker container
os.system(f"sudo docker rm {username}");

# restart apache
os.system("sudo systemctl restart apache2")

print("---------------------------")
print(f"Successfully removed {username} from FTP, SSH & Apache")
