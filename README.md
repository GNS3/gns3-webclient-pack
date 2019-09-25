# GNS3 WebClient pack

Client pack to use with the web Ui via protocol handlers

## Supported protocol handlers

The GNS3 WebClient currently support these URL schemes:

 * `gns3+telnet` for Telnet consoles
 * `gns3+vnc` for VNC consoles
 * `gns3+spice` for SPICE consoles
 * `gns3+pcap` for packet captures

URLs can include the following parameters:

 * `name` is the name or hostname of a GNS3 node or the description of a packet capture
 * `project_id` is the GNS3 project UUID
 * `node_id` is the GNS3 node UUID
 * `link_id` is the GNS3 link UUID

### URL examples

**Telnet console with all parameters**

`gns3+telnet://localhost:6000?name=R1&project_id=1234&node_id=5678`

**VNC console**

`gns3+vnc://localhost:5901`

**SPICE console**

`gns3+spice://localhost:5000`

**Packet capture**

`gns3+pcap://localhost:3080?project_id=d991dbc0-b98f-42aa-88b2-288170cca9c7&link_id=5c7f5285-ba2f-4ff6-8741-d1a77324441a&name=MyPacketCapture`

## Installation

### Windows

Use the provided installer. Protocol handlers are registered during the installation.

### macOS

Drag and drop the app from the DMG into /Applications. Start the app at least once the register the protocol handlers.

### Linux (Debian package)

**ONLY FOR UBUNTU 18.04 AT THE MOMENT**

You can install gns3-webclient-pack from our official [PPA](https://launchpad.net/~gns3/+archive/ubuntu/unstable):


```
sudo add-apt-repository ppa:gns3/unstable
sudo apt-get update
sudo apt-get install gns3-webclient-pack
```

or download .deb packages from [here](https://launchpad.net/~gns3/+archive/ubuntu/unstable/+packages).

The Debian package will install all dependencies including telnet, vinagre, virt-viewer and wireshark.

### Linux (Pypi package)

pip3 install gns3-webclient-pack

You may have to manually install dependencies including telnet, vinagre, virt-viewer and wireshark.

### Linux script installation

Alternatively, you can install gns3-webclient-pack from terminal using the following command:

wget -qO- https://raw.githubusercontent.com/GNS3/gns3-webclient-pack/master/install.sh | sh

This method should work on most Linux distros. Please open an new issue if this is not the case.
