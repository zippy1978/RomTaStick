#!/bin/bash

echo "RomTaStick installation script ..."

# Install depedencies
sudo apt-get install python-pip
#sudo apt-get install python-pygame
sudo pip install python-uinput
sudo pip install Pillow
sudo pip install spidev
sudo pip install requests
sudo pip install transitions
sudo pip install Adafruit_ILI9341
sudo pip install Adafruit-GPIO

# Copy scripts
cp menu/romtastick.sh /home/pi/RetroPie/retropiemenu
cp scripts/runcommand-onstart.sh /opt/retropie/configs/all
cp scripts/runcommand-onend.sh /opt/retropie/configs/all

# Install startup script
sudo cp scripts/romtastick /etc/init.d
sudo chmod +x /etc/init.d/romtastick
sudo update-rc.d romtastick defaults

# Splash screen
mkdir -p ~/RetroPie/splashscreens/romtastick
cp splashscreens/romtastick.png ~/RetroPie/splashscreens/romtastick


echo "Done."
