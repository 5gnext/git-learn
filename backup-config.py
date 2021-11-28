import paramiko
import time
import threading
def connect(server_ip, server_port, user, passwd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'connecting to {server_ip}')
    ssh_client.connect(hostname=server_ip, port=server_port, username=user, password=passwd, look_for_keys=False,
                       allow_agent=False)
    return ssh_client

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command, timeout=1):
    print(f'sending command: {command}')
    shell.send(command +'\n')
    time.sleep(timeout)

def show(shell, n=100000):
    output = shell.recv(n)
    return output.decode()

def backup(router):
    client = connect(**router)
    shell = get_shell(client)
    send_command(shell,'term len 0')
    send_command(shell,'enable')
    send_command(shell,'cisco')
    send_command(shell,'show run')
    time.sleep(15)
    output = show(shell)
    output_list = output.splitlines()
    output_list = output_list[18:-1]
    output = '\n'.join(output_list)
    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    file_name = f'{router["server_ip"]}_{year}-{month}-{day}-{hour}-{minute}'
    # print(output)

    f = open(file_name, 'w')
    f.write(output)
def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:
        print('closing connection')
        ssh_client.close()
if __name__ == '__main__':
    router1 = {'server_ip': '10.1.1.1', 'server_port': '22', 'user':'admin', 'passwd':'admin'}
    router2 = {'server_ip': '10.1.1.3', 'server_port': '22', 'user':'admin', 'passwd':'admin'}
    routers = [router1, router2]
    threads = list()
    for router in routers:
        th = threading.Thread(target=backup, args=(router,))
        threads.append(th)
    for th in threads:
        th.start()
    for th in threads:
        th.join()