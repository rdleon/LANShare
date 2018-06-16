#!/usr/bin/env python

import os, sys, socket, socketserver
from os.path import isfile, join
from zeroconf import ServiceInfo, ServiceBrowser, ServiceStateChange, Zeroconf
from time import sleep
from lanshare.conf import __version__

def list_dir(dirname=None):
    file_list = ""

    for file in os.listdir(dirname):
        if file[0] == '.':
            continue

        path = os.path.join(dirname, file)
        if os.path.isfile(path):
            file_list += file
            file_list += "\n"

    return file_list

def serve(dirname=None):
    """
    Register as a zeroconf/Bonjour service and serves files in dirname directory
    if dirname is missing, it serves files from the current working directory.
    """
    # Register with the Zeroconf/Bonjour daemon
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    # Should ask the OS for a port binding to 0
    port = 10108
    desc = {'version': __version__}

    info = ServiceInfo("_lanshare._tcp.local.",
                "{0}._lanshare._tcp.local.".format(hostname),
                socket.inet_aton(ip_addr),
                port, 0, 0,
                desc,
                "{0}.local.".format(hostname))

    zeroconf = Zeroconf()
    print("Press Ctrl-C to stop sharing...")
    zeroconf.register_service(info)

    if dirname is None:
        dirname = os.getcwd()

    class ShareHandler(socketserver.BaseRequestHandler):

        def handle(self):
            command = self.request.recv(1024).strip()
            parts = command.decode('utf-8').split(' ')

            if parts[0] == 'LIST':
                list_str = list_dir(dirname)
                message = "2 listing files\n" + list_str
                self.request.sendall(message.encode('utf-8'))

            elif parts[0] == 'GET':
                if len(parts) < 2:
                    self.request.sendall("5 missing file\n".encode('utf-8'))
                    return

                # check for file
                path = os.path.join(dirname, parts[1])
                if not os.path.isfile(path):
                    self.request.sendall("4 file not found\n".encode('utf-8'))
                    return

                f = open(path, 'rb')
                self.request.sendall("3 sending file\n".encode('utf-8'))
                b = f.read(1024)
                while (b):
                    self.request.sendall(b)
                    b = f.read(1024)
                f.close()

            else:
                self.request.sendall("1 unknown command\n".encode('utf-8'))

    # Here is where we will serve the files
    server = socketserver.TCPServer((hostname, port), ShareHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        # Stop on Ctrl+C
        pass
    finally:
        server.shutdown()
        server.server_close()
        # De-register the service
        zeroconf.unregister_service(info)
        zeroconf.close()

def list_hosts():
    """
    Scans the network for LANShare hosts and prints them to stdout.
    """
    def print_hostnames(zeroconf, service_type, name, state_change):
        """
        Prints the hostname to stdout
        """
        if state_change is ServiceStateChange.Added:
            hostname = name.split('.')
            print(hostname[0])

    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf,
                    '_lanshare._tcp.local.',
                    handlers=[print_hostnames])

    zeroconf.close()

def get_file_list(address, port):
    """ Ask a lanshare server for a list of files. """
    received = ""

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
         # Connect to server and request list of files
        sock.connect((address, port))
        sock.sendall(b"LIST")

        # Receive data from the server and shut down
        # Needs size limit?
        b = sock.recv(1024)
        while b:
            received += b.decode('utf-8')
            b = sock.recv(1024)
    finally:
        sock.close()

    if len(received) == 0 and received[0] != '2':
        print("Error getting list of files from")
        return

    i = received.find('\n')
    if i > 1:
        received = received[i+1:]
    print(received)


def list_files(hostname):
    """
    Asks a host for a list of it's shared files and prints them to stdout.
    """
    zeroconf = Zeroconf()
    fqdn = '{0}.local.'.format(hostname)

    def get_hostnames(zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            host = zeroconf.get_service_info(service_type, name)
            if host is not None and host.server == fqdn:
                get_file_list(socket.inet_ntoa(host.address), host.port)

    browser = ServiceBrowser(zeroconf,
                    '_lanshare._tcp.local.',
                   handlers=[get_hostnames])

    sleep(3)


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
    print("  lanshare -S [<dir>]               - serve directory to the LAN")

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
            serve(args[2])
        else:
            serve()
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

