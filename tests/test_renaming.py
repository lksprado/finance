import unittest
from unittest.mock import patch, MagicMock
import os
import sys 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.prep.renaming import list_files

class TestListFiles(unittest.TestCase):
    @patch('os.listdir')
    @patch('os.path.join', side_effect=lambda a, b: f"{a}/{b}")
    def test_list_files(self, mock_join, mock_listdir):
        # Mock the return value of os.listdir
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'file3.txt']

        # Call the function
        result = list_files('/some/path')

        # Check if os.listdir was called with the correct path
        mock_listdir.assert_called_once_with('/some/path')

        # Check if os.path.join was called the correct number of times
        self.assertEqual(mock_join.call_count, 3)

        # Check if the result is correct and sorted
        expected_result = [
            '/some/path/file1.txt',
            '/some/path/file2.txt',
            '/some/path/file3.txt'
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
