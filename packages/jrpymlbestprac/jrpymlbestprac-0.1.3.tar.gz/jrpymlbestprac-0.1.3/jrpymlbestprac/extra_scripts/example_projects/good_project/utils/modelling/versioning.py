from pins import board_temp
from vetiver import vetiver_pin_write


def store_model(model):
    """Store model using a temporary pins board

    :parameters:
    model: VetiverModel
      Model to be stored

    :returns:
    Pins board where model is stored
    """
    model_board = board_temp(versioned=True, allow_pickle_read=True)
    vetiver_pin_write(model_board, model)
    return model_board
