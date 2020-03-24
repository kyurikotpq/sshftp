def create_conf(subdomain, port):
    lines = [
        "<VirtualHost *:80>",
        "ServerAdmin webmaster@localhost",
        f"ServerName {subdomain}",

        "ProxyPreserveHost On",
        f"ProxyPass / http://localhost:{port}/",
        f"ProxyPassReverse / http://localhost:{port}/",

        "ErrorLog ${APACHE_LOG_DIR}/error.log",
        "CustomLog ${APACHE_LOG_DIR}/access.log combined",
        "</VirtualHost>"
    ]
    delimiter = "\n"
    return delimiter.join(lines)
