import os

# Get a not-used port from 50000:60000
def get_port():
    count = 50000

    while(os.system(f"sudo netstat -ntlp | grep {count}")):
        count += 1

    return count

# Create a new container for the user :)
def create_docker(CHROOT_DIR, username, password):
    PORT = get_port()
    
    COMMAND_LINES = [
        f"sudo docker run -d -v {CHROOT_DIR}/html:/var/www/localhost/htdocs/",
        f"-e MYSQL_USERNAME={username} MYSQL_ROOT_PASSWORD={password}",
        f'-p {PORT}:80 --name {username} "$USER"/alpine-lamp'
    ]

    delimiter = " "
    COMMAND = delimiter.join(COMMAND_LINES)
    os.system(COMMAND)
