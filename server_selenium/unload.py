import paramiko
import datetime
import os

def upload_server(local_dir, remote_dir):
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        start_time = datetime.datetime.now()
        print('upload file start')
        for root, dirs, files in os.walk(local_dir):
            print('[%s][%s][%s]' % (root, dirs, files))
            for filespath in files:
                local_file = os.path.join(root, filespath)
                print(11, '[%s][%s][%s][%s]' % (root, filespath, local_file, local_dir))
                a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                print('01', a, '[%s]' % remote_dir)
                remote_file = os.path.join(remote_dir, a)
                print(22, remote_file)
                try:
                    sftp.put(local_file, remote_file)
                except Exception as e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file, remote_file)
                    print("66 upload %s to remote %s" % (local_file, remote_file))
            for name in dirs:
                local_path = os.path.join(root, name)
                print(0, local_path, local_dir)
                a = local_path.replace(local_dir, '').replace('\\', '/').lstrip('/')
                print(1, a)
                print(1, remote_dir)
                remote_path = os.path.join(remote_dir, a)
                print(33, remote_path)
                try:
                    sftp.mkdir(remote_path)
                    print(44, "mkdir path %s" % remote_path)
                except Exception as e:
                    print(55, e)
        end_time = datetime.datetime.now()
        print('77,upload file success')
        upload_speed = 907 / (end_time - start_time).seconds
        print('文件上传速度为{}M/s'.format(upload_speed))
        t.close()
    except Exception as e:
        print(88, e)


if __name__ == '__main__':
    hostname = '192.168.1.115'
    username = 'root'
    password = '123456'
    port = 22
    local_dir = r'c:\wps'
    remote_dir = '/home/wps'
    upload_server(local_dir, remote_dir)