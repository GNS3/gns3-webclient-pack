# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Default general settings.
"""

import os
import sys
import distro
import shutil


# Pre-configured Telnet console commands on various OSes
if sys.platform.startswith("win"):
    userprofile = os.path.expandvars("%USERPROFILE%")
    if "PROGRAMFILES(X86)" in os.environ:
        # windows 64-bit
        program_files = os.environ["PROGRAMFILES"]
        program_files_x86 = os.environ["PROGRAMFILES(X86)"]
    else:
        # windows 32-bit
        program_files_x86 = program_files = os.environ["PROGRAMFILES"]

    PRECONFIGURED_TELNET_COMMANDS = {'Putty (normal standalone version)': 'putty_standalone.exe -telnet {host} {port} -loghost "{name}"',
                                     'Putty (custom deprecated version)': 'putty.exe -telnet {host} {port} -wt "{name}" -gns3 5 -skin 4',
                                     'MobaXterm': r'"{}\Mobatek\MobaXterm Personal Edition\MobaXterm.exe" -newtab "telnet {{host}} {{port}}"'.format(program_files_x86),
                                     'Royal TS V3': r'{}\code4ward.net\Royal TS V3\RTS3App.exe /connectadhoc:{{host}} /adhoctype:terminal /p:IsTelnetConnection="true" /p:ConnectionType="telnet;Telnet Connection" /p:Port="{{port}}" /p:Name="{{name}}"'.format(program_files),
                                     'Royal TS V5': r'"{}\Royal TS V5\RoyalTS.exe" /protocol:terminal /using:adhoc /uri:"{{host}}" /property:Port="{{port}}" /property:IsTelnetConnection="true" /property:Name="{{name}}"'.format(program_files_x86),
                                     'SuperPutty': r'SuperPutty.exe -telnet "{host} -P {port} -wt \"{name}\""',
                                     'SecureCRT': r'"{}\VanDyke Software\SecureCRT\SecureCRT.exe" /N "{{name}}" /T /TELNET {{host}} {{port}}'.format(program_files),
                                     'SecureCRT (personal profile)': r'"{}\AppData\Local\VanDyke Software\SecureCRT\SecureCRT.exe" /T /N "{{name}}" /TELNET {{host}} {{port}}'.format(userprofile),
                                     'TeraTerm Pro': r'"{}\teraterm\ttermpro.exe" /W="{{name}}" /M="ttstart.macro" /T=1 {{host}} {{port}}'.format(program_files_x86),
                                     'Telnet': 'telnet {host} {port}',
                                     'Xshell 4': r'"{}\NetSarang\Xshell 4\xshell.exe" -url telnet://{{host}}:{{port}}'.format(program_files_x86),
                                     'Xshell 5': r'"{}\NetSarang\Xshell 5\xshell.exe" -url telnet://{{host}}:{{port}} -newtab {{name}}'.format(program_files_x86),
                                     'Windows Terminal': r'wt.exe -w 1 new-tab --title {name} telnet {host} {port}',
                                     'ZOC 6': r'"{}\ZOC6\zoc.exe" "/TELNET:{{host}}:{{port}}" /TABBED "/TITLE:{{name}}"'.format(program_files_x86)}

    # default on Windows
    if shutil.which("Solar-PuTTY.exe"):
        # Solar-Putty is the default if it is installed.
        PRECONFIGURED_TELNET_COMMANDS["Solar-Putty (included with GNS3)"] = 'Solar-PuTTY.exe --telnet --hostname {host} --port {port}  --name "{name}"'
        DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Solar-Putty (included with GNS3)"]
    else:
        PRECONFIGURED_TELNET_COMMANDS["Solar-Putty (included with GNS3 downloaded from gns3.com)"] = 'Solar-PuTTY.exe --telnet --hostname {host} --port {port}  --name "{name}"'
        DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Putty (normal standalone version)"]

elif sys.platform.startswith("darwin"):
    # Mac OS X
    PRECONFIGURED_TELNET_COMMANDS = {
        'Terminal': r"""osascript"""
                    r""" -e 'set posix_path to do shell script "echo \"$PATH\""'"""
                    r""" -e 'tell application "Terminal"'"""
                    r""" -e 'activate'"""
                    r""" -e 'do script "echo -n -e \"\\033]0;{name}\\007\"; clear; PATH=" & quoted form of posix_path & " telnet {host} {port} ; exit"'"""
                    r""" -e 'end tell'""",
        'Terminal tabbed (experimental)': r"""osascript"""
                    r""" -e 'set posix_path to do shell script "echo \"$PATH\""'"""
                    r""" -e 'tell application "Terminal"'"""
                    r""" -e 'activate'"""
                    r""" -e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down'"""
                    r""" -e 'if (the (count of the window) = 0) then'"""
                    r""" -e 'repeat while contents of selected tab of window 1 starts with linefeed'"""
                    r""" -e 'delay 0.01'"""
                    r""" -e 'end repeat'"""
                    r""" -e 'tell application "System Events" to keystroke "n" using command down'"""
                    r""" -e 'end if'"""
                    r""" -e 'repeat while the busy of window 1 = true'"""
                    r""" -e 'delay 0.01'"""
                    r""" -e 'end repeat'"""
                    r""" -e 'do script "echo -n -e \"\\033]0;{name}\\007\"; clear; PATH=" & quoted form of posix_path & " telnet {host} {port} ; exit" in window 1'"""
                    r""" -e 'end tell'""",
        'iTerm2 2.x': r"""osascript"""
                    r""" -e 'set posix_path to do shell script "echo \"$PATH\""'"""
                    r""" -e 'tell application "iTerm"'"""
                    r""" -e 'activate'"""
                    r""" -e 'if (count of terminals) = 0 then'"""
                    r""" -e '  set t to (make new terminal)'"""
                    r""" -e 'else'"""
                    r""" -e '  set t to current terminal'"""
                    r""" -e 'end if'"""
                    r""" -e 'tell t'"""
                    r""" -e '  set s to (make new session at the end of sessions)'"""
                    r""" -e '  tell s'"""
                    r""" -e '    exec command "sh"'"""
                    r""" -e '    write text "PATH=" & quoted form of posix_path & " exec telnet {host} {port}"'"""
                    r""" -e '  end tell'"""
                    r""" -e 'end tell'"""
                    r""" -e 'end tell'""",
        'iTerm2 3.x': r"""osascript"""
                    r""" -e 'set posix_path to do shell script "echo \"$PATH\""'"""
                    r""" -e 'tell application "iTerm"'"""
                    r""" -e 'activate'"""
                    r""" -e 'if (count of windows) = 0 then'"""
                    r""" -e '   set t to (create window with default profile)'"""
                    r""" -e 'else'"""
                    r""" -e '   set t to current window'"""
                    r""" -e 'end if'"""
                    r""" -e 'tell t'"""
                    r""" -e '    create tab with default profile command "sh"'"""
                    r""" -e '    set s to current session'"""
                    r""" -e '    tell s'"""
                    r""" -e '        set name to "{name}"'"""
                    r""" -e '        write text "PATH=" & quoted form of posix_path & " exec telnet {host} {port}"'"""
                    r""" -e '    end tell'"""
                    r""" -e 'end tell'"""
                    r""" -e 'end tell'""",
        'Royal TSX': "open 'rtsx://telnet%3A%2F%2F{host}:{port}'",
        'SecureCRT': '/Applications/SecureCRT.app/Contents/MacOS/SecureCRT /N "{name}" /T /TELNET {host} {port}',
        'ZOC 6': '/Applications/zoc6.app/Contents/MacOS/zoc6 "/TELNET:{host}:{port}" /TABBED "/TITLE:{name}"',
        'ZOC 7': '/Applications/zoc7.app/Contents/MacOS/zoc7 "/TELNET:{host}:{port}" /TABBED "/TITLE:{name}"',
        'ZOC 8': '/Applications/zoc8.app/Contents/MacOS/zoc8 "/TELNET:{host}:{port}" /TABBED "/TITLE:{name}"'
    }

    # default Mac OS X Telnet console command
    DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Terminal"]

