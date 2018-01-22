
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
import json
from multiprocessing import Pool

def parse_command_line():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help="File containing list of IPs to scan for deployment")
    args = parser.parse_args()

    fileName = args.file
    return fileName

def log(status, message, section):

    logger = logging.getLogger(section)
    handler = logging.FileHandler("app_orchestrator.log")

    # make the log formatter as per our needs: timestamp, section of this program where log was generated, syslog level, and msg
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: "%(message)s"', datefmt="%Y-%m-%d %H:%M:%S")

    handler.formatter = formatter
    logger.addHandler(handler)

    if status == "ERR":
        logger.error(message)
    elif status == "CRIT":
        logger.critical(message)
    elif status == "SUCCESS":
        logger.info(message)

    return

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

        # NOTE: this is not a perfect regex for an IPv4 address but the idea is to do a basic check for obviously invalid characters
        # this will pass something like 999.999.999.999 which is obviously an invalid IP but,
        # We trade some accuracy off against simplicity
        searchObj = re.search(r'^(\d{1,3}\.){3}\d{1,3}$', line)
        if not searchObj:
            errorMsg = line.rstrip("\n") + " is not a valid IPv4 address"
            log("CRIT", errorMsg, "InputFile")
            raise Exception(errorMsg)

    return lines

def scan_IPs(ips):

    freeDict = {}
    # Let's not mess with privileged ports, let's find 100 non-privileged ports per machine
    targetPortsRange = [x for x in range(1025,1124)]

    # this will serially iterate thru all the ips, can this be made parallel
    for ip in ips:
        # ignore comments
        if(ip.startswith("#")):
            continue

        nm = nmap.PortScanner()
        try: 
	    # vijay - this section is blocking and will add delay if we have 100 ips. can this be made async?
            nm.scan(ip, '1025-1124')
        except:
            log("ERR", "Ports scan failed for %s" %ip.rstrip('\n'), "Scan" )
            raise
        else:
            log("SUCCESS", "Ports scan finished successfully for %s" %ip.rstrip('\n'), "Scan" )

        count = 0
        for host in nm.all_hosts():
            if nm[host].all_protocols():
                # at least one port in the list was occupied
                takenPortsList = nm[host]['tcp'].keys()
                freePortsList = [x for x in targetPortsRange if x not in takenPortsList]
            else:
                # all ports in the list were free
                freePortsList = targetPortsRange

	    freeDict[ip.rstrip('\n')] = freePortsList
            count += 1

    return freeDict

# global vars to persist across parallel function calls
resultDict = {}
targetPortsRange = [x for x in range(1025,1124)]

def scan_IP(ip):

    # ignore comments
    if(ip.startswith("#")):
        return

    nm = nmap.PortScanner()
    try: 
        nm.scan(ip, '1025-1124')
    except:
        log("ERR", "Ports scan failed for %s" %ip.rstrip('\n'), "Scan" )
        raise
    else:
        log("SUCCESS", "Ports scan finished successfully for %s" %ip.rstrip('\n'), "Scan" )

    count = 0
    for host in nm.all_hosts():
        if nm[host].all_protocols():
            # at least one port in the list was occupied
            takenPortsList = nm[host]['tcp'].keys()
            freePortsList = [x for x in targetPortsRange if x not in takenPortsList]
        else:
            # all ports in the list were free
            freePortsList = targetPortsRange

        resultDict[ip.rstrip('\n')] = freePortsList
        count += 1

    return resultDict

def get_cpu_cores():

    count = 0
    for line in open("/proc/cpuinfo"):
        if "processor" in line:
            count += 1

    return count

if __name__ == "__main__":

    serversFile = parse_command_line()
    ips = extract_IPs(serversFile)
    cores = get_cpu_cores()
#    freePorts = scan_IPs(ips)
    pool = Pool(processes=cores)

    freePorts = pool.map(scan_IP, ips)
    output = json.dumps(freePorts, indent=4, sort_keys=True)
    with open("result.json", "w") as f:
        f.write(output)

