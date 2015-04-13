from unittest import TestCase
import unittest
import poker_code

__author__ = 'tarahmarie'


class TestEvaluate(TestCase):

    def test_evaluate(self):
        data = poker_code.parse_json()
        p1 = data["hands"][0]["name"]
        p2 = data["hands"][1]["name"]
        h1 = data["hands"][0]["hand"]
        h2 = data["hands"][1]["hand"]
        h1e = poker_code.evaluate(h1)
        h2e = poker_code.evaluate(h2)
        self.assertTrue(1<= h1e <= 9)
        self.assertTrue(1<= h2e <= 9)

    def test_for_bad_data(self):
        data = poker_code.parse_json('bad_data.json')
        p1 = data["hands"][0]["name"]
        p2 = data["hands"][1]["name"]
        h1 = data["hands"][0]["hand"]
        h2 = data["hands"][1]["hand"]
        self.assertRaises(Exception, poker_code.evaluate(h1))

if "__main__" == __name__:
    unittest.main()