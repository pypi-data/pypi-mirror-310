import unittest
import localemembers

class TestLocaleMembers(unittest.TestCase):

    def test_locale_members(self):
        self.assertIsNotNone(localemembers.system_locale)
        self.assertIsNotNone(localemembers.locale_encoding)
        self.assertIsNotNone(localemembers.friendly_language)
        self.assertIsNotNone(localemembers.locale_country)
        self.assertIsNotNone(localemembers.language_code)
        self.assertIsNotNone(localemembers.country_code)
        self.assertIsNotNone(localemembers.formatted_language_code)

if __name__ == '__main__':
    unittest.main()
