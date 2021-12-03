from netmiko import ConnectHandler

with open('devices.txt') as f:
    devices = f.read().splitlines()

for ip in devices:

    cisco_device = {
           'device_type': 'cisco_ios',
           'host': ip,
           'username': 'u1',
           'password': 'cisco',
           'port': 22,             # optional, default 22
           'secret': 'cisco',      # this is the enable password
           'verbose': True         # optional, default False
           }
    connection = ConnectHandler(**cisco_device)
    print('Entering the enable mode...')
    connection.enable()

    output = connection.send_command('show run')
    # print(output)

    # creating the backup filename (hostname_date_backup.txt)
    prompt = connection.find_prompt()
    hostname = prompt[0:-1]
    # print(hostname)

    # getting the current date (year-month-day)
    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    # creating the backup filename (hostname_date_backup.txt)
    filename = f'{hostname}_{year}-{month}-{day}_backup.txt'

    # writing the backup to the file
    with open(filename, 'w') as backup:
        backup.write(output)
        print(f'Backup of {hostname} completed successfully')
        print('#' * 30)


    print('Closing connection')
    connection.disconnect()