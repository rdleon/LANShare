#!/usr/bin/env python

import sys, socket
from zeroconf import ServiceInfo, ServiceBrowser, ServiceStateChange, Zeroconf
from lanshare.conf import __version__
from lanshare.discover import get_hosts, browse_host
from lanshare.server import serve_files
from lanshare.transfer import get_file

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
    elif args[1] == "--version":
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
