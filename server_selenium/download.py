import paramiko
import datetime


def remote_scp(host_ip, remote_path, local_path, username, password):
    t = paramiko.Transport((host_ip, 22))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    start_time = datetime.datetime.now()
    src = remote_path
    des = local_path
    sftp.get(src, des)
    t.close()
    end_time = datetime.datetime.now()
    c = 58 / (end_time - start_time).seconds
    print('下载速度为:{}M/s'.format(c))

if __name__ == '__main__':
    host_ip = '192.168.1.115'
    remote_path = '/home/ifarm-lcc-exec.jar'
    local_path = r'c:\Users\a\ifarm-lcc-exec.jar'
    username = 'root'
    password = '123456'
    remote_scp(host_ip, remote_path, local_path, username, password)