'''
Problem Statement:

Get SMART data for a disk (read it from the given file) and return healthy/unhealthy status by checking if RAW_VALUE of attributes breach thresholds.

Smartctl Sample Output:

smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.16.0-23-generic] (local build)
Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x002f   200   200   051    Pre-fail  Always       -       0
  3 Spin_Up_Time            0x0027   100   253   021    Pre-fail  Always       -       0
  4 Start_Stop_Count        0x0032   100   100   000    Old_age   Always       -       1
  5 Reallocated_Sector_Ct   0x0033   200   200   140    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x002e   100   253   000    Old_age   Always       -       0
  9 Power_On_Hours          0x0032   084   084   000    Old_age   Always       -       11842
 10 Spin_Retry_Count        0x0032   100   253   000    Old_age   Always       -       0
 11 Calibration_Retry_Count 0x0032   100   253   000    Old_age   Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       1
 16 Unknown_Attribute       0x0022   002   198   000    Old_age   Always       -       141618575960
183 Runtime_Bad_Block       0x0032   100   100   000    Old_age   Always       -       0
192 Power-Off_Retract_Count 0x0032   200   200   000    Old_age   Always       -       0
193 Load_Cycle_Count        0x0032   200   200   000    Old_age   Always       -       1
194 Temperature_Celsius     0x0022   122   120   000    Old_age   Always       -       30 (Min/Max 24/32)
196 Reallocated_Event_Count 0x0032   200   200   000    Old_age   Always       -       0
197 Current_Pending_Sector  0x0032   200   200   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0030   200   200   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x0032   200   200   000    Old_age   Always       -       0
200 Multi_Zone_Error_Rate   0x0008   200   200   000    Old_age   Offline      -       0
241 Total_LBAs_Written      0x0032   200   200   000    Old_age   Always       -       61307357692
242 Total_LBAs_Read         0x0032   200   200   000    Old_age   Always       -       80311218268



Attributes and thresholds are provided in a config file:
Reallocated_Sector_Ct: 100
Seek_Error_Rate: 200
Current_Pending_Sector: 200
Offline_Uncorrectable: 150


Watch out:
- Ensure that the program/script is modular, easy to reconfigure the thresholds/attributes, easy to extend to a future uses.
- Periodically send the row values of critical attributes to a remote service to get a time series.
'''

import argparse
import yaml
import subprocess
import io
import json
import pprint


def read_config(configfile):

    with open(configfile) as f:
        config = yaml.safe_load(f)

    return config


def get_stats(command, config):

    result = {}

    command_list = command.split()
    output = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # stdout, stderr = output.communicate()
    for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):

        for key, value in config.items():
            if key in line:
                current_val = int(line.split()[-1:][0])
                result[key] = current_val
                if (current_val > value):
                    print("Alert! %s has exceeded threshold %d. Current value: %d" % (key, value , current_val))

    temp = json.dumps(result)
    result_json = json.loads(temp)
    return result_json


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', required=True, help="full command with args enclosed in quotes")
    parser.add_argument('-f', '--file', required=True, help="/path/to/configfile.yaml")
    args = parser.parse_args()

    config = read_config(args.file)

    stats = get_stats(args.command, config)
    print(json.dumps(stats, indent=4, sort_keys=True))
