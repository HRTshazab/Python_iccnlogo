import paramiko
import getpass
import time

sshcli = paramiko.SSHClient()
sshcli.load_system_host_keys()
sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ipaddr = input('Enter the IP address of the host: ')
print('Logging in as root...')
time.sleep(1)
pswd = getpass.getpass('Enter the root password: ')
print('\n')

print(f'Connecting to {ipaddr}...')
sshcli.connect(hostname=ipaddr, port=22, username='root', password=pswd, look_for_keys=False, allow_agent=False)
time.sleep(2)

shell = sshcli.invoke_shell()
print('Connected!!!')
time.sleep(1)
print('\n')

with open('commands.txt') as f:
    commands = f.read().splitlines()

print(f'Changes taking place on {ipaddr}, Please wait...')
for cmnd in commands:
    shell.send(cmnd + '\n')
    time.sleep(2)

out = shell.recv(10000)

shell.send('ls /usr/local/opnsense/www/themes/tukan/build/images/' + '\n')
time.sleep(2)
output = shell.recv(10000)
print('\n')
print('#' * 100)
if 'iccn' in output.decode():
    print('Changes have been made! Please refresh your GUI and/or clear the cache on your browser.')
else:
    print("Changes haven't been made!!! Please try again.")

if sshcli.get_transport().is_active():
    print('Closing connection...')
    sshcli.close()
