# https://community.ui.com/questions/Unifi-Python-API/4c58d69c-3278-4b61-86fd-7b497c70c102
# https://lazyadmin.nl/home-network/unifi-ssh-commands/
# https://pysnmp.readthedocs.io/en/latest/

""" 
https://community.ui.com/questions/Power-Cycle-POE-port-on-UniFi-Switch-remotely-/f14675bd-85ae-41de-a524-5ffdfcdca7bf
https://community.home-assistant.io/t/unifi-provide-switches-for-poe-ports/30256
https://github.com/chenkaie/Tools/blob/master/ubnt-unifi-switch-poe-on-off.sh
https://www.youtube.com/watch?v=VQHQlMX5Nzo


IP_ADDRESS_OF_POE_SWITCH=$(arp -a | grep 'd8:b3:70:1e:27:18' | awk '{print $2}' | sed 's/^[()]//; s/[()]$//')

ssh USERNAME_UNIFI_USW_ENTERPRISE_24_POE@"$IP_ADDRESS_OF_POE_SWITCH"
telnet localhost 23
enable
configure
interface 0/x  poe opmode shutdown poe opmode auto 
import subprocess
subprocess.call(['python3', 'pagekite.py', '8080', f'{homeName}.pagekite.me'])
#'(echo "enable" ; echo "configure" ; echo "interface '0/7'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'

<cr>                     Press enter to execute the command.
<3000-64000>             Configure PoE port power limit(mW).

(UBNT) (Interface 0/10)#poe power limit user-defined

(UBNT) (Interface 0/10)#show poe port configuration 0/10

(UBNT) (Interface 0/10)#show poe port info 0/10

(UBNT) (Interface 0/10)#poe priority High  ??? WILL THIS SPEED UP poe opmode auto ???
"""
import paramiko
from dotenv import dotenv_values

unifiEnvironmentVariables = dotenv_values()
userNAme = unifiEnvironmentVariables['USERNAME_UNIFI_USW_ENTERPRISE_24_POE']
pw = unifiEnvironmentVariables['PASSWORD_UNIFI_USW_ENTERPRISE_24_POE']
    
# Establish SSH connection 
# https://help.ui.com/hc/en-us/articles/204909374-UniFi-Connect-with-SSH-Advanced
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.100.120', username=userNAme, password=pw)

# Telnet command
telnet_command = '(echo "enable" ; echo "configure" ; echo "interface \'0/10\'" ; echo "poe opmode on" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'

# Execute the command
stdin, stdout, stderr = ssh.exec_command(telnet_command)

# Print the output
output = stdout.read().decode()
print(output)

# Close the SSH connection
ssh.close()