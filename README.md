# GNS3 WebClient pack

Client pack to use with the web Ui via protocol handlers

## Supported protocol handlers

The GNS3 WebClient currently support these URL schemes:

 * `gns3+telnet` for Telnet consoles
 * `gns3+vnc` for VNC consoles
 * `gns3+spice` for SPICE consoles

URLs can include the following parameters:

 * `name` is the name or hostname of a GNS3 node
 * `project_id` is the GNS3 project UUID
 * `node_id` is the GNS3 node UUID

### URL examples

**Telnet console with all parameters**

`gns3+telnet://localhost:6000?name=R1&project_id=1234&node_id=5678`

**VNC console**

`gns3+vnc://localhost:2900`

**SPICE console**

`gns3+spice://localhost:5000`
