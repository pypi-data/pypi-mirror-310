import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataCleaner:
    def __init__(self, dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        self.df = dataframe

    def handle_missing_data(self, method="mean", exclude_columns=None):
        """
        Handles missing data in the DataFrame.
        - method: 'mean', 'median', or 'drop'.
        - exclude_columns: List of columns to exclude from processing.
        """
        exclude_columns = exclude_columns or []
        numeric_cols = self.df.select_dtypes(include=np.number).columns.difference(exclude_columns)

        if method == "mean":
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
        elif method == "median":
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
        elif method == "drop":
            self.df.dropna(inplace=True)
        else:
            raise ValueError("Invalid method for handling missing data")
        return self.df

    def drop_duplicates(self):
        """Removes duplicate rows from the DataFrame."""
        self.df.drop_duplicates(inplace=True)
        return self.df

    def normalize_columns(self, columns=None):
        """
        Normalizes numeric columns in the DataFrame using MinMaxScaler.
        - columns: List of columns to normalize. If None, all numeric columns are normalized.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=np.number).columns
        else:
            # Ensure the specified columns are numeric
            columns = [col for col in columns if col in self.df.select_dtypes(include=np.number).columns]

        scaler = MinMaxScaler()
        self.df[columns] = scaler.fit_transform(self.df[columns])
        return self.df

    def remove_outliers(self, column, method="zscore", threshold=3):
        """
        Removes outliers from a specified column using Z-score or IQR method.
        - column: The column to process.
        - method: 'zscore' or 'iqr'.
        - threshold: Z-score threshold (default is 3).
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        if not np.issubdtype(self.df[column].dtype, np.number):
            raise ValueError(f"Column '{column}' is not numeric and cannot have outliers removed.")

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
        """Returns the cleaned DataFrame."""
        return self.df