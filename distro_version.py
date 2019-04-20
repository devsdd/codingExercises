
import os

def ubuntu_release():

    distro = {}

    with open('/etc/lsb-release') as f:
        lines = f.readlines()

    for line in lines:
        if "DISTRIB_ID" in line:
            os = line.split('=')[1]
        elif "DISTRIB_CODENAME" in line:
            release = line.split('=')[1]

    distro["os"] = os
    distro["release"] = release

    return distro

if __name__ == "__main__":
    if os.path.isfile('/etc/redhat-release'):
        distro = redhat_release()
    elif os.path.isfile('/etc/lsb-release'):
        distro = ubuntu_release()

    for key, value in distro.items():
        print(key + ": " + value)