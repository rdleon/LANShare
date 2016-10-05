# LANShare

Easily share your files in a local network.

This repo contains a sample command line application and a portable C library
that implements the lowlevel actions to discover clients and transfer files.

## How does it work?

First, bring up a server that shares all the files in the current directory.

    hostA$ lanshare -s

In another host, we search for lanshare servers in the network. This prints the
list of available hosts.

    hostB$ lanshare
    hostA
    host1
    host2
    ...
    hostN


We can get a list of all the available files being shared by certain <host>.

    hostB$ lanshare <host>
    file_1
    file_2
    ...
    file_N

Copies the specified <file> from <host> to the current working directory or
the path specified in <ouput>.

    hostB$ lanshare -g <host>:<file> [<output>]
