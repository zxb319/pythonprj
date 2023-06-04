
import paramiko

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.11',22,'zxb','zxb319')
stdin, stdout, stderr = ssh.exec_command("ls")
print(stdout.read().decode())