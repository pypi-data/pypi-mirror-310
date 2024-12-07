import pandas as pd
import numpy as np
from fastFM import sgd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix, hstack
from fastFM import als
from sklearn.metrics.pairwise import cosine_similarity


def train_model(
    file,
    target_column,
    numerical_columns,
    categorical_columns,
    item_id_column,
    n_iter=100,
    rank=8,
    init_stdev=0.01,
    step_size=0.01,
    l2_reg_w=0.001,
    l2_reg_V=0.001,
    test_size=0.2,
):
    """
    Train a factorization machine (FM) model on any dataset.

    Args:
        file (str): Path to the CSV file containing the dataset.
        target_column (str): Name of the target column.
        numerical_columns (list): List of numerical feature columns.
        categorical_columns (list): List of categorical feature columns.
        item_id_column (str): Name of the column that uniquely identifies items.
        n_iter (int): Number of iterations for the FM model.
        rank (int): Rank of factorization.
        init_stdev (float): Standard deviation for initialization.
        step_size (float): Learning rate.
        l2_reg_w (float): Regularization parameter for weights.
        l2_reg_V (float): Regularization parameter for latent factors.
        test_size (float): Fraction of the dataset to be used as test data.

    Returns:
        tuple: Trained FM model, train/test data, vectorizer, target scaler, and original dataset.
    """
    # Load the dataset from CSV
    df = pd.read_csv(file).dropna()

    # Validate required columns
    required_columns = set([target_column, item_id_column] + numerical_columns + categorical_columns)
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in dataset: {missing_columns}")

    # Ensure categorical columns are strings
    df[categorical_columns] = df[categorical_columns].astype(str)

    # Ensure numerical columns are floats
    df[numerical_columns] = df[numerical_columns].astype(float)

    # Process the target variable
    y = df[target_column].astype(float)
    scaler_target = MinMaxScaler()
    y_scaled = scaler_target.fit_transform(y.values.reshape(-1, 1)).flatten()

    # Scale numerical features
    scaler = MinMaxScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    # Encode categorical features
    vectorizer = DictVectorizer(sparse=True)
    categorical_features = vectorizer.fit_transform(df[categorical_columns].to_dict(orient="records"))

    # Combine numerical and categorical features
    numerical_features = csr_matrix(df[numerical_columns].values)
    X = hstack([categorical_features, numerical_features])
    X = MaxAbsScaler().fit_transform(X)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=test_size, random_state=42)

    # Train the FM model
    model = als.FMRegression(
        n_iter=n_iter,
        init_stdev=init_stdev,
        l2_reg_w=l2_reg_w,
        l2_reg_V=l2_reg_V,
        rank=rank,
    )
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_test, vectorizer, scaler_target, df


def find_similar_items(model, dict_vectorizer, item_features, item_id, item_id_column, top_k=5):
    """
    Find top-k similar items based on FM latent feature weights.

    Args:
        model: Trained FM model.
        dict_vectorizer: DictVectorizer for categorical encoding.
        item_features (DataFrame): DataFrame containing original features.
        item_id: ID of the item to find similarities for.
        item_id_column (str): Column name for item IDs.
        top_k (int): Number of similar items to retrieve.

    Returns:
        list: Top-k similar items with similarity scores.
    """
    if item_id_column not in item_features.columns:
        raise ValueError(f"Column '{item_id_column}' not found in item_features DataFrame.")

    # Find the index of the item in the DataFrame
    item_index = item_features[item_features[item_id_column] == item_id].index[0]

    # Transform item features to vector format
    item_vector = dict_vectorizer.transform(
        item_features.iloc[item_index : item_index + 1].to_dict(orient="records")
    )

    # Compute cosine similarity with FM latent weights
    latent_weights = model.V
    item_latent_vector = latent_weights[item_vector.indices, :]
    similarities = cosine_similarity(item_latent_vector, latent_weights).flatten()

    # Get top-k similar items
    similar_indices = similarities.argsort()[::-1][: top_k + 1]  # Include itself
    similar_items = [
        (item_features.iloc[i][item_id_column], similarities[i])
        for i in similar_indices
        if i != item_index
    ]

    return similar_items[:top_k]


def evaluate_model(model, X_test, y_test, scaler_target):
    """
    Evaluate the FM model using mean squared error.

    Args:
        model: Trained FM model.
        X_test: Test feature matrix.
        y_test: Test target values.
        scaler_target: Scaler used to scale the target variable.

    Returns:
        tuple: Predicted values and mean squared error.
    """
    # Predict and inverse transform
    pred_scaled = model.predict(X_test)
    pred = scaler_target.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
    y_test = scaler_target.inverse_transform(y_test.reshape(-1, 1)).flatten()

    # Filter valid predictions
    valid_indices = ~np.isnan(y_test) & ~np.isnan(pred)
    y_test, pred = y_test[valid_indices], pred[valid_indices]

    # Compute MSE
    mse = mean_squared_error(y_test, pred)
    return pred, mse