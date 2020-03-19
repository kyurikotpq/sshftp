# sshftp scripts
A collection of Python scripts to make linux webserver sysadmin easier. Requires Python 3.7.5 installed.

## This repo is in a mess and I'm going to clean it up by the end of Mar 2020.

**Why Python and not Bash:** 
1) I'm trying to pick up Python
2) I don't actively use a Linux device at home

## Switching to Python 3.7 from Python 2
(assuming you have 3.7.5 already installed)
```bash
# update-alternatives: --install needs <link> <name> <path> <priority>
# Therefore, run:

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```

## Run index.sh, which will in turn run:
### startup.sh
- Individual Usage: `./index.sh` (navigate to root directory first)
- In charge of starting the firewall, apache, sftp (vsftpd), ssh, and mysql

# Individually-run scripts
### create-users.py
- Usage: `python ./scripts/create-users.py <new domain> <path to csv>` (navigate to root directory first)
- In charge of creating users from CSV file (FORMAT: group,username,password)
- Please provide a domain without the subdomain, i.e. google.com