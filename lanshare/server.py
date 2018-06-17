import os, os.path, socket, socketserver
from lanshare.conf import __block_size__

shared_dir = None

def list_directory(directory, hidden=False):
    """
    Returns a list of files ready to be shared
    """
    files = []

    for filename in os.listdir(dirname):
        if not hidden and filename[0] == '.':
            continue

        if filename == '.' or filename == '..':
            continue

        path = os.path.join(dirname, filename)
        if os.path.isfile(path):
            files.append(filename)

    return files

class ShareHandler(socketserver.BaseRequestHandler):
    """
    Server handler, dispatches the commands, listing the
    available files and sending the requested files
    """
    def handle(self):
        command = self.request.recv(__block_size__).strip()
        parts = command.decode('utf-8').split(' ')

        if parts[0] == 'LIST':
            files = list_dir(shared_dir)
            listing = files.join("\n")
            message = "2 listing files\n" + listing.encode('utf-8')
            self.request.sendall(message)

        elif parts[0] == 'GET':
            if len(parts) < 2:
                self.request.sendall("5 missing file\n")
                return

            path = os.path.join(shared_dir, parts[1])
            if not os.path.isfile(path):
                self.request.sendall("4 file not found\n")
                return

            file = open(path, 'rb')
            self.request.sendall("3 sending file\n")
            buff = file.read(__block_size__)
            while buff:
                self.request.sendall(buff)
                buff = file.read(__block_size__)
            file.close()

        else:
            self.request.sendall("1 unknown command\n")

def serve_files(dirname=None):
    """
    Register as a ZeroConf/Bonjour/mDNS service and serves the files
    in the supplied directory. If dirname is missing it serves files
    from the current working directory.
    """
    hostname = socket.gethostname
    ip_addr = socket.gethostbyname(hostname)
    # TODO: Ask the OS for a port binding
    port = 10108
    desc = {'version': '0.1'}

    info = ServiceInfo("_lanshare._tcp.local.",
               "{0}._lanshare._tcp.local".format(hostname),
               socket.inet_aton(ip_addr),
               port, 0, 0, desc,
               "{0}.local.".format(hostname))

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    if dirname is not None:
        shared_dir = dirname
    else:
        shared_dir = os.getcwd()

    server = socketserver.TCPServer((hostname, port), ShareHandler)

    try:
        print("Press Ctrl-C to stop sharing...")
        server.serve_forever()
    except KeyboardInterrupt:
        # Stop on Ctrl+C
        pass
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()
        server.shutdown()
        server.server_close()
