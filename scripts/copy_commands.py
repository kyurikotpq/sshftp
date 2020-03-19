# THIS CAN BE RUN INDIVIDUALLY ON THE SHELL (TBC)
# OR IMPORTED IN ANOTHER PYTHON SCRIPT AND RUN
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

    # copy command dependency libraries
    if not path.exists(f"/home/{username}/ftp/lib"):
        os.system(f"sudo mkdir /home/{username}/ftp/lib")

    if not path.exists(f"/home/{username}/ftp/lib64"):
        os.system(f"sudo mkdir /home/{username}/ftp/lib64")


    for lib_path in bash_commands.BASH_LIB:
        os.system(f"sudo cp -v {lib_path} /home/{username}/ftp/lib")

    for lib_path in bash_commands.BASH_LIB64:
        os.system(f"sudo cp -v {lib_path} /home/{username}/ftp/lib64")

# check if params are given
# if len(sys.argv) < 2:
#     sys.exit("Usage: `python ./scripts/copy-commands.py <username>` (navigate to root directory first)")

# # Extract params
# username = sys.argv[1]
# copy_commands(username)