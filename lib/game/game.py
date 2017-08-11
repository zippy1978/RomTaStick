import os.path
import xml.etree.ElementTree as ET

class GameInfo(object):
    name = None
    releasedate = None
    developer = None
    image = None

    def __init__(self, name, releasedate=None, developer=None, image=None, description=None, genre=None):
        self.name = name
        self.releasedate = releasedate
        self.developer = developer
        self.image = image
        self.description = description
        self.genre = genre

class GameQuery(object):
    system = None
    rom_path = None

    def __init__(self, system, rom_path):
        self.system = system
        self.rom_path = rom_path


# Filter game by path
def _filter_by_path(seq, path):
   for el in seq:
       if el.find('path').text==path: yield el

# Get XML element text value if exists
def _get_text(element):
    if element != None:
        return element.text
    return None

# Get first item of an iterable
def _get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

# Find game info
def find_game_info(game_query):

    xml_file = "/home/pi/.emulationstation/gamelists/%s/gamelist.xml" % (game_query.system)
    short_rom_path = game_query.rom_path.split('/')[-1]

    if os.path.isfile(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        games_el = root.findall(".//game")
        game_el = _get_first(_filter_by_path(games_el,"./%s" % (short_rom_path)))
	if game_el != None:
            name = _get_text(game_el.find('name'))
            releasedate = _get_text(game_el.find('releasedate'))
            developer = _get_text(game_el.find('developer'))
            image = _get_text(game_el.find('image'))
            desc = _get_text(game_el.find('desc'))
            genre = _get_text(game_el.find('genre'))
            return GameInfo(name, releasedate = releasedate, developer = developer, image = image, description = desc, genre = genre)

    return GameInfo(short_rom_path)
