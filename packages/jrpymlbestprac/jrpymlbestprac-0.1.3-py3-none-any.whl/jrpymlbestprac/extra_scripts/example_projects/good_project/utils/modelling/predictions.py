"""Functions involved in generating model predictions using either the sklearn model or
API (if deployed)"""

from vetiver.server import predict, vetiver_endpoint


def model_predict(model, data):
    """Get predictions from model

    :parameters:
    model: sklearn model or pipeline object
      Trained sklearn model or pipeline ready for predictions
    data: 2-D data structure
      Untransformed input data for predictions

    :returns:
    1-D data structure with the model predictions
    """
    return model.predict(data)


def api_predict(endpoint_url, input_data):
    """Get predictions from API at endpoint

    :parameters:
    endpoint_url: str
      Endpoint URL for model
    input_data: Pandas DataFrame
      Untransformed input data for predictions
    covariates: list
      List of column names for data covariates

    :returns:
    1-D data structure with the API predictions
    """
    endpoint = vetiver_endpoint(endpoint_url)
    return predict(endpoint, input_data)
