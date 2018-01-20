
'''
The challenge:

You have 10 servers.
You need to deploy 1000 web apps onto in between these 10 servers.
Assume the deployment process is

deploy <appname> free ip free port

Write a program to find free ports available on free ips to deploy the app.

Log all the details to a log file.
See the use of various log levels.
'''

import argparse
import sys
import os
import re

# TODO: LOG ALL ERRORS
def parse_command_line():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help="File containing list of IPs to scan for deployment")
    args = parser.parse_args()

    if(len(sys.argv) != 3):
        parser.print_help()
        sys.exit(1)

    fileName = args.file
    return fileName

# takes a file as input and checks if it contains one IP per line. Returns a list of IP's if file contents are valid
def extract_IPs(fileName):

    lines = []

    if(os.path.getsize(fileName) <= 0):
        raise Exception("File which should contain list of servers is empty...")

    try:
        with open(fileName, 'r') as f:
            lines = f.readlines()
    except:
        # LOG exception
        raise

    for line in lines:
        if(line == '\n'):
            raise Exception("No blank lines allowed in list of IPs")

        temp = line.split()
        if (len(temp) != 1):
            raise Exception("File must contain exactly one IP per line")

        # NOTE: this is not a perfect regex but the idea is to do a basic check for extra dots, spaces etc.
        # this will pass something like 999.999.999.999 which is obviously an invalid IP but,
        # We trade some accuracy off against simplicity
        searchObj = re.search(r'^(\d{1,3}\.){3}\d{1,3}$', line)
        if not searchObj:
            raise Exception(line + " is not a valid IPv4 address")

    return lines


if __name__ == "__main__":

    serversFile = parse_command_line()
    ips = extract_IPs(serversFile)
#    print(ips)
