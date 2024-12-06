"""Functions for dealing with data preprocessing, including cleaning, scaling and
one-hot encoding
"""

import janitor  # noqa: F401
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def clean_data(data):
    """Remove missing values and clean up variable names

    :parameters:
    data: pd.DataFrame
      Pandas DataFrame with the data to be cleaned

    :returns:
    pd.DataFrame object with the tidy data
    """
    data.dropna(inplace=True)
    data = data.clean_names()
    return data


def calibrate_transformer(data, numerical_features, categorical_features):
    """Calibrate a data transformer using the input data

    :parameters:
    data: pd.DataFrame
      Input data used for calibrating the transformer

    :returns:
    sklearn ColumnTransformer object for applying consistent scaling and encoding to
    data
    """
    transformer = ColumnTransformer(
        [
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(drop="first"), categorical_features),
        ]
    )
    transformer.fit(data)
    return transformer


def transform_data(data, transformer):
    """ Scale and encode data using a pre-calibrated transformer

    :parameters:
    data: pd.DataFrame
      Data to be preprocessed
    transformer: sklearn ColumnTransformer
      Pre-calibrated transformer for scaling and encoding the data

    :returns:
    pd.DataFrame object with transformed data
    """
    return transformer.transform(data)
