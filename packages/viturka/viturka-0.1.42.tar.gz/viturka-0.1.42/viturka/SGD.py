from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np
from fastFM import sgd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.utils import resample
import smogn

def generate_synthetic_dataset(df, numerical_columns, categorical_columns, target_column, sampling_percentage=0.2, noise_level=0.1):
    """
    Generates synthetic data using SMOGN for numerical data and random sampling for categorical data.
    """
    # Prepare numerical data with the target column
    numerical_df = df[numerical_columns + [target_column]].copy()

    # Define control points based on target column statistics
    target_min = numerical_df[target_column].min()
    target_max = numerical_df[target_column].max()
    target_median = numerical_df[target_column].median()

    relevance_function = {
        "method": "range",
        "control.pts": [
            [target_min, 1],           # High relevance for minimum
            [target_median, 0],       # Low relevance for median
            [target_max, 1],          # High relevance for maximum
        ],
    }

    # Apply SMOGN to generate synthetic numerical data
    try:
        augmented_numerical_data = smogn.smoter(
            data=numerical_df,
            y=target_column,
            samp_method="balance",
            rel_method=relevance_function,
            pert=noise_level,
            under_samp=True,
        )
    except Exception as e:
        raise ValueError(f"SMOGN failed with error: {e}. Check target column distribution.")

    # Generate synthetic data for categorical columns
    num_synthetic_samples = len(augmented_numerical_data) - len(numerical_df)
    synthetic_categorical_data = df[categorical_columns].sample(
        n=num_synthetic_samples, replace=True, random_state=42
    ).reset_index(drop=True)

    # Add synthetic categorical data to augmented numerical data
    synthetic_data = augmented_numerical_data[len(numerical_df):].copy()
    synthetic_data[categorical_columns] = synthetic_categorical_data

    # Concatenate original data with synthetic data
    augmented_data = pd.concat([df, synthetic_data], ignore_index=True)
    return augmented_data

def model(
    file,
    target_column,
    numerical_columns,
    categorical_columns,
    n_iter=100,
    rank=8,
    init_stdev=0.01,
    step_size=0.01,
    l2_reg_w=0.001,
    l2_reg_V=0.001,
    test_size=0.2,
    generate_synthetic_data=False,
    synthetic_ratio=1.5,
    k_features=None,
):
    # Load the dataset from CSV
    df = pd.read_csv(file)
    df = df.dropna()

    # Ensure target_column, numerical_columns, and categorical_columns are in the dataset
    missing_columns = set([target_column] + numerical_columns + categorical_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in dataset: {missing_columns}")

    # Convert categorical columns to string type
    for col in categorical_columns:
        df[col] = df[col].astype(str)

    # Convert numerical columns to float type
    for col in numerical_columns:
        df[col] = df[col].astype(float)

    # Optionally generate synthetic data
    if generate_synthetic_data:
        df = generate_synthetic_dataset(
            df, numerical_columns, categorical_columns, target_column, sampling_percentage=synthetic_ratio
        )

    # Process target variable `y`
    y = df[target_column].astype(float)

    # Print target stats
    print("Original target stats:\n", df[target_column].describe())

    # Scale target variable
    scaler_target = MinMaxScaler()
    y_scaled = scaler_target.fit_transform(y.values.reshape(-1, 1)).flatten()

    # Scale numerical features
    scaler = MinMaxScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    # Combine categorical and numerical features
    v = DictVectorizer(sparse=True)
    categorical_features = v.fit_transform(df[categorical_columns].to_dict(orient="records"))
    numerical_features = csr_matrix(df[numerical_columns].values)

    # Concatenate categorical and numerical features
    X = hstack([categorical_features, numerical_features])

    # Feature selection (optional)
    if k_features:
        X, selected_features = select_features(X, y_scaled, k_features)
        print(f"Selected features indices: {selected_features}")

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=test_size, random_state=42)

    # Train a local fastFM model
    local_model = sgd.FMRegression(
        n_iter=n_iter,
        init_stdev=init_stdev,
        l2_reg_w=l2_reg_w,
        l2_reg_V=l2_reg_V,
        rank=rank,
        step_size=step_size,
    )
    local_model.fit(X_train, y_train)

    return local_model, X_test, y_test, v, scaler_target


def select_features(X, y, k_features):
    """
    Select top-k features using univariate feature selection.
    """
    selector = SelectKBest(score_func=f_regression, k=k_features)
    X_new = selector.fit_transform(X, y)
    selected_features = selector.get_support(indices=True)
    return X_new, selected_features


def adjust_features_sparse(X_test, model):
    """
    Adjust X_test to match the model's feature set for sparse matrices.
    """
    num_features = len(model.w_)
    current_features = X_test.shape[1]

    if current_features < num_features:
        padding = num_features - current_features
        padding_array = csr_matrix((X_test.shape[0], padding), dtype=X_test.dtype)
        X_test_adjusted = hstack([X_test, padding_array])
    elif current_features > num_features:
        X_test_adjusted = X_test[:, :num_features]
    else:
        X_test_adjusted = X_test

    return X_test_adjusted


def evaluate(local_model, X_test, y_test, scaler_target):
    """
    Evaluate the model using Mean Squared Error and predictions.
    """
    # Adjust features to match the model's input size
    X_test = adjust_features_sparse(X_test, local_model)

    # Predict using the trained model
    pred_scaled = local_model.predict(X_test)

    # Inverse transform predictions and true values
    pred = scaler_target.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
    y_test_original = scaler_target.inverse_transform(y_test.reshape(-1, 1)).flatten()

    # Ensure no NaN values
    valid_indices = ~np.isnan(y_test_original) & ~np.isnan(pred)
    y_test_original = y_test_original[valid_indices]
    pred = pred[valid_indices]

    # Print evaluation stats
    print(f"Predictions (original scale): {pred[:10]}")
    print(f"True values (original scale): {y_test_original[:10]}")

    # Calculate mean squared error
    mse = mean_squared_error(y_test_original, pred)
    return pred, mse


def feature_importance(local_model, vectorizer):
    """
    Compute feature importance using the weights of the FastFM model.
    """
    weights = local_model.w_
    feature_names = vectorizer.feature_names_

    # Pair feature names with weights
    feature_importance = sorted(zip(feature_names, weights), key=lambda x: abs(x[1]), reverse=True)

    print("Top Features by Importance:")
    for name, weight in feature_importance[:10]:
        print(f"{name}: {weight:.4f}")

    return feature_importance