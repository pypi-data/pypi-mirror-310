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
import smogn

def generate_synthetic_dataset(df, numerical_columns, categorical_columns, target_column, sampling_percentage=0.2, noise_level=0.1):
    """
    Generates synthetic data using SMOGN for numerical data and random sampling for categorical data.
    """
    # Prepare numerical data with the target column
    numerical_df = df[numerical_columns + [target_column]].copy()

    # Define custom relevance function
    relevance_function = {
        "method": "range",  # "range" works for numeric targets with clear bounds
        "control.pts": [[df[target_column].min(), 1],
                        [df[target_column].quantile(0.5), 0],
                        [df[target_column].max(), 1]],
    }

    # Apply SMOGN to generate synthetic numerical data
    augmented_numerical_data = smogn.smoter(
        data=numerical_df,
        y=target_column,
        samp_method="balance",
        rel_method=relevance_function,
        pert=noise_level,
        under_samp=True,
    )

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

def model(file, target_column, numerical_columns, categorical_columns, n_iter=100, rank=8, init_stdev=0.01, step_size= 0.001, l2_reg_w=0.1, l2_reg_V=0.1, test_size=0.2, generate_synthetic_data= False, synthetic_ratio=1.5):
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
        df = generate_synthetic_dataset(df, numerical_columns, categorical_columns, target_column, sampling_percentage=synthetic_ratio)


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
    
