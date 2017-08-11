import sys
sys.path.append('../game')

import unittest

import game

class TestGame(unittest.TestCase):

    def test_find_game_info_with_metadata(self):
        query = game.GameQuery('arcade', '/home/pi/RetroPie/roms/arcade/ddragon.zip')
        game_info = game.find_game_info(query)

        self.assertEqual(game_info.name, 'Double Dragon')
        self.assertEqual(game_info.developer, 'Technos Japan')
        self.assertEqual(game_info.releasedate, '19870701T000000')

    def test_find_game_info_without_metadata(self):
        query = game.GameQuery('arcade', '/home/pi/RetroPie/roms/arcade/nbajam.zip')
        game_info = game.find_game_info(query)

        self.assertEqual(game_info.name, 'NBA Jam (rev 3.01 04/07/93)')
        self.assertEqual(game_info.developer, None)
        self.assertEqual(game_info.releasedate, None)

if __name__ == '__main__':
    unittest.main()
