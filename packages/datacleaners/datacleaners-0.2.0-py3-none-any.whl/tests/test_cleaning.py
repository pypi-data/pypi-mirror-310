# tests/test_cleaning.py
import unittest
import pandas as pd
from dataCleaner import DataCleaner

class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            "A": [1, 2, np.nan, 4, 5],
            "B": [5, 5, 6, 6, 7],
            "C": [100, 200, 300, 400, 500]
        })
        self.cleaner = DataCleaner(self.data)

    def test_handle_missing_data(self):
        self.cleaner.handle_missing_data(method="mean")
        self.assertFalse(self.cleaner.df.isnull().any().any())

    def test_drop_duplicates(self):
        self.cleaner.drop_duplicates()
        self.assertEqual(len(self.cleaner.df), 4)

    def test_normalize_columns(self):
        self.cleaner.normalize_columns(columns=["C"])
        self.assertAlmostEqual(self.cleaner.df["C"].max(), 1.0)

    def test_remove_outliers(self):
        self.cleaner.remove_outliers(column="C", method="iqr")
        self.assertTrue((self.cleaner.df["C"] <= 500).all())

if __name__ == "__main__":
    unittest.main()
