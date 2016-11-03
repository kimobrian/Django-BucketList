from django.test import LiveServerTestCase
from selenium import webdriver


class FrontEndViewsTests(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()

    def tearDown(self):
        self.selenium.quit()

    def test_page_title(self):
        """Test the page title"""
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        self.assertEqual(selenium.title, "Djangular BucketList")
