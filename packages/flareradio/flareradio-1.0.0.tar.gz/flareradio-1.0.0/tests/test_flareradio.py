import unittest
from unittest.mock import patch
from flareradio import stats, upcoming

class TestFlareRadio(unittest.TestCase):
    @patch('flareradio.requests.get')
    def test_stats(self, mock_get):
        mock_get.return_value.json.return_value = {'listeners': 100}
        result = stats()
        self.assertEqual(result, {'listeners': 100})

    @patch('flareradio.requests.get')
    def test_upcoming(self, mock_get):
        mock_get.return_value.json.return_value = {'shows': []}
        result = upcoming()
        self.assertEqual(result, {'shows': []})

if __name__ == '__main__':
    unittest.main()
