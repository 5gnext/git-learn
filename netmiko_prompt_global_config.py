from netmiko import ConnectHandler
cisco_device = {
       'device_type': 'cisco_ios',     #device type from https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py
       'host': '10.1.1.1',
       'username': 'admin',
       'password': 'admin',
       'port': 22,             # optional, default 22
       'secret': 'cisco',      # this is the enable password
       'verbose': True         # optional, default False
       }
connection = ConnectHandler(**cisco_device)

# getting the router's prompt
prompt = connection.find_prompt()
if '>' in prompt:
       connection.enable()   # entering the enable mode

output = connection.send_command('sh run')
print(output)

if not connection.check_config_mode(): # returns True if it's already in the global config mode
       connection.config_mode()  # entering the global config mode

print(connection.check_config_mode())
connection.send_command('username u3 secret cisco')

connection.exit_config_mode()  # exiting the global config mode
print(connection.check_config_mode())

print('Closing connection')
connection.disconnect()