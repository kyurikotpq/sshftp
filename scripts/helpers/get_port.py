from subprocess import call


# Get a not-used port from 50000:60000
def get_port():
    count = 50000
    netstat = call(f"sudo netstat -ntlp | grep {count}", shell=True)

    while netstat != 1:
        count += 1
        netstat = call(f"sudo netstat -ntlp | grep {count}", shell=True)
        
        if(count == 50300):
            count = -1
            break

    return count
