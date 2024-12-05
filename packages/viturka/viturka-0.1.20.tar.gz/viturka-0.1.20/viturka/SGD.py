from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np
from fastFM import sgd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix, hstack

def generate_synthetic_dataset(df, numerical_columns, categorical_columns, target_column, synthetic_ratio=1.0):
    """
    Generates synthetic data to augment the dataset using SMOTE for numerical data
    and random sampling for categorical columns.
    """
    # Separate numerical and categorical features
    numerical_data = df[numerical_columns]
    categorical_data = df[categorical_columns]
    target_data = df[target_column]

    # Apply SMOTE for numerical data
    smote = SMOTE(sampling_strategy=synthetic_ratio, random_state=42)
    X_num_resampled, y_resampled = smote.fit_resample(numerical_data, target_data)

    # Generate synthetic categorical data by random sampling
    num_synthetic_samples = len(X_num_resampled) - len(numerical_data)
    if num_synthetic_samples > 0:
        synthetic_categorical_data = categorical_data.sample(
            n=num_synthetic_samples, replace=True, random_state=42
        ).reset_index(drop=True)

        # Combine synthetic numerical and categorical data
        synthetic_data = pd.DataFrame(X_num_resampled[len(numerical_data):], columns=numerical_columns)
        synthetic_data[categorical_columns] = synthetic_categorical_data
        synthetic_data[target_column] = y_resampled[len(target_data):]

        # Concatenate with the original dataset
        augmented_data = pd.concat([df, synthetic_data], ignore_index=True)
    else:
        augmented_data = df

    return augmented_data

def model(file, target_column, numerical_columns, categorical_columns, n_iter=100, rank=8, init_stdev=0.01, step_size= 0.001, l2_reg_w=0.1, l2_reg_V=0.1, test_size=0.2, generate_synthetic_data= False):
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
        df = generate_synthetic_dataset(df, numerical_columns, categorical_columns, target_column)


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
    
