# dataCleaner/cleaning.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataCleaner:
    def __init__(self, dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        self.df = dataframe

    def handle_missing_data(self, method="mean"):
        if method == "mean":
            self.df.fillna(self.df.mean(), inplace=True)
        elif method == "median":
            self.df.fillna(self.df.median(), inplace=True)
        elif method == "drop":
            self.df.dropna(inplace=True)
        else:
            raise ValueError("Invalid method for handling missing data")
        return self.df

    def drop_duplicates(self):
        self.df.drop_duplicates(inplace=True)
        return self.df

    def normalize_columns(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include=np.number).columns
        scaler = MinMaxScaler()
        self.df[columns] = scaler.fit_transform(self.df[columns])
        return self.df

    def remove_outliers(self, column, method="zscore", threshold=3):
        if method == "zscore":
            z_scores = (self.df[column] - self.df[column].mean()) / self.df[column].std()
            self.df = self.df[np.abs(z_scores) < threshold]
        elif method == "iqr":
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            self.df = self.df[(self.df[column] >= (Q1 - 1.5 * IQR)) & (self.df[column] <= (Q3 + 1.5 * IQR))]
        else:
            raise ValueError("Invalid method for outlier removal")
        return self.df

    def get_cleaned_data(self):
        return self.df
