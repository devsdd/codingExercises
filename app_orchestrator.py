
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
import logging
import nmap

# TODO: LOG ALL ERRORS

'''
use CRITICAL for failure to run program, ERROR for run-time errors
logger.error('Failed to open file', exc_info=True)

'''
def log(status, message, operation):

    logger = logging.getLogger(operation)
    handler = logging.FileHandler("app_orchestrator.log")

    #add formatter to the handler
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: "%(message)s"', datefmt="%Y-%m-%d %H:%M:%S")

    handler.formatter = formatter
    logger.addHandler(handler)

    if status == "ERR":
        logger.setLevel(logging.ERROR)
        logger.error(message)
    elif status == "CRIT":
        logger.setLevel(logging.CRITICAL)
        logger.critical(message)
    elif status == "SUCCESS":
        logger.setLevel(logging.INFO)
        logger.info(message)

    return

def parse_command_line():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help="File containing list of IPs to scan for deployment")
    args = parser.parse_args()

    # TODO: check what exceptions argparse throws and catch them
    if(len(sys.argv) != 3):
        parser.print_help()
        sys.exit(1)

    fileName = args.file
    return fileName

# takes a file as input and checks if it contains one IP per line. Returns a list of IP's if file contents are valid
def extract_IPs(fileName):

    lines = []

    if(os.path.getsize(fileName) <= 0):
        errorMsg = "File which should contain list of servers is empty"
        log("CRIT", errorMsg, "InputFile")
        raise Exception(errorMsg)

    try:
        with open(fileName, 'r') as f:
            lines = f.readlines()
    except:
        # LOG exception
        log("CRIT", "Error reading input file", "InputFile")
        raise

    count = 0
    for line in lines:
        count += 1
        if(line == '\n'):
            errorMsg = "Found blank line at line number " + str(count)
            log("CRIT", errorMsg, "InputFile")
            raise Exception(errorMsg)

        # ignore comments
        if(line.startswith("#")):
            continue

        # abort if any line contains more than one whitespace-separated field
        temp = line.split()
        if (len(temp) != 1):
            errorMsg = "File must contain exactly one IP per line"
            log("CRIT", errorMsg, "InputFile")
            raise Exception(errorMsg)

        # NOTE: this is not a perfect regex but the idea is to do a basic check for extra dots, spaces etc.
        # this will pass something like 999.999.999.999 which is obviously an invalid IP but,
        # We trade some accuracy off against simplicity
        searchObj = re.search(r'^(\d{1,3}\.){3}\d{1,3}$', line)
        if not searchObj:
            errorMsg = line.rstrip("\n") + " is not a valid IPv4 address"
            log("CRIT", errorMsg, "InputFile")
            raise Exception(errorMsg)

    return lines

def scan_IPs(ips):

    takenDict = {}
    freeDict = {}
    # Let's not mess with privileged ports, let's find 100 non-privileged ports per machine
    targetPortsRange = [x for x in range(9025,9124)]

    for ip in ips:
        # ignore comments
        if(ip.startswith("#")):
            continue

        nm = nmap.PortScanner()
        try: 
            nm.scan(ip, '9025-9124')
        except:
            log("ERR", "Ports scan failed for %s" %ip.rstrip('\n'), "Scan" )
            raise
        else:
            log("SUCCESS", "Ports scan finished successfully for %s" %ip.rstrip('\n'), "Scan" )

        count = 0
        for host in nm.all_hosts():
            takenPortsList = []
            freePortsList = []

            takenPortsList = nm[host]['tcp'].keys()
            freePortsList = [x for x in targetPortsRange if x not in takenPortsList]
	    freeDict[ip.rstrip('\n')] = freePortsList
            count += 1
    return freeDict

if __name__ == "__main__":

    serversFile = parse_command_line()
    ips = extract_IPs(serversFile)
    freePorts = scan_IPs(ips)
    print(freePorts)

