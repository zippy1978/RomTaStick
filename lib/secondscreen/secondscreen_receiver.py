import sys
from subprocess import call
from events.events import *
from secondscreen.util import *
from settings.settings import *
from game.game import *
from transitions import Machine
from menu import *
from retropiecontrol.retropie import *

from secondscreen.display import *

LEFT_BUTTON = 17
RIGHT_BUTTON = 18

class SecondScreenEventReceiver(BaseEventReceiver):


    states = ['emu_menu', 'game', 'game_root_menu', 'game_details', 'game_exit', 'system_menu', 'system_shutdown', 'system_reboot']
    transitions = [
        { 'trigger': 'stop_game', 'source': '*', 'dest': 'emu_menu' },
        { 'trigger': 'start_game', 'source': '*', 'dest': 'game' },
        { 'trigger': 'left_button_pressed', 'source': 'game', 'dest': 'game_root_menu' },
        { 'trigger': 'left_button_pressed', 'source': 'emu_menu', 'dest': 'system_menu' },
        { 'trigger': 'left_button_pressed', 'source': 'game_details', 'dest': 'game_root_menu' },
    ]
    game_info = None
    device = None
    menu = None

    def __init__(self):
         self.machine = Machine(model=self, states=SecondScreenEventReceiver.states, transitions=self.transitions, initial='emu_menu', ignore_invalid_triggers=True)
         self.on_enter_emu_menu(None)

    # Get screen device interface
    def get_device(self):

        if self.device == None:
            stgs = Settings()
            device_type = stgs.read('SECOND_SCREEN', 'type')
            if device_type != 'None':
                klass = get_class('secondscreen.display.' + device_type + 'Display')
                self.device =  klass()
            else:
                self.device =  None

        return self.device

    # Update current menu display
    def refresh_menu(self):
        if self.menu != None:
            device = self.get_device()
            if device != None:
                device.show_menu(self.menu)

    def system_menu_back(self):
        if self.game_info != None:
            self.to_game_root_menu()
        else:
            self.to_emu_menu()

    def on_event(self, event):

        if event.type == 'gpio_button_pressed' and event.data['button_num'] == LEFT_BUTTON:
            # Left button is used for selection in menus
            if self.menu == None:
                self.left_button_pressed()
            else :
                selected_item = self.menu.items[self.menu.get_selected_index()]
                if selected_item.action != None:
                    selected_item.action()

        elif event.type == 'gpio_button_pressed' and event.data['button_num'] == RIGHT_BUTTON:
            # Right button is used to change selection in menus
            if self.menu != None:
                self.menu.select_next()
                self.refresh_menu()

        elif event.type == 'start_game':
            self.start_game(event)

        elif event.type == 'stop_game':
            self.stop_game(event)

    def on_enter_game(self, event=None):
        self.menu = None
        device = self.get_device()
        if device != None:
            if event != None :
                game_query = GameQuery(event.data['system'], event.data['rom'])
                self.game_info = find_game_info(game_query)
            device.show_game_info(self.game_info)

    def on_enter_game_root_menu(self):
        self.menu = Menu([
            MenuItem('BACK', self.to_game),
            MenuItem('GAME DETAILS', self.to_game_details),
            MenuItem('EXIT GAME', self.to_game_exit),
            MenuItem('SYSTEM', self.to_system_menu, MenuItem.SYMBOL_ARROW)
        ], self.game_info.name)
        self.refresh_menu()

    def on_enter_game_details(self):
        self.menu = None
        device = self.get_device()
        if device != None:
            if self.game_info.genre != None:
                device.show_game_details(self.game_info)
            else:
                device.show_system_message('No details available for this game.')

    def on_enter_game_exit(self):
        self.menu = None
        self.game_info = None
        game_exit()

    def on_enter_system_menu(self):

        self.menu = Menu([
            MenuItem('BACK', self.system_menu_back),
            MenuItem('SHUTDOWN', self.to_system_shutdown),
            MenuItem('REBOOT', self.to_system_reboot)
        ], 'SYSTEM')
        self.refresh_menu()

    def on_enter_system_shutdown(self):
        self.menu = None
        self.game_info = None
        device = self.get_device()
        if device != None:
            device.show_system_message("System is shutting down.\nDon't unplug the power supply until this screen has disappeared.")
        system_shutdown()

    def on_enter_system_reboot(self):
        self.menu = None
        self.game_info = None
        device = self.get_device()
        if device != None:
            device.show_system_message("System is rebooting.")
        system_reboot()

    def on_enter_emu_menu(self, event=None):
        self.menu = None
        self.game_info = None
        device = self.get_device()
        if device != None:
            device.show_splashscreen()


# Register receiver
register_event_receiver(SecondScreenEventReceiver())