else:
    PRECONFIGURED_TELNET_COMMANDS = {'Xterm': 'xterm -T "{name}" -e "telnet {host} {port}"',
                                     'Putty': 'putty -telnet {host} {port} -title "{name}" -sl 2500 -fg SALMON1 -bg BLACK',
                                     'Gnome Terminal': 'gnome-terminal -t "{name}" -e "telnet {host} {port}"',
                                     'Xfce4 Terminal': 'xfce4-terminal --tab -T "{name}" -e "telnet {host} {port}"',
                                     'ROXTerm': 'roxterm -n "{name}" --tab -e "telnet {host} {port}"',
                                     'KDE Konsole': 'konsole --new-tab -p tabtitle="{name}" -e "telnet {host} {port}"',
                                     'SecureCRT': 'SecureCRT /T /N "{name}"  /TELNET {host} {port}',
                                     'Mate Terminal': 'mate-terminal --tab -e "telnet {host} {port}" -t "{name}"',
                                     'LXTerminal': 'lxterminal -t "{name}" -e "telnet {host} {port}"',
                                     'urxvt': 'urxvt -title {name} -e telnet {host} {port}',
                                     'kitty': 'kitty -T {name} telnet {host} {port}'}

    # default Telnet command on other systems
    DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Xterm"]

    if sys.platform.startswith("linux"):

        def find_desktop(*desktops):
            current_desktop = os.getenv('XDG_CURRENT_DESKTOP')
            if current_desktop:
                current_desktop = current_desktop.lower()
                for desktop in desktops:
                    if desktop in current_desktop:
                        return True
            return False


        if find_desktop("gnome", "unity", "cinnamon"):
            DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Gnome Terminal"]
        elif find_desktop("kde"):
            DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["KDE Konsole"]
        elif find_desktop("mate"):
            DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Mate Terminal"]
        elif find_desktop("xfce"):
            DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Xfce4 Terminal"]
        elif find_desktop("lxde", "lxqt"):
            DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["LXTerminal"]
        elif distro.name() in ["Debian", "Ubuntu", "LinuxMint"]:
            DEFAULT_TELNET_COMMAND = PRECONFIGURED_TELNET_COMMANDS["Gnome Terminal"]
        elif shutil.which("x-terminal-emulator"):
            DEFAULT_TELNET_COMMAND = 'x-terminal-emulator -T "{name}" -e "telnet {host} {port}"'

