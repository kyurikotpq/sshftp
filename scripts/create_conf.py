def create_conf(subdomain):
    lines = [
        "<VirtualHost *:80>",
        "ServerAdmin webmaster@localhost",
        f"ServerName {subdomain}",
        f"DocumentRoot /var/www/html/{subdomain}/public_html",
        "ErrorLog ${APACHE_LOG_DIR}/error.log",
        "CustomLog ${APACHE_LOG_DIR}/access.log combined",
        "</VirtualHost>"
    ]
    delimiter = "\n"
    return delimiter.join(lines)
