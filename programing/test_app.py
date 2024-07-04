import unittest
import pandas as pd
from map import preprocess_data

class TestApp(unittest.TestCase):

    def setUp(self):
        self.data_path = 'C:/Users/ramab/Downloads/programing/1976-2020-president.csv'
        self.df = pd.read_csv(self.data_path)

    def test_preprocess_data(self):
        df = preprocess_data(self.df)
        self.assertFalse(df.empty, "DataFrame should not be empty after preprocessing")
        self.assertTrue('state' in df.columns, "DataFrame should have a 'state' column")
        self.assertTrue('candidate' in df.columns, "DataFrame should have a 'candidate' column")
        self.assertTrue('party_simplified' in df.columns, "DataFrame should have a 'party_simplified' column")

if __name__ == '__main__':
    unittest.main()
