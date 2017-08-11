import sys
sys.path.append('../settings')

import os
import unittest
import ConfigParser

import settings

class TestSettings(unittest.TestCase):

    test_path = '/tmp/test-settings.ini'

    def tearDown(self):
        if os.path.isfile(self.test_path):
            os.remove(self.test_path)

    def test_write(self):
        stgs = settings.Settings(self.test_path)
        stgs.write('section1', 'prop1', 'yes')

        # File is created
        self.assertTrue(os.path.isfile(self.test_path))

        # Property is present
        config = ConfigParser.RawConfigParser()
        config.read(self.test_path)
        self.assertEqual(config.get('section1', 'prop1'), 'yes')

    def test_write_same_section_twice(self):
        stgs = settings.Settings(self.test_path)
        stgs.write('section1', 'prop1', 'yes')
        stgs.write('section1', 'prop1', 'yes')

        # File is created
        self.assertTrue(os.path.isfile(self.test_path))

        # Property is present
        config = ConfigParser.RawConfigParser()
        config.read(self.test_path)
        self.assertEqual(config.get('section1', 'prop1'), 'yes')

    def test_read(self):
        config = ConfigParser.RawConfigParser()
        config.add_section('section1')
        config.set('section1', 'prop1', 'ok')
        with open(self.test_path, 'wb') as configfile:
            config.write(configfile)

        stgs = settings.Settings(self.test_path)
        self.assertEqual(stgs.read('section1', 'prop1'), 'ok')


if __name__ == '__main__':
    unittest.main()
