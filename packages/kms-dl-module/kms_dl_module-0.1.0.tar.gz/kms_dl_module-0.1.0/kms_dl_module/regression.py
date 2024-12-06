#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv1D, Flatten, LSTM, SimpleRNN
from keras.layers import LeakyReLU, Activation

from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import seaborn as sns





class RegressionModel:
    def __init__(self, dataframe, target_variable, features=None, epochs=10, categorical=None, test_size=0.2):
        self.dataframe = dataframe
        self.target_variable = target_variable
        self.features = features if features else [col for col in dataframe.columns if col != target_variable]
        self.epochs = epochs
        self.test_size = test_size
        self.categorical = categorical
        self.label_encodings = {}
        self.dropped_columns = []
        self.dropped_rows_count = 0
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.models = {}
        self.results = pd.DataFrame()
        self.best_model_name = None
        self.best_model = None

    def data_preprocessing(self):
        """
        Handle data preprocessing:
        - Drop index and null values
        - Encode categorical variables
        - Scale numeric features
        - Split data into train/test sets
        """
        # Drop any index column if present
        if 'index' in self.dataframe.columns:
            self.dataframe = self.dataframe.drop(columns=['index'])

        # Handle null values by dropping them
        self.dataframe = self.dataframe.dropna()
        self.dropped_rows_count = len(self.dataframe)

        # Separate features and target variable
        X = self.dataframe.drop(columns=[self.target_variable])
        y = self.dataframe[self.target_variable]

        # Handle categorical variables using label encoding
        if self.categorical:
            for col in self.categorical:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col])
                self.label_encodings[col] = dict(zip(le.classes_, le.transform(le.classes_)))

        # Scale numeric columns
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        # if numeric_cols:
        if not numeric_cols.empty:
            scaler = StandardScaler()
            X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

        # Handle non-numeric or datetime features
        for col in X.columns:
            if pd.api.types.is_datetime64_any_dtype(X[col]):
                self.dropped_columns.append(col)
                X = X.drop(columns=[col])
            elif X[col].dtype == 'O':
                try:
                    X[col] = pd.to_numeric(X[col])
                except ValueError:
                    # If conversion fails and there are fewer than 100 unique values, label encode
                    if X[col].nunique() < 100:
                        le = LabelEncoder()
                        X[col] = le.fit_transform(X[col])
                        self.label_encodings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
                    else:
                        self.dropped_columns.append(col)
                        X = X.drop(columns=[col])

        # Handle target variable: Convert to numeric, drop rows with invalid target values
        try:
            y = pd.to_numeric(y)
        except ValueError:
            raise ValueError(f"Target variable {self.target_variable} cannot be converted to numeric values.")

        # Splitting into train/test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)

    def get_dropped_info(self):
        """
        Get information about dropped columns and rows during preprocessing.
        """
        print(f"Dropped rows due to null values: {self.dropped_rows_count}")
        print(f"Dropped columns: {self.dropped_columns}")

    def get_label_encodings(self):
        """
        Get the label encodings for categorical features.
        """
        print("Label Encodings:")
        for col, encodings in self.label_encodings.items():
            print(f"{col}: {encodings}")

    def train_module_regression(self):
      # Perform data preprocessing
      self.data_preprocessing()

      # Define models for each structure and activation function
      activations = ['relu', 'leaky_relu']
      layer_structures = ['L1', 'L2', 'L3']
      
      for model_type in ['MLP', 'CNN', 'RNN', 'LSTM']:  # Added LSTM here
          for activation in activations:
              for layer_structure in layer_structures:  # Use the layer structure L1, L2, L3
                  model_name = f"{model_type}_{activation.upper()}_{layer_structure}"
                  model = self.build_model(model_type, activation, layer_structure)
                  history = model.fit(self.X_train, self.y_train, epochs=self.epochs, validation_split=0.2, verbose=0)
                  self.evaluate_model(model, model_name, history)

      # Show comparison of all models
      self.display_results()

      # Display the best model
      self.display_best_model_results()


    def build_model(self, model_type, activation, layer_structure):
        """
        Build the model based on type, activation function, and layer structure.
        """
        if model_type == 'MLP':
            return self.build_mlp_model(activation, layer_structure)
        elif model_type == 'CNN':
            return self.build_cnn_model(activation, layer_structure)
        elif model_type == 'RNN':
            return self.build_rnn_model(activation, layer_structure)
        elif model_type == 'LSTM':  # Added LSTM case
            return self.build_lstm_model(activation, layer_structure)


    # MLP Model
    def build_mlp_model(self, activation, layer_structure):
        model = Sequential()
        input_shape = (self.X_train.shape[1],)

        # Handle activation function choices
        activation_layer = LeakyReLU(alpha=0.1) if activation == 'leaky_relu' else Activation('relu')

        # MLP structure based on layer structure
        model.add(Dense(128, input_shape=input_shape))
        model.add(activation_layer)
        
        if layer_structure == 'L2':
            model.add(Dense(64))
            model.add(activation_layer)
        elif layer_structure == 'L3':
            model.add(Dense(64))
            model.add(activation_layer)
            model.add(Dense(32))
            model.add(activation_layer)

        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=Adam(), loss='mean_squared_error')
        return model

    # CNN Model
    def build_cnn_model(self, activation, layer_structure):
        model = Sequential()
        input_shape = (self.X_train.shape[1], 1)

        # Handle activation function choices
        activation_layer = LeakyReLU(alpha=0.1) if activation == 'leaky_relu' else Activation('relu')

        model.add(Conv1D(64, kernel_size=2, activation='relu', input_shape=input_shape))
        model.add(Flatten())

        if layer_structure == 'L2':
            model.add(Dense(64))
            model.add(activation_layer)
        elif layer_structure == 'L3':
            model.add(Dense(64))
            model.add(activation_layer)
            model.add(Dense(32))
            model.add(activation_layer)

        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=Adam(), loss='mean_squared_error')
        return model


    def build_rnn_model(self, activation, layer_structure):
        model = Sequential()
        input_shape = (self.X_train.shape[1], 1)
    
        # Handle activation function choices
        activation_layer = LeakyReLU(alpha=0.1) if activation == 'leaky_relu' else Activation('relu')
    
        # Building the RNN structure based on layer_structure
        if layer_structure == 'L1':
            model.add(SimpleRNN(64, input_shape=input_shape, return_sequences=False))
            
        elif layer_structure == 'L2':
            model.add(SimpleRNN(64, input_shape=input_shape, return_sequences=True))
            model.add(SimpleRNN(32, return_sequences=False))
            
        elif layer_structure == 'L3':
            model.add(SimpleRNN(128, input_shape=input_shape, return_sequences=True))
            model.add(SimpleRNN(64, return_sequences=True))
            model.add(SimpleRNN(32, return_sequences=False))
        
        # Adding the activation layer
        model.add(Dense(64))
        model.add(activation_layer)
    
        model.add(Dense(1, activation='linear'))  # Final output layer for regression
        model.compile(optimizer=Adam(), loss='mean_squared_error')
        
        return model

    # LSTM Model (Newly Added)
    def build_lstm_model(self, activation, layer_structure):
        model = Sequential()
        input_shape = (self.X_train.shape[1], 1)

        # Handle activation function choices
        activation_layer = LeakyReLU(alpha=0.1) if activation == 'leaky_relu' else Activation('relu')

        model.add(LSTM(64, input_shape=input_shape, return_sequences=False))

        if layer_structure == 'L2':
            model.add(Dense(64))
            model.add(activation_layer)
        elif layer_structure == 'L3':
            model.add(Dense(64))
            model.add(activation_layer)
            model.add(Dense(32))
            model.add(activation_layer)

        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=Adam(), loss='mean_squared_error')
        return model


    def evaluate_model(self, model, model_name, history):
        """
        Evaluate the model, calculate metrics, and store the results.
        """
        y_pred = model.predict(self.X_test)
    
        # Ensure y_pred is one-dimensional
        if y_pred.ndim > 1:
            y_pred = y_pred.flatten()
    
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)
        adj_r2 = 1 - (1 - r2) * (len(self.y_test) - 1) / (len(self.y_test) - self.X_test.shape[1] - 1)
        mape = np.mean(np.abs((self.y_test - y_pred) / self.y_test)) * 100
        smape = 100 * np.mean(2 * np.abs(y_pred - self.y_test) / (np.abs(self.y_test) + np.abs(y_pred)))
    
        self.models[model_name] = model
    
        # Store results in DataFrame for comparison
        results_df = pd.DataFrame([{
            'Model': model_name,
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R-Squared': r2,
            'Adjusted R-Squared': adj_r2,
            'MAPE': mape,
            'SMAPE': smape
        }])

        self.results = pd.concat([self.results, results_df], ignore_index=True)
    
        # Check if this model is the best one (based on RMSE for now)
        if self.best_model is None or rmse < self.results['RMSE'].min():
            self.best_model = model
            self.best_model_name = model_name
            self.best_history = history


    def display_results(self):
        """
        Display the comparison of all trained models based on the metrics.
        """
        print(self.results)

    def display_best_model_results(self):
        """
        Display results and plots for the best model.
        """
        print(f"Best Model: {self.best_model_name}")

        # Plot the loss curves
        plt.figure(figsize=(10, 6))
        plt.plot(self.best_history.history['loss'], label='Train Loss')
        plt.plot(self.best_history.history['val_loss'], label='Validation Loss')
        plt.title(f"Train vs Validation Loss - {self.best_model_name}")
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

        # Residuals Histogram
        y_pred = self.best_model.predict(self.X_test)
        residuals = self.y_test - y_pred.reshape(-1)
        sns.histplot(residuals, kde=True)
        plt.title("Residuals Distribution")
        plt.show()

        # Predicted vs Actual Plot
        plt.figure(figsize=(8, 6))
        plt.scatter(self.y_test, y_pred)
        plt.title(f"Predicted vs Actual - {self.best_model_name}")
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.plot([min(self.y_test), max(self.y_test)], [min(self.y_test), max(self.y_test)], color='red')
        plt.show()

    def evaluate(self, model_name):
        """
        Evaluate and plot the graphs for a specific model chosen by the user.
        """
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return

        model = self.models[model_name]
        y_pred = model.predict(self.X_test)
        y_pred = y_pred.flatten()
        y_test = self.y_test.values.flatten()

        # Print Metrics
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)
        adj_r2 = 1 - (1-r2)*(len(self.y_test)-1)/(len(self.y_test)-self.X_test.shape[1]-1)
        mape = np.mean(np.abs((self.y_test - y_pred) / self.y_test)) * 100
        smape = 100 * np.mean(2 * np.abs(y_pred - self.y_test) / (np.abs(self.y_test) + np.abs(y_pred)))

        print(f"Metrics for {model_name}:")
        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"RMSE: {rmse}")
        print(f"R-Squared: {r2}")
        print(f"Adjusted R-Squared: {adj_r2}")
        print(f"MAPE: {mape}")
        print(f"SMAPE: {smape}")

        # Plotting same graphs for the selected model
        residuals = self.y_test - y_pred.reshape(-1)
        sns.histplot(residuals, kde=True)
        plt.title(f"Residuals Distribution - {model_name}")
        plt.show()

        plt.figure(figsize=(8, 6))
        plt.scatter(self.y_test, y_pred)
        plt.title(f"Predicted vs Actual - {model_name}")
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.plot([min(self.y_test), max(self.y_test)], [min(self.y_test), max(self.y_test)], color='red')
        plt.show()

    def save_model(self, model_name, path='.'):
        """
        Save the model by model name.
        """
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return

        model = self.models[model_name]
        model.save(f"{path}/{model_name}.h5")
        print(f"Model {model_name} saved at {path}/{model_name}.h5")

    def save_best_model(self, path='.'):
        """
        Save the best model.
        """
        if self.best_model:
            self.best_model.save(f"{path}/{self.best_model_name}.h5")
            print(f"Best model {self.best_model_name} saved at {path}/{self.best_model_name}.h5")



