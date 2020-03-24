import os


# Get a not-used port from 50000:60000
def get_port():
    count = 50000
    netstat = os.system(f"sudo netstat -ntlp | grep {count}")

    while not netstat:
        netstat = os.system(f"sudo netstat -ntlp | grep {count}")
        count += 1

        if(count == 50300):
            count = -1
            break

    return count
