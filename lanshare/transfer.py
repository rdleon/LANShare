import sys, socket
from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange
from lanshare.conf import __block_size__

def download_file(host, port, filename, save_as):
    """
    Asks for a file to a LANShare server and
    saves it
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file = open(output, "wb")

    try:
        sock.connect((host, port))
        command = "GET {0}".format(filename)
        sock.sendall(command.encode("utf-8"))
        buff = sock.recv(__block_size__)
        if buff[0:1] == b"3":
            i = buff.index(b"\n")
            if i > 0:
                buff = buff[i+1:]
                while buff:
                    f.write(buff)
                    buff = sock.recv(__block_size__)
            else:
                print("Error saving the file", file=sys.stderr)
        else:
            print("File {0} not found".format(filename), file=sys.stderr)
        # TODO: delete file if transfer fails
    finally:
        f.close()
        sock.close()

def get_file(hostname, filename, save_as=None):
    """
    Requests a file and saves it to the given path
    """
    zeroconf = Zeroconf()
    fqdn = "{0}.local.".format(hostname)

    if output is None:
        output = filename

    def find_host(zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            host = zeroconf.get_service_info(service_type, name)
            if host is not None and host.server == fqdn:
                download_file(socket.inet_ntoa(host.address), host.port, filename, output)

    browser = ServiceBrowser(zeroconf,
                "_lanshare._tcp.local.",
                handlers=[find_host])
