from netmiko import ConnectHandler

# reading the devices ip address from a file into a list (each ip on its own line)
with open('devices.txt') as f:
   devices = f.read().splitlines()

device_list = list()

# iterating over the list with the devices ip addresses
for ip in devices:
   cisco_device = {
           'device_type': 'cisco_ios',
           'host': ip,
           'username': 'u1',
           'password': 'cisco',
           'port': 22,
           'secret': 'cisco', #this is the enable password
           'verbose': True
           }
   device_list.append(cisco_device)

# print(device_list)

for device in device_list:
    connection = ConnectHandler(**device)

    print('Entering the enable mode ...')
    connection.enable()

    # prompting the user for a config file
    file = input(f'Enter a configuration file (use a valid path) for {device["host"]}:')

    print(f'Running commands from file: {file} on device: {device["host"]}')
    output = connection.send_config_from_file(file)
    print(output)

    print(f'Closing connection to {cisco_device["host"]}')
    connection.disconnect()

    print('#' * 30)

