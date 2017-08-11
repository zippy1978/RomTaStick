#!/bin/bash

echo "RomTaStick uninstall script..."

# Remove scripts
rm ~/RetroPie/retropiemenu/romtastick.sh
rm /opt/retropie/configs/all/runcommand-onstart.sh
rm /opt/retropie/configs/all/runcommand-onend.sh

# Remove startup script
# Install startup script
sudo update-rc.d romtastick disable
sudo rm /etc/init.d/romtastick

# Remove Splash screen
rm -rf ~/RetroPie/splashscreens/romtastick

echo "Done."
