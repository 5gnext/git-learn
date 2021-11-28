import paramiko
import time

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

def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:
        print('closing connection')
        ssh_client.close()
if __name__ == '__main__':
    router1 = {'server_ip': '10.1.1.1', 'server_port': '22', 'user':'admin', 'passwd':'admin'}
    client = connect(**router1)
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
    print(output)
    f = open('r1-config-backup.txt', 'w')
    f.write(output)