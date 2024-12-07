import unittest
from mantas_z_mod1_atsiskaitymas.crawler import crawl

class TestCrawl(unittest.TestCase):

    def test_crawl_gintarine(self):
        source = "gintarine"
        result = crawl(source, data_format="list")
        self.assertEqual(list(result[0].keys()), ["Title", "Price"])

    def test_crawl_benu(self):
        source = "benu"
        result = crawl(source, data_format="list")
        self.assertEqual(list(result[0].keys()), ["Title", "Price"])

    def test_invalid_url(self):
        source = "lrytas"
        with self.assertRaises(ValueError):
            crawl(source, data_format="list")

    def test_timeout(self):
        source = "gintarine"
        with self.assertRaises(TimeoutError):
            crawl(source, time_limit=1)

    def test_csv_output(self):
        source = "gintarine"
        result = crawl(source, data_format="csv")
        self.assertEqual(result, "CSV failas 'data_csv.csv' sukurtas sėkmingai")

if __name__ == "__main__":
    unittest.main()