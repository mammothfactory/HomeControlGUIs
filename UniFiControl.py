# https://community.ui.com/questions/Unifi-Python-API/4c58d69c-3278-4b61-86fd-7b497c70c102
# https://lazyadmin.nl/home-network/unifi-ssh-commands/

""" 
https://community.ui.com/questions/Power-Cycle-POE-port-on-UniFi-Switch-remotely-/f14675bd-85ae-41de-a524-5ffdfcdca7bf
ssh USERNAME_UNIFI_USW_ENTERPRISE_24_POE@192.168.3.2 
telnet localhost 23
enable
configure
interface 0/x  poe opmode shutdownpoe opmode auto 
import subprocess
subprocess.call(['python3', 'pagekite.py', '8080', f'{homeName}.pagekite.me'])
#'(echo "enable" ; echo "configure" ; echo "interface '0/7'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
"""

import paramiko
from dotenv import dotenv_values

unifiEnvironmentVariables = dotenv_values()
userNAme = unifiEnvironmentVariables['USERNAME_UNIFI_USW_ENTERPRISE_24_POE']
pw = unifiEnvironmentVariables['PASSWORD_UNIFI_USW_ENTERPRISE_24_POE']
    
# Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.3.2', username=userNAme, password=pw)

# Telnet command
telnet_command = '(echo "enable" ; echo "configure" ; echo "interface \'0/10\'" ; echo "poe opmode on" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'

# Execute the command
stdin, stdout, stderr = ssh.exec_command(telnet_command)

# Print the output
output = stdout.read().decode()
print(output)

# Close the SSH connection
ssh.close()


"""

import requests
import json
from pprint import pprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# set up connection parameters in a dictionary
gateway = {"ip": "192.168.3.2", "port": "8443"}

# set REST API headers
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
# set URL parameters
loginUrl = 'api/login'
url = f"https://{gateway['ip']}:{gateway['port']}/{loginUrl}"
# set username and password
body = {
    "username": "ubnt",
    "password": "ubnt"
}
# Open a session for capturing cookies
session = requests.Session()
# login
response = session.post(url, headers=headers,
                        data=json.dumps(body), verify=False)

# parse response data into a Python object
api_data = response.json()
print("/" * 50)
pprint(api_data)
print('Logged in!')
print("/" * 50)

# Set up to get site name
getSitesUrl = 'api/self/sites'
url = f"https://{gateway['ip']}:{gateway['port']}/{getSitesUrl}"
response = session.get(url, headers=headers,
                       verify=False)
api_data = response.json()
# print("/" * 50)
# pprint(api_data)
# print("/" * 50)

# Parse out the resulting list of
responseList = api_data['data']
# pprint(responseList)
n = 'name'
for items in responseList:
    if items.get('desc') == 'Knox-Home':
        n = items.get('name')
# print(n)

getDevicesUrl = f"api/s/{n}/stat/device"
url = f"https://{gateway['ip']}:{gateway['port']}/{getDevicesUrl}"
response = session.get(url, headers=headers,
                       verify=False)
api_data = response.json()
responseList = api_data['data']
print('DEVICE LIST AND STATUS')
for device in responseList:
    print(f"The device {device['name']} has IP {device['ip']}")
    print(f"MAC:            {device['mac']}")
    print(f"DHCP?:          {device['config_network']['type']}")
    if device['state'] == 1:
        print('State:          online')
    else:
        print('State:          offline')
    print(f"Upgradable?     {device['upgradable']}")
    print(' ')
"""