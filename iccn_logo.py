import paramiko
import getpass
import time

sshcli = paramiko.SSHClient()
sshcli.load_system_host_keys()
sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ipaddr = input('Enter the IP address of the host: ')
# user = input('Enter the username: ')
print('Logging in as root...')
time.sleep(1)
pswd = getpass.getpass('Enter the root password: ')
print('\n')

print(f'Connecting to {ipaddr}...')
sshcli.connect(hostname=ipaddr, port=22, username='root', password=pswd, look_for_keys=False, allow_agent=False)
time.sleep(2)

# print('Invoking Shell!!!')
shell = sshcli.invoke_shell()

print('Connected!!!')
print('\n')

commands = ('8', 'git clone https://github.com/Fuzail98/iccn-theme.git',
            'cd iccn-theme/', 'cp *.* /usr/local/opnsense/www/themes/tukan/build/images/', 'cd ..', 'rm -r iccn-theme/')

print(f'Changes taking place on {ipaddr}, Please wait...')
for cmnd in commands:
    # print(f'Sending Command: {cmnd}')
    shell.send(cmnd + '\n')
    time.sleep(2)

output = shell.recv(10000)
out = output.decode()
# print(out)

if sshcli.get_transport().is_active():
    # print('Closing Connection!!!')
    # print('\n')
    sshcli.close()

print('#' * 100)
print('\n')
print('Changes have been made! Please refresh your GUI and/or clear the cache on your browser.')
