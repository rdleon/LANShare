# LANShare

Easily share your files in a local network.

This repo contains a sample CLI application and a portable C library that
implements the lowlevel actions to discover clients and transfer files.

## How does it work?

  `$ lanshare -s`

Brings up a server that shares all the files in the current directory.

  `$ lanshare`

Searches for other lanshares hosts in the network.

  `$ lanshare <host>`

List all the available files being share by that host
