#!/bin/sh
#/home/pi/RomTaStick/bin/game_info.py --system "$1" --rom "$3"
/home/pi/RomTaStick/bin/push_event.py --type start_game --data "{\"system\":\"$1\",\"rom\":\"$3\"}"
