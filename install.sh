#!/bin/bash

set -e

do_install() {

	# install pip3 if missing
  if [ ! $(which pip3) ]
  then
    wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py && sudo python3 /tmp/get-pip.py
  fi

  # install the webclient pack
	sudo python3 -m pip install gns3-webclient-pack

	# build cache database of MIME types handled by desktop files
	sudo update-desktop-database -q || true
	sudo update-mime-database -n /usr/share/mime || true

  echo "Installation successfuly completed!"

	exit 0
}

# Detect the Linux distribution
if [ -r /etc/os-release ]
then
	. /etc/os-release
elif [ $(which lsb_release) ]
then
	ID=$(lsb_release -si)
	VERSION_ID=$(lsb_release -sr)
else]]
	echo "Sorry, your Linux distribution is not supported"
	exit 1
fi

echo "Detected Linux distribution: $ID $VERSION_ID (${ID_LIKE:-"none"})"

for distro_id in $ID $ID_LIKE; do
	case "$distro_id" in
		debian|ubuntu)
			sudo apt-get install -y python3 python3-pyqt5 telnet vinagre virt-viewer wireshark
			do_install
			;;
		arch|archlinux|manjaro)
			sudo pacman -S python python-pyqt5 qt5-websockets vinagre virt-viewer wireshark-qt
			do_install
			;;
		fedora)
			sudo dnf install -y python3 python3-pyqt5 telnet vinagre virt-viewer wireshark-qt
			do_install
			;;
		opensuse|suse)
			sudo zypper install -y python3 python3-pyqt5 telnet vinagre virt-viewer wireshark-ui-qt
			do_install
			;;
		#centos|CentOS|rhel)
		#	sudo yum install -y python3 PyQt5 telnet vinagre virt-viewer wireshark-gnome
		#	do_install
		#	;;
		*)
			continue
			;;
	esac
done

echo "Sorry, your Linux distribution is not supported"
exit 1
