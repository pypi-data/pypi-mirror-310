from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np
from fastFM import sgd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix, hstack
from sklearn.utils import resample

def generate_synthetic_dataset(
    df,
    numerical_columns,
    categorical_columns,
    target_column,
    synthetic_ratio=1.0,
    noise_level=0.01
):
    """
    Generate synthetic data with better distribution control to minimize error.

    Parameters:
        df (pd.DataFrame): Original dataset.
        numerical_columns (list): Numerical column names.
        categorical_columns (list): Categorical column names.
        target_column (str): Target column name.
        synthetic_ratio (float): Ratio of synthetic data to original data.
        noise_level (float): Noise level for numerical data.

    Returns:
        pd.DataFrame: Dataset with synthetic samples.
    """
    df = df.dropna().reset_index(drop=True)

    num_synthetic_samples = int(len(df) * synthetic_ratio)
    if num_synthetic_samples <= 0:
        return df

    # Generate synthetic samples by resampling
    synthetic_data = resample(df, n_samples=num_synthetic_samples, random_state=42, replace=True)

    # Preserve correlations by adding small, scaled noise
    for col in numerical_columns:
        col_range = df[col].max() - df[col].min()
        noise = np.random.normal(0, noise_level * col_range, size=num_synthetic_samples)
        synthetic_data[col] += noise

    # Maintain categorical distributions
    for col in categorical_columns:
        value_probs = df[col].value_counts(normalize=True)  # Probability distribution of original data
        synthetic_data[col] = np.random.choice(value_probs.index, size=num_synthetic_samples, p=value_probs.values)

    # Maintain target class balance
    if pd.api.types.is_numeric_dtype(df[target_column]):
        target_range = df[target_column].max() - df[target_column].min()
        target_noise = np.random.normal(0, noise_level * target_range, size=num_synthetic_samples)
        synthetic_data[target_column] += target_noise
    else:
        target_probs = df[target_column].value_counts(normalize=True)
        synthetic_data[target_column] = np.random.choice(target_probs.index, size=num_synthetic_samples, p=target_probs.values)

    # Combine original and synthetic data
    augmented_data = pd.concat([df, synthetic_data], ignore_index=True)
    return augmented_data

def model(file, target_column, numerical_columns, categorical_columns, n_iter=100, rank=8, init_stdev=0.01, step_size= 0.001, l2_reg_w=0.1, l2_reg_V=0.1, test_size=0.2, generate_synthetic_data= False, synthetic_ratio=1.0):
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

    if generate_synthetic_data:
        df = generate_synthetic_dataset(df, numerical_columns, categorical_columns, target_column, synthetic_ratio=synthetic_ratio)


    # Target variable
    y = df[target_column].astype(float)

    scaler = MinMaxScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    # Combine categorical and numerical features
    v = DictVectorizer(sparse=True)
    categorical_features = v.fit_transform(df[categorical_columns].to_dict(orient='records'))
    numerical_features = csr_matrix(df[numerical_columns].values)

    # Concatenate categorical and numerical features
    X = hstack([categorical_features, numerical_features])

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Train a local fastFM model
    local_model = sgd.FMRegression(
        n_iter=n_iter,
        init_stdev=init_stdev,
        l2_reg_w=l2_reg_w,
        l2_reg_V=l2_reg_V,
        rank=rank,
        step_size= step_size
    )
    local_model.fit(X_train, y_train)

    return local_model, X_test, y_test, v


def adjust_features_sparse(X_test, model):
    """Adjust X_test to match the model's feature set for sparse matrices."""
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


def evaluate(local_model, X_test, y_test):
    X_test = adjust_features_sparse(X_test, local_model)
    # Predict using the trained model
    pred = local_model.predict(X_test)
    # Ensure both predictions and true values are not NaN
    valid_indices = ~np.isnan(y_test) & ~np.isnan(pred)
    y_test = y_test[valid_indices]
    pred = pred[valid_indices]
    # Calculate the mean squared error
    mse = mean_squared_error(y_test, pred)
    return pred, mse
    
