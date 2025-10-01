import unittest
from nst_news import NSTArticle

# Check length is more than 0

class TestNSTNews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setup NSTArticle for testing.")
        cls.nst = NSTArticle()

    @classmethod
    def tearDownClass(cls):
        print("Closing NSTArticle.")
        cls.nst.close()

    def test_scrape_index(self):
        results = self.nst.scrape_index()
        self.assertTrue(len(results) > 0)

    def test_scrape_latest(self):
        results = self.nst.scrape_latest()
        self.assertTrue(len(results) > 0)

    def test_scrape_worlds(self):
        results = self.nst.scrape_worlds()
        self.assertTrue(len(results) > 0)

    def test_scrape_search_results(self):
        query = "economy"
        results = self.nst.scrape_search_results(query, limit=3)
        self.assertTrue(len(results) > 0)