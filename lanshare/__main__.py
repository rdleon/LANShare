#!/usr/bin/env python

import os, sys, socket, socketserver
from os.path import isfile, join
from zeroconf import ServiceInfo, ServiceBrowser, ServiceStateChange, Zeroconf
from time import sleep
from lanshare.conf import __version__
from lanshare.discover import get_hosts, browse_host
from lanshare.server import serve_files

def list_hosts():
    """
    Scans the network for LANShare hosts and prints them to stdout.
    """
    hosts = get_hosts()
    for host in hosts:
        print(host)

def list_files(hostname):
    """
    Asks a host for a list of it's shared files and prints them to stdout.
    """
    files = browse_host(hostname)

    for filename in files:
        print(filename)


def download_file(host, port, filename, output):
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f = open(output, 'wb')

    try:
         # Connect to server and request list of files
        sock.connect((host, port))
        command = "GET {0}".format(filename)
        sock.sendall(command.encode('utf-8'))
        buff = sock.recv(1024)
        if buff[0:1] == b'3':
            i = buff.index(b"\n")
            if i > 0:
                buff = buff[i+1:]
# check the size of the buffer, if the buffer isn't full, stop.
                while buff:
                    f.write(buff)
                    buff = sock.recv(1024)
            else:
                print('Error getting file')
        else:
            print('Error getting file:', buff)
    finally:
        f.close()
        sock.close()

def get_file(hostname, filename, output=None):
    """
    Gets a filename from hostname and save it as output.
    """
    zeroconf = Zeroconf()
    fqdn = '{0}.local.'.format(hostname)
    finish = False

    if output is None:
        output = filename

    def find_host(zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            host = zeroconf.get_service_info(service_type, name)
            if host is not None and host.server == fqdn:
                download_file(socket.inet_ntoa(host.address), host.port, filename, output)
                print('finished downloading')

    browser = ServiceBrowser(zeroconf,
                    '_lanshare._tcp.local.',
                   handlers=[find_host])

def usage():
    """
    Print the help message
    """
    print("lanshare help...")
    print("  lanshare -h                       - Show this message")
    print("  lanshare -v                       - Print version info and exit")
    print("  lanshare                          - List hosts")
    print("  lanshare <host>                   - List files on hosts")
    print("  lanshare <host> <file> [<output>] - List files on hosts")
    print("  lanshare -S [<dir>]               - Serve directory to the LAN")

def parse_options(args):
    """
    Read the command line options and call the related function.
    + Serve files
    + List available hosts
    + List files on a host
    + Get a file from a host
    """
    if len(args) == 1:
        list_hosts()
    elif args[1] == "-v" or args[1] == "--version":
        print("lanshare v{}".format(__version__))
    elif args[1] == "-S":
        if len(sys.argv) > 2:
            serve_files(args[2])
        else:
            serve_files()
    elif args[1] == "-h" or args[1] == "--help":
        usage()
    elif len(args) == 2:
        list_files(args[1])
    else:
        if len(args) == 3:
            get_file(args[1], args[2])
        else:
            get_file(args[1], args[2], args[3])

def main():
    parse_options(sys.argv)

if __name__ == "__main__":
    main()

