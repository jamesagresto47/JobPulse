import unittest
from unittest.mock import patch
import os
import tempfile
import sqlite3

# Adjust path to import jobpulse modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'jobpulse')))

from jobpulse.config import DB_PATH
import database
from filter import is_relevant_job
from scraper import get_jobs

class TestJobPulse(unittest.TestCase):
    def setUp(self):
        # Use a temporary file database for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        database.DB_PATH = self.db_path
        database.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)


    def test_empty_state_and_deduplication(self):
        # 1. Empty State Test
        company = "MockCompany"
        title = "Software Engineer"
        url = "http://example.com/job1"
        
        # Initially not tracked
        is_tracked = database.is_job_tracked(database.generate_job_id(company, title, url))
        self.assertFalse(is_tracked)
        
        # Track it (simulate first run)
        tracked = database.filter_unseen_and_track(company, title, url)
        self.assertTrue(tracked)
        
        # 2. De-duplication Test
        # Track it again (simulate second run immediately after)
        tracked_again = database.filter_unseen_and_track(company, title, url)
        self.assertFalse(tracked_again) # Should return False, indicating it's an old job

    def test_exclusion_validation(self):
        # 3. Exclusion Validation
        # "Senior Software Engineer" should be excluded due to 'senior' keyword
        self.assertFalse(is_relevant_job("Senior Software Engineer"))
        
        # "Junior Software Engineer" should be included
        self.assertTrue(is_relevant_job("Junior Software Engineer"))
        
        # "Python Developer" should be included
        self.assertTrue(is_relevant_job("Python Developer"))
        
        # "Manager of Engineering" should be excluded
        self.assertFalse(is_relevant_job("Manager of Engineering"))

    @patch('scraper.requests.get')
    def test_resiliency(self, mock_get):
        # 4. Resiliency Test
        # Mocking requests.get to raise a RequestException for a broken URL
        import requests
        mock_get.side_effect = requests.RequestException("Domain does not exist")
        
        # Calling get_jobs on a broken URL should not crash, but return an empty list
        jobs = get_jobs("https://this-domain-does-not-exist-12345.com", "BrokenCompany")
        
        self.assertEqual(jobs, [])

if __name__ == '__main__':
    unittest.main()
