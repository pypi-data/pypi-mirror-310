"""Functions associated with setting up the model object and the data input variables"""

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline


def extract_target_variable(data, target, covariates):
    """Extract target variable to be predicted by trained model

    :parameters:
    data: pd.DataFrame
      Pandas DataFrame with the raw data from which to select the target variable
    target: str
      String with the name of the column to set as the target variable y
    covariates: list
      List of column names to set as the covariates x

    :returns:
    Two outputs as tuple (y, X):
    - Target variable column
    - Predictor variable columns
    """
    y = data[target]
    x = data[covariates]
    return y, x


def setup_model():
    """Constucts a model object (currently LinearRegression) to use for training

    :returns:
    Sklearn model class
    """
    return LinearRegression()


def setup_pipeline(transformer, model):
    """Constructs a pipeline for data transformation and modelling

    :parameters:
    transformer: Sklearn ColumnTransformer object
      Calibrated transformer for applying scaling and one-hot encoding to data
    model: Sklean model object
      Model to be trained on data

    :returns:
    Sklearn Pipeline class including a calibrated data transformer and a model that is
    ready for training
    """
    return Pipeline(
        [
            ("transform", transformer),
            ("model", model),
        ]
    )