# Pre-configured VNC console commands on various OSes
if sys.platform.startswith("win"):
    # Windows
    PRECONFIGURED_VNC_COMMANDS = {
        'TightVNC (included with GNS3)': 'tvnviewer.exe {host}:{port}',
        'UltraVNC': r'"{}\uvnc bvba\UltraVNC\vncviewer.exe" {{host}}:{{port}}'.format(program_files)
    }

    # default Windows VNC console command
    DEFAULT_VNC_COMMAND = PRECONFIGURED_VNC_COMMANDS['TightVNC (included with GNS3)']

elif sys.platform.startswith("darwin"):
    # Mac OS X
    PRECONFIGURED_VNC_COMMANDS = {
        'OSX builtin screen sharing': "osascript"
        " -e 'tell application \"Screen Sharing\"'"
        " -e '   display dialog \"WARNING OSX VNC support is limited if you have trouble connecting to a device please use an alternative client like Chicken of the VNC.\" buttons {\"OK\"} default button 1 with icon caution with title \"GNS3\"'"
        " -e '  open location \"vnc://{host}:{port}\"'"
        " -e 'end tell'",
        'Chicken of the VNC': "/Applications/Chicken.app/Contents/MacOS/Chicken {host}:{port}",
        'Chicken of the VNC < 2.2': r"/Applications/Chicken\ of\ the\ VNC.app/Contents/MacOS/Chicken\ of\ the\ VNC {host}:{port}",
        'Royal TSX': "open 'rtsx://vnc%3A%2F%2F{host}:{port}'",
    }

    # default Mac OS X VNC command
    DEFAULT_VNC_COMMAND = PRECONFIGURED_VNC_COMMANDS['OSX builtin screen sharing']

else:
    PRECONFIGURED_VNC_COMMANDS = {
        'TightVNC': 'vncviewer {host}:{port}',
        'Vinagre': 'vinagre {host}::{port}',
        'gvncviewer': 'gvncviewer {host}:{port}',
        'Remote Viewer': 'remote-viewer vnc://{host}:{port}'
    }

    # default VNC command on other systems
    DEFAULT_VNC_COMMAND = PRECONFIGURED_VNC_COMMANDS['TightVNC']

