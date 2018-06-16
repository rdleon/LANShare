import socket
from zeroconf import ServiceInfo, ServiceBrowser, ServiceStateChange, Zeroconf

def get_hosts():
    """
    Returns a list of available hosts in the network
    """
    hosts = []

    def search_hostnames(zeroconf, service_type, name, state_change):
        """
        Prints the hostname to stdout
        """
        if state_change is ServiceStateChange.Added:
            hostname = name.split('.')
            hosts.append(hostname[0])

    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf,
                  '_lanshare._tcp.local.',
                  handlers=[search_hostnames])

    # Should sleep to allow discover?
    zeroconf.close()

    return hosts

def get_files(host, port):
    """
    Returns a list of files shared by the given host
    """
    files = []
    received = ""

    address = host
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server
        sock.connect((address, port))
        # Request the list of files
        sock.sendall(b"LIST")

        buff = sock.recv(1024)
        while buff:
            received += buff.decode('utf-8')
            buff = sock.recv(1024)
    finally:
        sock.close()

    if len(received) == 0 and received[0] != '2':
        raise Exception()

    files = received.split("\n")
    files.pop()

    return files
