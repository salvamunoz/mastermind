import unittest
from unittest.mock import patch
from v1.mastermindv1 import get_next_nr_game, check_guess


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


class TestCheckGuess(unittest.TestCase):
    def test_exact_match(self):
        result = check_guess("RRRR", "RRRR")
        self.assertEqual(result, (4, 0))

    def test_color_match(self):
        result = check_guess("RRBB", "BBRR")
        self.assertEqual(result, (0, 4))

    def test_no_match(self):
        result = check_guess("YYYY", "RRRR")
        self.assertEqual(result, (0, 0))

    def test_partial_match(self):
        result = check_guess("YBRY", "RBYB")
        self.assertEqual(result, (1, 2))


if __name__ == '__main__':
    unittest.main()