# Pre-configured SPICE console commands on various OSes
if sys.platform.startswith("win"):
    # Windows
    PRECONFIGURED_SPICE_COMMANDS = {
        'Remote Viewer': r'"{}\VirtViewer v7.0-256\bin\remote-viewer.exe" spice://{{host}}:{{port}}'.format(program_files),
    }

    # default Windows SPICE command
    DEFAULT_SPICE_COMMAND = PRECONFIGURED_SPICE_COMMANDS['Remote Viewer']

elif sys.platform.startswith("darwin"):
    # Mac OS X
    PRECONFIGURED_SPICE_COMMANDS = {
        'Remote Viewer': '/Applications/RemoteViewer.app/Contents/MacOS/RemoteViewer spice://{host}:{port}',
    }

    # default Mac OS X SPICE command
    DEFAULT_SPICE_COMMAND = PRECONFIGURED_SPICE_COMMANDS['Remote Viewer']

else:
    PRECONFIGURED_SPICE_COMMANDS = {
        'Remote Viewer': 'remote-viewer spice://{host}:{port}',
    }

    # default SPICE command on other systems
    DEFAULT_SPICE_COMMAND = PRECONFIGURED_SPICE_COMMANDS['Remote Viewer']

# Pre-configured packet capture reader commands on various OSes
WIRESHARK_NORMAL_CAPTURE = "Wireshark Traditional Capture"
WIRESHARK_LIVE_TRAFFIC_CAPTURE = "Wireshark Live Traffic Capture"

if sys.platform.startswith("win"):
    PRECONFIGURED_PACKET_CAPTURE_READER_COMMANDS = {WIRESHARK_NORMAL_CAPTURE: r"{}\Wireshark\wireshark.exe {{pcap_file}}".format(program_files),
                                                    WIRESHARK_LIVE_TRAFFIC_CAPTURE: r'tail.exe -f -c +0b {{pcap_file}} | "{}\Wireshark\wireshark.exe" -o "gui.window_title:{{name}}" -k -i -'.format(program_files)}

elif sys.platform.startswith("darwin"):
    # Mac OS X
    PRECONFIGURED_PACKET_CAPTURE_READER_COMMANDS = {WIRESHARK_NORMAL_CAPTURE: "/usr/bin/open -a /Applications/Wireshark.app {pcap_file}",
                                                    "Wireshark V1.X Live Traffic Capture": 'tail -f -c +0 {pcap_file} | /Applications/Wireshark.app/Contents/Resources/bin/wireshark -o "gui.window_title:{name}" -k -i -',
                                                    WIRESHARK_LIVE_TRAFFIC_CAPTURE: 'tail -f -c +0 {pcap_file} | /Applications/Wireshark.app/Contents/MacOS/Wireshark -o "gui.window_title:{name}" -k -i -'}

elif sys.platform.startswith("freebsd"):
    # FreeBSD
    PRECONFIGURED_PACKET_CAPTURE_READER_COMMANDS = {WIRESHARK_NORMAL_CAPTURE: "wireshark {pcap_file}",
                                                    WIRESHARK_LIVE_TRAFFIC_CAPTURE: 'gtail -f -c +0b {pcap_file} | wireshark -o "gui.window_title:{name}" -k -i -'}
else:
    PRECONFIGURED_PACKET_CAPTURE_READER_COMMANDS = {WIRESHARK_NORMAL_CAPTURE: "wireshark {pcap_file}",
                                                    WIRESHARK_LIVE_TRAFFIC_CAPTURE: 'tail -f -c +0b {pcap_file} | wireshark -o "gui.window_title:{name}" -k -i -'}

DEFAULT_PACKET_CAPTURE_READER_COMMAND = PRECONFIGURED_PACKET_CAPTURE_READER_COMMANDS[WIRESHARK_LIVE_TRAFFIC_CAPTURE]


GENERAL_SETTINGS = {
    "geometry": "",
    "state": "",
}

COMMANDS_SETTINGS = {
    "telnet_command": DEFAULT_TELNET_COMMAND,
    "vnc_command": DEFAULT_VNC_COMMAND,
    "spice_command": DEFAULT_SPICE_COMMAND,
    "pcap_command": DEFAULT_PACKET_CAPTURE_READER_COMMAND
}

CUSTOM_COMMANDS_SETTINGS = {
    "telnet": {},
    "vnc": {},
    "spice": {}
}
