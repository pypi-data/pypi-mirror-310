from utils.data import (
    calibrate_transformer,
    clean_data,
    fetch_data,
    save_data,
    load_data,
)
from utils.modelling import (
    create_deployable_model,
    create_model_api,
    cross_validation,
    extract_target_variable,
    generate_report_template,
    setup_model,
    setup_pipeline,
    store_model,
    train_model,
)
# from utils.deployment import deploy_locally, generate_dockerfile

# Fetch and store the data
data = fetch_data()
save_data(data)

# Load raw data
data = load_data()

# Clean data
data = clean_data(data)

# Extract target and covariates
target = "body_mass_g"
covariates = [
    "species",
    "island",
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "sex",
]
y, x = extract_target_variable(data, target, covariates)

# Set up model pipeline
numerical_features = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
]
categorical_features = ["species", "island", "sex"]
transfomer = calibrate_transformer(x, numerical_features, categorical_features)
model = setup_model()
model = setup_pipeline(transfomer, model)

# Train the model and generate scores
model = train_model(model, x, y)
scores = cross_validation(model, x, y)
print(scores)

# Build deployable model API
model_name = "vetiver-model"
v_model = create_deployable_model(model, x, model_name)
app = create_model_api(v_model)

# Generate model report
generate_report_template()

# Store and version the model
model_board = store_model(v_model)

# Generate a model dockerfile for cloud deployment
# generate_dockerfile(model_board, model_name)

# Deploy model API locally
# deploy_locally(app)
