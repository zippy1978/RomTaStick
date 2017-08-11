import sys
sys.path.append('../secondscreen')

import unittest

import menu

class TestMenu(unittest.TestCase):

    def test_select_next(self):
        items = [menu.MenuItem('a'), menu.MenuItem('b')]
        m = menu.Menu(items)
        m.select_next()
        self.assertEqual(m.get_selected_index(), 1)

    def test_select_next_on_last(self):
        items = [menu.MenuItem('a'), menu.MenuItem('b')]
        m = menu.Menu(items)
        m.select_next()
        m.select_next()
        self.assertEqual(m.get_selected_index(), 0)


if __name__ == '__main__':
    unittest.main()
