import ConfigParser
import os

class Settings(object):

    _file_path = '/home/pi/.RomTaStick/settings.json'
    _config = None

    def __init__(self, file_path='/home/pi/.RomTaStick/settings.json'):
        self._file_path = file_path

        # Create parent dir
        parent_dir = os.path.abspath(os.path.join(self._file_path, os.pardir))
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        self._config = ConfigParser.RawConfigParser(allow_no_value=True)

    def write(self, section, property, value):

        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, property, value)
        with open(self._file_path, 'wb') as configfile:
            self._config.write(configfile)

    def read(self, section, property):
        try:
            self._config.read(self._file_path)
            value = self._config.get(section, property)
            if value == None:
                value = 'None'
            return self._config.get(section, property)
        except ConfigParser.NoSectionError:
            return 'None'
