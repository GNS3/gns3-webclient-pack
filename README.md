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

Drag and drop the app from the DMG into /Applications. Start the app at least once to register the protocol handlers.

### Linux (Debian package)

**ONLY FOR UBUNTU AT THE MOMENT**

You can install gns3-webclient-pack from our official [PPA](https://launchpad.net/~gns3/+archive/ubuntu/unstable):


```
sudo add-apt-repository ppa:gns3/unstable
sudo apt-get update
sudo apt-get install gns3-webclient-pack
```

or download .deb packages from [here](https://launchpad.net/~gns3/+archive/ubuntu/unstable/+packages).

The Debian package will install all dependencies including telnet, vinagre, virt-viewer and wireshark.

### Linux (Pypi package)

```
sudo python3 -m pip install gns3-webclient-pack
sudo gns3-webclient-config --install-mime-types
```

You may have to manually install dependencies including telnet, vinagre, virt-viewer and wireshark.

### Linux script installation

Alternatively, you can install gns3-webclient-pack from terminal using the following command:

```
wget -qO- https://raw.githubusercontent.com/GNS3/gns3-webclient-pack/master/install.sh | sh
```

This method should work on most Linux distros. Please open an new issue if this is not the case.

## Debugging

Use the `xdg-open` tool on Linux (from the `xdg-utils` package). For instance to start a Telnet console:

`xdg-open "gns3+telnet://127.0.0.1:5000/PC1"`

On other platforms, check the launcher logs:

- Windows: `%APPDATA%\GNS3\WebClient\launcher.log`
- Linux and MacOS: `~/.config/GNS3/WebClient/launcher.log`

## Tips

How to fix Chrome protocol handler “Always open these types of links in the associated app” pop up.

### Windows

Save the following content in a .reg file and execute as an Administrator.

```
[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome]
"ExternalProtocolDialogShowAlwaysOpenCheckbox"=dword:00000001
```

Note: the GNS3 all-in-one installer already does this.

### Linux

Create the folders as needed.

`sudo mkdir -p /etc/opt/chrome/policies/managed/`

Create an empty JSON file.

`sudo touch /etc/opt/chrome/policies/managed/managed_policies.json`

Add the following content in this JSON file.

```
{
  "ExternalProtocolDialogShowAlwaysOpenCheckbox": true
}
```

### MacOS

Run the following in a terminal.

```
defaults write com.google.Chrome URLWhitelist -array 'gns3+telnet://*' 'gns3+vnc://*' 'gns3+spice://*' 'gns3+pcap://*'
```
