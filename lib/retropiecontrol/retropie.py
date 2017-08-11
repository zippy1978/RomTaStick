import sys
import os
from subprocess import call

def system_shutdown():
    call(['sudo', 'shutdown', '-h', 'now'])

def system_reboot():
    call(['sudo', 'reboot'])

def game_exit():
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

    for pid in pids:
        try:
            commandpath = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
            if commandpath[0:24] == '/opt/retropie/emulators/':
                os.system('kill -QUIT %s' % pid)
                print('kill -QUIT %s' % pid)
        except IOError:
            continue
