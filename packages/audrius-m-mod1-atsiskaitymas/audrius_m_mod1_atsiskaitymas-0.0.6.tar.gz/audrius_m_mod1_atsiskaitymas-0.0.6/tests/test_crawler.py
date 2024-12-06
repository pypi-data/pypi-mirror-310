import unittest
from audrius_m_mod1_atsiskaitymas.crawler import crawl


class CrawlTestCase(unittest.TestCase):
    """
    Unit tests
    """

    def test_crawl_html_format(self):
        # Test crawling with default parameters and expecting HTML format
        result = crawl()
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith('<!DOCTYPE html>'))

    def test_crawl_text_format(self):
        # Test crawling and expecting text format
        result = crawl(return_format='text')
        self.assertIsNotNone(result)
        self.assertTrue('Welcome to Wikipedia' in result)

    def test_crawl_with_custom_source(self):
        # Test crawling from a custom source
        result = crawl(source='https://en.wikipedia.org/wiki/Python_(programming_language)')[100:]
        self.assertIsNotNone(result)
        self.assertIn('Python (programming language)', result)

    def test_crawl_with_invalid_url(self):
        # Test crawling with an invalid URL
        result = crawl(source='https://en.wikipedia.org/wiki/Non_existent_page')
        self.assertIsNone(result)

    def test_crawl_with_timeout(self):
        # Test crawling with a timeout
        result = crawl(time_limit=5, source='https://httpbin.org/delay/10')
        self.assertIsNone(result)

    def test_crawl_with_unsupported_format(self):
        # Test crawling with an unsupported format should raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            crawl(return_format='json')


if __name__ == '__main__':
    unittest.main()
