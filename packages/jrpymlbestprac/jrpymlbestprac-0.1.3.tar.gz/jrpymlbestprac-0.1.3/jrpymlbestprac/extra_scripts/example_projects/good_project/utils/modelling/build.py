"""Functions associated with training the model and converting it to an API"""

from vetiver import VetiverAPI, VetiverModel


def train_model(model, x, y):
    """Train the model using the training data

    :parameters:
    model: sklearn model or pipeline object
      Model or pipeline for training
    x: 2-D data structure
      Covariates for training
    y: 1-D data structure
      Target variable to predict

    :returns:
    Sklearn model or pipeline object after training
    """
    model.fit(x, y)
    return model


def create_deployable_model(model, input_data, model_name="vetiver-model"):
    """Convert model to a deployable model object

    :parameters:
    model: sklearn model object
      Trained model object
    input_data: 2-D data structure
      Input data covariates used to create a prototype input for the API
    model_name: str
      Identifier name for model

    :returns:
    VetiverModel object ready for deployment as an API
    """
    return VetiverModel(model, model_name, prototype_data=input_data)


def create_model_api(model):
    """Convert VetiverModel-type object into a deployable FastAPI

    :parameters:
    model: VetiverModel
      VetiverModel object constructed from a trained sklearn model

    :returns:
    VetiverAPI object ready to deploy
    """
    return VetiverAPI(model)
