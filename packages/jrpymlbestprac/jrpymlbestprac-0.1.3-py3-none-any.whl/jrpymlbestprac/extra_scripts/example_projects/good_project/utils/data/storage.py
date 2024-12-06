"""Functions for managing direct interactions with the raw data"""

import os
import pandas as pd
import seaborn as sns


def fetch_data():
    """Fetches toy dataset to be used for model training

    :returns:
    pd.DataFrame object with the data to be used for training
    """
    return sns.load_dataset("penguins")


def save_data(data, output="raw_data"):
    """Save data to a CSV file in the project data/ folder

    :parameters:
    data: pd.DataFrame
      Pandas DataFrame containing the data to be saved
    output: str
      Output filename (without extension) for the CSV data
    """
    filepath = construct_data_filepath(output)
    data.to_csv(filepath, index=False)


def load_data(filename="raw_data"):
    """Load raw CSV data from the project datastore

    :parameters:
    filename: str (default: "raw_data")
      Filename of the data (without the .csv extension)

    :returns:
    pd.DataFrame object with the loaded data
    """
    filepath = construct_data_filepath(filename)
    return pd.read_csv(filepath)


def construct_data_filepath(filename="raw_data"):
    """Construct filepath to data CSV file

    :parameters:
    filename: str (default: "raw_data")
      Filename of the data (without the .csv extension)

    :returns:
    str with the full filepath for loading and writing the data
    """
    file = f"{filename}.csv"
    return os.path.join("data", file)
