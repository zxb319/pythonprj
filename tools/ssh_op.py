import paramiko


class SshAgent:
    def __init__(self, ip='192.168.1.4', user='zxb', pwd='zxb319', port=22):
        self.ip=ip
        self.port=port
        self.user=user
        self._pwd=pwd

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, port, user, pwd)
        a, b, c = self.ssh.exec_command('pwd')
        self.cur_path = b.read().decode().strip()

        self.sftp=self.ssh.open_sftp()


    def exec(self, cmd):
        cmd=cmd.strip()
        if not cmd:
            return ''
        new_cmd=rf'cd {self.cur_path};{cmd};echo;pwd'
        a, b, c = self.ssh.exec_command(new_cmd)
        # print('test:',cmd,b.read().decode())
        ret=b.read().decode().strip('\n').split('\n')
        # print('test:',ret)
        self.cur_path=ret[-1]

        ret='\n'.join(ret[:-1]).strip()

        cret=c.read().decode()
        if cret:
            return cret

        return ret+'\n' if ret else ret


    def stat(self,fp):
        return self.sftp.listdir_attr(fp)


def main():
    # user = input('login as:')
    # pwd = input('password:')
    ssh=SshAgent()

    while True:
        prefix=rf'{ssh.user}@{ssh.ip} {ssh.cur_path}>>:'
        b = ssh.exec(input(prefix))
        print(b,end='')

if __name__ == '__main__':
    ssh=SshAgent()
    a=ssh.stat(rf'D:\weiyun')
    print(*a,sep='\n')