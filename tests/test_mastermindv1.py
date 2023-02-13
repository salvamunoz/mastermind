import unittest
from unittest.mock import patch
from v1.mastermindv1 import get_next_nr_game


class TestGetNextNrGame(unittest.TestCase):
    @patch('v1.mastermindv1.collection')
    def test_get_next_nr_game_empty_collection(self, mock_collection):
        mock_collection.find_one.return_value = None
        result = get_next_nr_game()
        self.assertEqual(result, 0)

    @patch('v1.mastermindv1.collection')
    def test_get_next_nr_game_non_empty_collection(self, mock_collection):
        mock_collection.find_one.return_value = {'game_id': 100}
        result = get_next_nr_game()
        self.assertEqual(result, 101)


if __name__ == '__main__':
    unittest.main()
