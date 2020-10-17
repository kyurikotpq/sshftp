import os

# Create a new container for the user :)
def create_docker(CHROOT_DIR, PORT, username, password):
    COMMAND_LINES = [
        f"sudo docker run -d -v {CHROOT_DIR}/html:/var/www/localhost/htdocs/",
        f"-e USERNAME={username} -e MYSQL_ROOT_PASSWORD={password}",
        f"--restart always",
        f'-p {PORT}:80 --name {username} kyurikotpq/lampm2'
    ]

    delimiter = " "
    COMMAND = delimiter.join(COMMAND_LINES)

    os.system(COMMAND)
    
    return True
