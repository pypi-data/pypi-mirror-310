from vetiver import prepare_docker


def deploy_locally(app, port=8080):
    """Deploy the model API on the localhost

    :parameters:
    app: VetiverAPI
      Model API to be deployed
    port: int (default: 8080)
      Port number for deployment
    """
    app.run(port=port)


def generate_dockerfile(model_board, name):
    """Generates a dockerfile that can be used to deploy the model API to the chosen
    platform

    :parameters:
    model_board: pins board
      Location where model is stored
    name: str
      Identifier string for VetiverModel object
    """
    # TODO: Add model dependencies to VetiverModel object
    prepare_docker(model_board, name)
