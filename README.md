# LANShare

Easily share your files in a heterogeneus local network.

## How does it work?

First, bring up a server that shares all the files in the current directory.

    hostA$ lanshare -s [<file/dir>]

In another host, we search for lanshare servers in the network. This prints the
list of available hosts.

    hostB$ lanshare -f
    hostA
    host1
    host2
    ...
    hostN


We can get a list of all the available files being shared by certain <host>.

    hostB$ lanshare -f <host>
    file_1
    file_2
    ...
    file_N

Copies the specified <file> from <host> to the current working directory or
the path specified in <ouput>.

    hostB$ lanshare <host>:<file> [<output>]


# Future Plans

A Portable C library, a collection of executables and a fully open and
documented protocol.
