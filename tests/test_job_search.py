import unittest
from unittest.mock import MagicMock
from src.job_search import JobSearch

class TestJobSearch(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.config = {
            'search_terms': ['Software Engineer'],
            'location': 'San Francisco, CA',
            'date_posted': 'Past week',
            'sort_by': 'Most recent'
        }
        self.job_search = JobSearch(self.mock_driver, self.config)

    def test_search(self):
        self.mock_driver.find_elements.return_value = [MagicMock(get_attribute=MagicMock(return_value='123'))]
        job_listings = self.job_search.search()
        self.assertEqual(len(job_listings), 1)
        self.assertEqual(job_listings[0], '123')

if __name__ == '__main__':
    unittest.main()