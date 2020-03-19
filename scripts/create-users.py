# python ./scripts/create-users.py wsc.com "$PWD"/sample-files/worldskills.csv

import os
import csv
import sys
import time
import bash_commands
from create_user import create_user
from getpass import getpass

# check if params are given
if len(sys.argv) < 3:
    sys.exit("Usage: `python ./scripts/create-users.py <new domain> <path to csv>` (navigate to root directory first)")

# Ask for MYSQL credentials
mysql_username = input("MySQL username: ")
mysql_password = getpass("MySQL password: ")

# Extract params
domain = sys.argv[1]
csv_path = sys.argv[2]

# Give feedback that params are extracted successfully
print("----------------------------------------------")
print(f"Creating users on {domain} from {csv_path}...")

# Read CSV file
with open(csv_path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    user_count = 0
    for row in csv_reader:
        # Assumption: first row is the headers
        if line_count != 0: 
            # Extract data from row
            group = row[0]

            if group != "":
                username = row[1]
                password = row[2]

                SSHD_CONFIG_STRING = f"Match Group {group}\\n    ChrootDirectory /home/%u/ftp\\n"
                SSHD_CONFIG_STRING += "    AllowTCPForwarding no\\n    X11Forwarding no\\n"
                sshd_config_handle = [
                    f"if ! grep -q {group} /etc/group",
                    f"then sudo groupadd {group}",
                    "fi",
                    f"if ! grep -q 'Match Group {group}' /etc/ssh/sshd_config",
                    "then",
                    f'  sudo cp /etc/ssh/sshd_config "$PWD"/backup/ssh/sshd_config_{time.time()}',
                    f"  sudo sed -i '$ a {SSHD_CONFIG_STRING}' /etc/ssh/sshd_config",
                    "fi"
                ]
                delimiter = "\n"

                # add to sshd config if group is new
                os.system(delimiter.join(sshd_config_handle))
                
                # form the subdomain
                subdomain = username + "." + domain

                # Create user
                success = create_user(group, username, password, subdomain, mysql_username, mysql_password)
                if success:
                    user_count += 1
        line_count += 1
    print(f"Processed {line_count} lines, created {user_count} users.")
