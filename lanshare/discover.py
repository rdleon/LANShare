import socket
import sys

from zeroconf import ServiceInfo, ServiceBrowser, ServiceStateChange, Zeroconf


def get_hosts():
    """Returns a list of available hosts in the network."""
    hosts = []

    def search_hostnames(zeroconf, service_type, name, state_change):
        """Prints the hostname to stdout."""
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


def list_files(address, port):
    """Returns a list of files shared by the given host."""
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

def browse_host(hostname):
    """Get a list of files stored in a host.

    First searches for the hostname in mDNS and then
    asks the host for a list of files.
    """
    filenames = []
    found = False
    zeroconf = Zeroconf()
    fqdn = '{0}.local.'.format(hostname)

    def get_hostnames(zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            host = zeroconf.get_service_info(service_type, name)
            if host is not None and host.server == fqdn:
                found = True
                address = socket_inet_ntoa(host.address)
                filenames = list_files(address, host.port)

    browser = ServiceBrowser(zeroconf,
                    '_lanshare._tcp.local.',
                   handlers=[get_hostnames])

    if not found:
        print("Couldn't find {0} in the network".format(hostname),
              file=sys.stderr)

    return filenames
