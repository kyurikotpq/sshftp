# sshftp scripts
A collection of Python scripts to make Linux webserver sysadmin easier.

**Why Python and not Bash:** 
1) I'm trying to pick up Python
2) I don't actively use a Linux device at home

# Acknowledgements
Thank you @glats for your alpine-lamp with phpmyadmin Dockerfile. It has helped me immensely in getting started with Docker and implementing my own image that suits the needs of this project. For more information, you may view the `docker` folder in this project.

# A few observations
```bash
cd ./docker
sudo docker build -t kyurikotpq/alpine-lamp .

sudo docker run -d -v ~/Desktop/sshftp/containers:/var/www/localhost/htdocs/ -e MYSQL_ROOT_PASSWORD=lamp-1 -p 8080:80 --name lamp-1 kyurikotpq/alpine-lamp

sudo docker exec -it lamp-exec -it lamp-1 /bin/sh
```
Container is accessible via localhost:8080 in the browser.
Container's htdocs is bound to sshftp/containers thanks to the -v parameter. We can use this for ftp and use the ftp chroot folder instead for apache-rendering. Then on the container side, it will just be handling the phpmyadmin stuff tbh. But i guess it works both ways...

What if i don't bind?

Container name can be admin number.
Container port (8080) can be random generated?

---

# Host System requirements
- Tested with Ubuntu 19.10
- Packages: net-tools, vsftpd, apache2, Python 3.7.5
- Apache: `sudo a2enmod proxy proxy_http`
- VSFTPD: `chroot_local_user=YES` (uncommented)

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