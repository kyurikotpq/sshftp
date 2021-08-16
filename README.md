# sshftp scripts
A collection of Python scripts that (run Bash commands to) easily create LAMP instances in Docker. You can easily create and delete users on your Linux machine; these users can deploy and manage their websites via SSH and FTP.

**Use Case**
- Users need to be able to deploy their websites on this server
- Users need to be segregated during SSH and FTP sessions, i.e. they can't access another user's files
- In the SSH sessions, shared software like `php`, `mysql` should be accessible

**Backstory**
- Please see the file [Backstory.md](/Backstory.md)

**Why Python and not Bash:** 
1) I'm trying to pick up Python
2) I don't actively use a Linux device at home

# Acknowledgements
Thank you @glats for your alpine-lamp with phpmyadmin Dockerfile. It has helped me immensely in getting started with Docker and implementing my own image that suits the needs of this project. For more information, you may view the `docker` folder in this project.

# Host System requirements
- Tested with Ubuntu 19.10
- Packages: net-tools, apache2, Python 3.7.5
- Apache: `sudo a2enmod proxy proxy_http`

## Remember to switch to Python 3.7 from Python 2
(assuming you have 3.7.5 already installed)
```bash
# update-alternatives: --install needs <link> <name> <path> <priority>
# Therefore, run:

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```

## If you are starting with a fresh installation of Ubuntu
1. Navigate to the project root directory
2. Make the script executable: `sudo chmod +x ./bash/setup.sh`
3. Run setup.sh: `./bash/setup.sh`.
It will take care of the installation of the necessary packages for this project to run.

## If you have already installed and configured the packages
```bash
sudo apt-get install docker.io # ONLY if Docker is not yet installed 
cd ./docker && sudo docker build -t $USER/alpine-lamp .
```

---

# ./scripts and their functionalities
## Standalone scripts
Run these scripts from the command line.
- [create-users.py](/#create-users.py)
- [remove-user.py](/#remove-user.py)

### `create-users.py`
Creates users from a CSV file.
**users.csv**
```
Group,Username,Password
competitor,bb,bb123!
competitor,cc,cc123!
```

1. Navigate to project root directory
2. Run the script. Example:
```bash
# python ./scripts/create-users.py <new domain> <path to csv>
python ./scripts/create-users.py google.com ./sample-files/users.csv
```

## Helper scripts
These scripts aid in the execution of the above standalone scripts by exporting functionalities into one Python function. **They cannot be run from the command line.**
- create_user.py: Handles creation of one user
- create_conf.py: Handles creation of .conf file for Apache
- create_docker.py: Handles creation of Docker container named after the user's username
- bash_commands.py: List of file paths to binaries, etc. to enable commands in the user's SSH shell
- copy_commands.py: Copies the binaries, etc. defined in `bash_commands.py` to the user's home directory
