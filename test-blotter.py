import os
import unittest
import pandas as pd
from calcStats import calcTradeStats

class testito(unittest.TestCase):
    def setUp(self):
        i_path = os.path.realpath('SampleInput.csv')
        o_path = os.path.realpath('SampleOutput.csv')
        calcTradeStats(i_path, 'temp.csv')
        self.i_data = pd.read_csv(i_path)
        self.o_data = pd.read_csv(o_path)
        self.test_data = pd.read_csv('temp.csv')


    def test_correct_output(self):
        self.assertTrue(self.o_data.compare(self.test_data).empty)
    
    def tearDown(self) -> None:
        os.remove('temp.csv')
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()