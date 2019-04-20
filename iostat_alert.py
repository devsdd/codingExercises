'''
Problem statement:
* Check the output of iostat and alert if writes per second breaches the threshold of 100
'''

import subprocess

output = subprocess.Popen(['iostat', '-dmx', '/dev/sda'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout,stderr = output.communicate()
out = float(stdout.split()[28].decode('utf-8'))

if out > 10:
    print("Alert! Writes per sec = %.2f" % out)