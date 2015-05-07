#!/usr/bin/env python
#encoding: utf-8
#author: zengqiu

import os, re, sys, socket, struct, time

def ip_check(ip):
    ip_int_start = struct.unpack('!L', socket.inet_aton('1.0.0.0'))[0]
    ip_int_end = struct.unpack('!L', socket.inet_aton('255.255.255.255'))[0]
    
    try:
        ip_int = struct.unpack('!L', socket.inet_aton(ip))[0]
    except Exception, e:
        print 'Please enter the right ip address'
        sys.exit()

    return ip_int

def ip_generate(ip_start, ip_end):
    ip_int_start = ip_check(ip_start)
    ip_int_end = ip_check(ip_end)

    if (ip_int_start < ip_int_end):
        filename = 'ip_list.txt'
        if os.path.isfile(filename):
            os.rename(filename, filename + '_' + time.strftime('%Y%m%d%H%M', time.localtime()))
        
        ip_list = open(filename, 'a')
        ip_int = ip_int_start
        
        while ip_int <= ip_int_end:
            ip = socket.inet_ntoa(struct.pack('!L', ip_int))
            ip_list.write(ip + '\n')
            ip_int = ip_int + 1

        ip_list.close()
    else:
        print 'Please enter the ip address with a right order'
        sys.exit()

# Generate all IP address
def ip_generate_all():
    ip_generate('1.0.0.0', '255.255.255.255')

# Generate outside IP address
def ip_generate_outside():
    # A
    ip_generate('1.0.0.0', '9.255.255.255')
    ip_generate('11.0.0.0', '126.255.255.255')
	# B
    ip_generate('128.0.0.0', '172.15.255.255')
    ip_generate('172.32.0.0', '191.255.255.255')
    # C
    ip_generate('192.0.0.0', '192.167.255.255')
    ip_generate('192.169.0.0', '223.255.255.255')

# Generate inside IP address
def ip_generate_inside():
    # A
    ip_generate('10.0.0.0', '10.255.255.255')
    # B
    ip_generate('172.16.0.0', '172.31.255.255')
    # C
    ip_generate('192.168.0.0', '192.168.255.255')

def main():
    print 'Please ./ip_generate ip_start ip_end'
    ip_generate(sys.argv[1], sys.argv[2])
    print 'Generate ip list successed'

if __name__ == '__main__':
    main()