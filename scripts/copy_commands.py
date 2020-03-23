import os
from os import path
import sys
import bash_commands

# username: Linux Username of the user
def copy_commands(username):
    # copy command executables
    if not path.exists(f"/home/{username}/ftp/bin"):
        os.system(f"sudo mkdir /home/{username}/ftp/bin/")

    for cmd_path in bash_commands.BASH_COMMANDS:
        os.system(f"sudo cp -v {cmd_path} /home/{username}/ftp/bin/")

    # Create the folders if necessary
    if not path.exists(f"/home/{username}/ftp/lib"):
        os.system(f"sudo mkdir /home/{username}/ftp/lib")

    if not path.exists(f"/home/{username}/ftp/lib64"):
        os.system(f"sudo mkdir /home/{username}/ftp/lib64")

    # copy command dependency libraries
    for lib_path in bash_commands.BASH_LIB:
        os.system(f"sudo cp -v {lib_path} /home/{username}/ftp/lib")

    for lib_path in bash_commands.BASH_LIB64:
        os.system(f"sudo cp -v {lib_path} /home/{username}/ftp/lib64")
