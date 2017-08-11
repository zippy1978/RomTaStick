import sys
sys.path.append('../secondscreen')

import unittest

import display

class TestSSD1331Display(unittest.TestCase):

    def test_constructor(self):
        device = display.SSD1331Display()
        self.assertEqual(device.width, 96)
        self.assertEqual(device.height, 64)

if __name__ == '__main__':
    unittest.main()
