#!/usr/bin/python

'''
Problem Statement:

Given a apache log :

A) Find all client IP addresses.
B) Count the number of pages requested by each individual client.
C) Find all the unique status code returned by the server and count of each status code.
D) Print only the User agents .
'''

import argparse

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logfile", required=True, help="/path/to/apache/access_log")
    args = parser.parse_args()

    logfile = args.logfile

    return logfile


def get_unique_client_ips(lines):

    ips = []

    for line in lines:
        ip = line.split()[0]
        if ip not in ips:
            ips.append(ip)

    return ips


def page_count(lines):
    all_ips = []
    pages_per_client = {}
    count = 0
    unique_ips = get_unique_client_ips(lines)

    for line in lines:
        ip = line.split()[0]
        if ip not in pages_per_client:
            pages_per_client[ip] = 1
        else:
            count = pages_per_client[ip]
            count += 1
            pages_per_client[ip] = count

    return pages_per_client


def unique_status_codes(lines):
    unique_codes = []

    for line in lines:
        code = line.split()[8]
        if code not in unique_codes:
            unique_codes.append(code)

    return unique_codes


def code_count(lines):
    all_codes = []
    count_per_code = {}
    count = 0
    unique_codes = unique_status_codes(lines)

    for line in lines:
        code = line.split()[8]
        if code not in count_per_code:
            count_per_code[code] = 1
        else:
            count = count_per_code[code]
            count += 1
            count_per_code[code] = count

    return count_per_code


def user_agents(lines):
    agents = []

    for line in lines:
        code = line.split()[11]
        if code not in agents:
            agents.append(code)

    return agents

if __name__ == "__main__":

    apache_logfile = parse_command_line()
    with open(apache_logfile) as f:
        lines_in_file = f.readlines()

    # all_client_ips = get_unique_client_ips(lines_in_file)
    # print("Unique client IPs:")
    # for ip in all_client_ips:
    #     print(ip)

    # print("Pages requested per client:")
    # pages_per_client = page_count(lines_in_file)
    #
    # for key,value in pages_per_client.items():
    #     print(key + ": " + str(value))

    # print("Unique status codes: ")
    # unique_codes = unique_status_codes(lines_in_file)
    # print(unique_codes)

    # print("Status codes by count:")
    # codes_by_count = code_count(lines_in_file)
    #
    # for key,value in codes_by_count.items():
    #     print(key + ": " + str(value))

    print("Unique user agents: ")
    agents = user_agents(lines_in_file)
    print(agents)