#!/usr/bin/env bash

ROMTASTICK_HOME=/home/pi/RomTaStick
ROMS_PATH=/home/pi/RetroPie/roms

function safe_exit() {
  exit $1
}

# Expect sectio, property and name as parameters
# If the current vlaue is set in settings returns 'on', otherwise 'off'
function setting_property_onoff() {
  section=$1
  property=$2
  value=$3
  current_value=$($ROMTASTICK_HOME/bin/read_value.py --section $section --property $property)
  if [ "$value" = "$current_value" ]; then
    echo "on"
  else
    echo "off"
  fi;
}

function secondscreen_menu() {
  cmd=(dialog \
     --cancel-label "Back" \
     --radiolist "Select installed second screen" 19 80 12)
  options=(
    none      "None" $(setting_property_onoff SECOND_SCREEN type None)
    ssd1331   "SSD1331 (OLED 96x64)" $(setting_property_onoff SECOND_SCREEN type SSD1331)
    ili9341   "ILI9341 (TFT 240x320)" $(setting_property_onoff SECOND_SCREEN type ILI9341)
  )
  choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
  if [[ -n "$choice" ]]; then
    case $choice in
      0) main_menu
        ;;
  	  none)
        $ROMTASTICK_HOME/bin/write_value.py --section SECOND_SCREEN --property type --value None
    		;;
  	  ssd1331)
        $ROMTASTICK_HOME/bin/write_value.py --section SECOND_SCREEN --property type --value SSD1331
    		;;
      ili9341)
        $ROMTASTICK_HOME/bin/write_value.py --section SECOND_SCREEN --property type --value ILI9341
        ;;
    esac
  fi
}

function main_menu() {
  while true; do
    cmd=(dialog \
      --title " Welcome to RomTaStick " \
      --cancel-label "Exit" \
      --menu "Anything you need to run your RomTaStick" 19 80 12)
    options=(
      secondscreen "Configure second screen"
    )
    choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
      case $choice in
        secondscreen)  secondscreen_menu
            ;;
      esac
    else
      break
    fi
  done
}

main_menu

safe_exit 0
