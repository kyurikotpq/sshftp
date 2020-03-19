import os
import sys
import time
from getpass import getpass

# check if params are given
if len(sys.argv) < 3:
    sys.exit("Usage: `python ./scripts/remove-user.py <domain> <username>` (navigate to root directory first)")

# Ask for MYSQL credentials
mysql_username = input("MySQL username: ")
mysql_password = getpass("MySQL password: ")

# Extract params
domain = sys.argv[1]
username = sys.argv[2]
subdomain = username + "." + domain

# remove domain from hosts
# backup first!
os.system(f'sudo cp /etc/hosts "$PWD"/backup/hosts/hosts_{time.time()}')
# os.system(f'sudo mv "$PWD"/backup/hosts "$PWD"/backup/hosts_{time.time()}')
os.system(f"sudo sed -i '/127.0.0.1 {subdomain}/d' /etc/hosts")

# umount from fstab and actual unmounting
os.system(f"sudo sed -i '/\/var\/www\/html\/{subdomain}\/public_html \/home\/{username}\/ftp\/html none bind 0 0/d' /etc/fstab")
os.system(f"sudo umount /home/{username}/ftp/html")

# remove conf and folder
os.system(f"sudo unlink /etc/apache2/sites-enabled/{subdomain}.conf")
os.system(f'sudo rm "$PWD"/httpd/{subdomain}.conf')
os.system(f"sudo rm -rf /home/{username}")
os.system(f"sudo rm -rf /var/www/html/{subdomain}")
os.system(f"sudo userdel {username}")

# remove from MySQL
MYSQL_CONNECT = f"mysql -u {mysql_username} -p{mysql_password}"
sql_command = [
    "SELECT CONCAT('DROP DATABASE \`',schema_name,'\`;') AS \`-- Drop DBs with prefix \`",
    "FROM information_schema.schemata",
    f"WHERE schema_name LIKE '{username}_%'",
    "ORDER BY schema_name;",
    f"DROP USER IF EXISTS {username};"
]
delimiter = " "

filename = f"drop_{username}.sql"
os.system(f'{MYSQL_CONNECT} -e "{delimiter.join(sql_command)}" > "$PWD"/{filename}')
os.system(f'{MYSQL_CONNECT} < {filename}')
os.system(f'sudo rm "$PWD"/{filename}')

# restart apache
os.system("sudo systemctl restart apache2")

print("---------------------------")
print(f"Successfully removed {username} from MySQL, FTP, SSH & virtual host")
