

from tensorflow.keras.utils import plot_model


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
import seaborn as sns 
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, precision_recall_curve
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt


class ClassificationModel:
    def __init__(self):
        # Initialize any required variables, like dropped columns or encoding mappings
        self.columns_dropped = []
        self.label_encodings = {}
        self.rows_dropped = 0
        self.models = {}
        self.metrics_results = pd.DataFrame(columns=['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'])
        self.best_model = None
        self.best_model_name = None
        self.training_histories = {}  

    def build_mlp(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds an MLP (Multi-Layer Perceptron) model.
        """
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape,)))

        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()

        if layer_structure == 'L1':
            model.add(layers.Dense(64, activation=act_func))
        elif layer_structure == 'L2':
            model.add(layers.Dense(64, activation=act_func))
            model.add(layers.Dense(32, activation=act_func))
        elif layer_structure == 'L3':
            model.add(layers.Dense(128, activation=act_func))
            model.add(layers.Dense(64, activation=act_func))
            model.add(layers.Dense(32, activation=act_func))

        model.add(layers.Dense(output_shape, activation=output_activation))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy', metrics=['accuracy'])
        return model


    def build_lstm(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Long Short-Term Memory (LSTM) model.
        """
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape, 1)))  # Reshaping input for LSTM

        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()

        if layer_structure == 'L1':
            model.add(layers.LSTM(64, activation=act_func))
        elif layer_structure == 'L2':
            model.add(layers.LSTM(64, activation=act_func, return_sequences=True))
            model.add(layers.LSTM(32, activation=act_func))
        elif layer_structure == 'L3':
            model.add(layers.LSTM(128, activation=act_func, return_sequences=True))
            model.add(layers.LSTM(64, activation=act_func))
            model.add(layers.LSTM(32, activation=act_func))

        model.add(layers.Dense(output_shape, activation=output_activation))  # Output layer

        model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy',
                    metrics=['accuracy'])
        return model


    def build_rnn(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Recurrent Neural Network (RNN) model.
        """
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape, 1)))  # Reshaping input for RNN

        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()

        if layer_structure == 'L1':
            model.add(layers.SimpleRNN(64, activation=act_func))
        elif layer_structure == 'L2':
            model.add(layers.SimpleRNN(64, activation=act_func, return_sequences=True))
            model.add(layers.SimpleRNN(32, activation=act_func))
        elif layer_structure == 'L3':
            model.add(layers.SimpleRNN(128, activation=act_func, return_sequences=True))
            model.add(layers.SimpleRNN(64, activation=act_func))
            model.add(layers.SimpleRNN(32, activation=act_func))

        model.add(layers.Dense(output_shape, activation=output_activation))  # Output layer

        model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy',
                    metrics=['accuracy'])
        return model


    def build_cnn(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Convolutional Neural Network (CNN) model.
        """
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape, 1)))  # Input shape for CNN is different (image-like structure)

        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()

        if layer_structure == 'L1':
            model.add(layers.Conv1D(32, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
        elif layer_structure == 'L2':
            model.add(layers.Conv1D(32, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
            model.add(layers.Conv1D(64, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
        elif layer_structure == 'L3':
            model.add(layers.Conv1D(64, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
            model.add(layers.Conv1D(128, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))

        model.add(layers.Flatten())  # Flatten the output for fully connected layers
        model.add(layers.Dense(64, activation=act_func))
        model.add(layers.Dense(output_shape, activation=output_activation))  # Output layer

        model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy',
                    metrics=['accuracy'])
        return model


    def preprocess_data(self, df, target_variable, features=None, categorical_cols=None):
        """
        Preprocesses the dataframe by handling missing values, scaling numeric columns,
        encoding categorical columns, and dropping unwanted columns.
        """
        # Step 1: Drop the index column if any
        if 'index' in df.columns:
            df = df.drop(columns=['index'])

        if 'id' in df.columns:
            df = df.drop(columns=['id'])

        if 'Index' in df.columns:
            df = df.drop(columns=['Index'])

        if 'ID' in df.columns:
            df = df.drop(columns=['ID'])

        if 'Id' in df.columns:
            df = df.drop(columns=['Id'])

        

        # Step 2: Drop rows with any missing values and record how many rows were dropped
        initial_rows = df.shape[0]
        df = df.dropna()
        self.rows_dropped = initial_rows - df.shape[0]

        # Step 3: Identify features if not provided, otherwise use all except target
        if features is None:
            features = [col for col in df.columns if col != target_variable]

        # Step 4: Check for and remove datetime or non-convertible object columns
        for col in features:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                self.columns_dropped.append(col)
                df = df.drop(columns=[col])

            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except ValueError:
                    unique_vals = df[col].nunique()
                    if unique_vals < 100:
                        # Label encode if fewer than 100 unique values
                        le = LabelEncoder()
                        df[col] = le.fit_transform(df[col])
                    else:
                        self.columns_dropped.append(col)
                        df = df.drop(columns=[col])

        # Step 5: Handle categorical columns if specified by user
        if categorical_cols:
            for col in categorical_cols:
                if col in df.columns:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col])

        # Step 6: Scale numeric columns (excluding the target variable)
        numeric_cols = [col for col in df.select_dtypes(include=np.number).columns.tolist() if col != target_variable]
        if numeric_cols:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        # Return the processed dataframe and feature columns
        return df, features

    def encode_target_variable(self, df, target_variable):
        """
        Encodes the target variable using label encoding if necessary.
        Stores the mapping in a dictionary.
        """
        if df[target_variable].dtype == 'object':
            le = LabelEncoder()
            df[target_variable] = le.fit_transform(df[target_variable])
            self.label_encodings[target_variable] = dict(zip(le.classes_, le.transform(le.classes_)))

        return df


    def train_module(self, df, target_variable, features=None, epochs=10, categorical_cols=None, test_size=0.2):
        """
        Main function to handle data preprocessing and model training.
        Args:
        - df: Input dataframe
        - target_variable: Name of the target column
        - features: List of feature columns (optional)
        - epochs: Number of epochs for training (default: 10)
        - categorical_cols: List of categorical columns (optional)
        - test_size: Percentage of data for test set (default: 0.2)
        """
        # Step 1: Preprocess the data
        df, features = self.preprocess_data(df, target_variable, features, categorical_cols)

        # Step 2: Encode target variable
        df = self.encode_target_variable(df, target_variable)

        # Step 3: Split data into training and test sets
        X = df[features]
        y = df[target_variable]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        print("Data Preprocessing Complete")
        print(f"Rows Dropped: {self.rows_dropped}")
        print(f"Columns Dropped: {self.columns_dropped}")
        print(f"Label Encoding for Target Variable: {self.label_encodings}")

        # Assuming df is your DataFrame and 'target' is your column name
        unique_values = y_train.unique()
        print(unique_values)

        # Placeholder for actual model training (to be added later)
        print("Model training with deep learning will happen here (placeholder).")
        print(f"Training for {epochs} epochs...")
        

        # Step 4: Determine the number of unique classes for the output layer
        num_classes = len(y.unique())
        output_activation = 'sigmoid' if num_classes == 2 else 'softmax'

        # Placeholder for actual model training
        model_names = ['MLP', 'CNN', 'RNN', 'LSTM']
        # model_names = ['CNN']
        activation_functions = ['ReLU', 'LeakyReLU']
        layer_structures = ['L1', 'L2', 'L3']  # Placeholder for actual layer structures

        # # Store test data as attributes
        # if model_name == 'RNN' or model_name == 'LSTM':
        #     self.X_test_rnn = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))  # Reshape for RNN/LSTM
        # else:
        #     self.X_test = X_test  # No reshaping for MLP/CNN

        self.X_test_rnn = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))  # Reshape for RNN/LSTM
        self.X_test = X_test  # No reshaping for MLP/CNN
        self.y_test = y_test

        # Store unique classes
        self.unique_classes = y.unique() 
        # Prepare class labels
        self.class_labels = [str(label) for label in df[target_variable].unique()]
        self.unique_classes_len = len(self.class_labels)

        # Step 5: Loop through each model, activation, and layer structure
        for model_name in model_names:
            for activation_function in activation_functions:
                for layer_structure in layer_structures:
        
                    # For RNN models, reshape the data
                    if model_name == 'RNN' or model_name == 'LSTM':
                        # Reshape data to (samples, timesteps=1, features)
                        X_train_rnn = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))    
                        X_test_rnn = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))  
                        input_shape = X_train_rnn.shape[2]  # Get the number of features (features count)

                        
                        # Build the RNN model
                        model = self.build_model(model_name, activation_function, layer_structure, input_shape=input_shape, output_shape=num_classes, output_activation=output_activation)
                        model_name_string = f"{model_name}_{activation_function}_{layer_structure}"
                        
                        # Train and evaluate the RNN model
                        history = self.train_and_evaluate_model(model, X_train_rnn, y_train, X_test_rnn, y_test, epochs, model_name_string)
                    
                    else:  # For non-RNN models
                        # No need to reshape, directly use X_train and X_test
                        input_shape = X_train.shape[1]  # Number of features
                        model = self.build_model(model_name, activation_function, layer_structure, input_shape=input_shape, output_shape=num_classes, output_activation=output_activation)
                        model_name_string = f"{model_name}_{activation_function}_{layer_structure}"
                        
                        # Train and evaluate the non-RNN model
                        history = self.train_and_evaluate_model(model, X_train, y_train, X_test, y_test, epochs, model_name_string)
        
                    # Store the model
                    self.models[model_name_string] = model

        # Display results after all models are trained
        print(self.metrics_results)

        # Identify the best model based on accuracy
        self.best_model_name = self.metrics_results.sort_values('Accuracy', ascending=False).iloc[0]['Model']
        self.best_model = self.models[self.best_model_name]
        print(f"\nBest Model: {self.best_model_name}")

        # Plot results for the best model
        self.plot_results_for_best_model(self.best_model_name)

    def build_model(self, model_name, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds the desired deep learning model architecture based on the provided model type, activation function, and layer structure.
        """
        if model_name == 'MLP':
            return self.build_mlp(activation_function, layer_structure, input_shape, output_shape, output_activation)
        elif model_name == 'CNN':
            return self.build_cnn(activation_function, layer_structure, input_shape, output_shape, output_activation)
        elif model_name == 'RNN':
            return self.build_rnn(activation_function, layer_structure, input_shape, output_shape, output_activation)
        elif model_name == 'LSTM':
            return self.build_lstm(activation_function, layer_structure, input_shape, output_shape, output_activation)


    def build_mlp(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds an MLP (Multi-Layer Perceptron) model.
        """
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape,)))

        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()

        if layer_structure == 'L1':
            model.add(layers.Dense(64, activation=act_func))
        elif layer_structure == 'L2':
            model.add(layers.Dense(64, activation=act_func))
            model.add(layers.Dense(32, activation=act_func))
        elif layer_structure == 'L3':
            model.add(layers.Dense(128, activation=act_func))
            model.add(layers.Dense(64, activation=act_func))
            model.add(layers.Dense(32, activation=act_func))

        model.add(layers.Dense(output_shape, activation=output_activation))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy', metrics=['accuracy'])
        return model


    



    
    
    def build_cnn(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Convolutional Neural Network (CNN) model.
        """
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape, 1)))  # Input shape for CNN is different (image-like structure)
    
        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()
    
        if layer_structure == 'L1':
            model.add(layers.Conv1D(32, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
        elif layer_structure == 'L2':
            model.add(layers.Conv1D(32, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
            model.add(layers.Conv1D(64, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
        elif layer_structure == 'L3':
            model.add(layers.Conv1D(64, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
            model.add(layers.Conv1D(128, kernel_size=3, activation=act_func))
            model.add(layers.MaxPooling1D(pool_size=2))
    
        model.add(layers.Flatten())  # Flatten the output for fully connected layers
        model.add(layers.Dense(64, activation=act_func))
        model.add(layers.Dense(output_shape, activation=output_activation))  # Output layer
    
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy',
                      metrics=['accuracy'])
        return model



    def train_and_evaluate_model(self, model, X_train, y_train, X_test, y_test, epochs, model_name):
        """
        Trains the model and evaluates it. Stores evaluation metrics.
        """
        history = model.fit(X_train, y_train, epochs=epochs, validation_split=0.2, verbose=1)
        self.training_histories[model_name] = history 
    
        # Predictions and evaluation
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1) if y_pred.shape[1] > 1 else (y_pred > 0.5).astype("int32")
        # y_pred = model.predict(X_test)
        # y_pred_classes = np.argmax(y_pred, axis=1) if y_pred.shape[1] > 1 else (y_pred > 0.5).astype("int32")
        y_pred_proba = model.predict(X_test)  # Change here
    
        accuracy = accuracy_score(y_test, y_pred_classes)
        precision = precision_score(y_test, y_pred_classes, average='weighted')
        recall = recall_score(y_test, y_pred_classes, average='weighted')
        f1 = f1_score(y_test, y_pred_classes, average='weighted')
        # roc_auc = roc_auc_score(y_test, y_pred_proba, average='weighted', multi_class='ovo' if y_test.nunique() > 2 else 'raise')

        # ROC-AUC calculation
        if y_pred_proba.shape[1] > 1:  # Multi-class
            roc_auc = roc_auc_score(y_test, y_pred_proba, average='weighted', multi_class='ovo')
        else:  # Binary
            roc_auc = roc_auc_score(y_test, y_pred_proba)
    
        # Store the results

        new_row = pd.DataFrame({    
            'Model': [model_name],     
            'Accuracy': [accuracy],     
            'Precision': [precision],    
            'Recall': [recall],     
            'F1-Score': [f1],     
            'ROC-AUC': [roc_auc]    
        })

        self.metrics_results = pd.concat([self.metrics_results, new_row], ignore_index=True)

    
        return history

    def plot_results_for_best_model(self, best_model_name):
        """
        Plots the results (loss, accuracy, confusion matrix, etc.) for the best model.
        """
        if best_model_name not in self.models:
            print(f"Model {best_model_name} not found.")
            return
        
        best_model = self.models[best_model_name]
    
        # Plot the model's layer structure (Architecture)
        # self.plot_model_architecture(best_model, best_model_name)
    
        # Instead of using best_model_name, use best_model to access layers
        layers = best_model.layers
        plt.figure(figsize=(8, 3))
        for i, layer in enumerate(layers):
            plt.text(0.5, 1 - (i + 1) * 0.1, layer.name, fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
        plt.axis('off')
        plt.title(f'{best_model_name} Architecture')
        plt.show()

        
        # Plot the model's training history (Loss curve, Accuracy curve)
        history = self.training_histories[best_model_name]
    
        # Loss Curve
        plt.figure(figsize=(10, 6))
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title(f'{best_model_name} Loss Curve')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
    
        # Accuracy Curve
        plt.figure(figsize=(10, 6))
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title(f'{best_model_name} Accuracy Curve')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()
    
        # Confusion Matrix
        # y_pred = best_model.predict(self.X_test)
        # y_pred_classes = y_pred.argmax(axis=1)

        # Make predictions
        if 'RNN' in best_model_name or 'LSTM' in best_model_name:
            # Use reshaped X_test for RNN/LSTM
            y_pred = best_model.predict(self.X_test_rnn)
        else:
            # Use original X_test for MLP/CNN
            y_pred = best_model.predict(self.X_test)
    
        y_pred_classes = y_pred.argmax(axis=1)

        
        
        
        
        conf_matrix = confusion_matrix(self.y_test, y_pred_classes)
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title(f'{best_model_name} Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
    


        # ROC-AUC Curve
        if len(self.unique_classes) == 2:  # For binary classification
            y_pred_prob = y_pred[:, 1]  # Get the probability for the positive class
            fpr, tpr, _ = roc_curve(self.y_test, y_pred_prob)
            
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, label='ROC Curve')
            plt.title(f'ROC Curve for {best_model_name}')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.show()
    
            # Precision-Recall Curve
            precision, recall, _ = precision_recall_curve(self.y_test, y_pred_prob)
            plt.figure(figsize=(8, 6))
            plt.plot(recall, precision, label='Precision-Recall Curve')
            plt.title(f'Precision-Recall Curve for {best_model_name}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.legend()
            plt.show()
        else:  # For multi-class classification
            # Compute Precision-Recall for each class
            plt.figure(figsize=(8, 6))
            for i in range(len(self.unique_classes)):
                fpr, tpr, _ = roc_curve(self.y_test == self.unique_classes[i], y_pred[:, i])
                plt.plot(fpr, tpr, label=f'Class {self.unique_classes[i]}')
    
            plt.title(f'ROC Curve for {best_model_name}')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.show()
            
            for i in range(len(self.unique_classes)):
                precision, recall, _ = precision_recall_curve(self.y_test == self.unique_classes[i], y_pred[:, i])
                plt.plot(recall, precision, label=f'Class {self.unique_classes[i]}')
    
            plt.title(f'Precision-Recall Curve for {best_model_name}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.legend()
            plt.show()
        

    # 


    def evaluate(self, model_name):
        """
        Allows the user to evaluate a specific model and see the plots.
        """
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return
        
        model = self.models[model_name]
    
        # Display model architecture
        layers = model.layers
        plt.figure(figsize=(8, 3))
        for i, layer in enumerate(layers):
            plt.text(0.5, 1 - (i + 1) * 0.1, layer.name, fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
        plt.axis('off')
        plt.title(f'{model_name} Architecture')
        plt.show()
    
        # Replot graphs and display metrics
        print(f"Evaluating {model_name}...")
        

        if 'RNN' in model_name or 'LSTM' in model_name:
            # Convert DataFrame to NumPy array and reshape for RNN/LSTM
            X_test_model = self.X_test.to_numpy().reshape((self.X_test.shape[0], 1, self.X_test.shape[1]))
        else:
            # Use original X_test for MLP/CNN
            X_test_model = self.X_test


    
        # Evaluate the model and print the classification report
        y_pred = model.predict(X_test_model)
        
        # Handle multi-class and binary classification
        if len(self.class_labels) == 2:  # For binary classification
            y_pred_classes = y_pred.argmax(axis=1)
            y_pred_prob = y_pred[:, 1]  # Get the probability for the positive class
        else:  # For multi-class classification
            y_pred_classes = y_pred.argmax(axis=1)
        
        report = classification_report(self.y_test, y_pred_classes, target_names=self.class_labels)
        print(report)
    
        # Confusion Matrix
        conf_matrix = confusion_matrix(self.y_test, y_pred_classes)
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title(f'{model_name} Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
    
        # ROC-AUC Curve
        if len(self.class_labels) == 2:  # For binary classification
            fpr, tpr, _ = roc_curve(self.y_test, y_pred_prob)
            roc_auc = auc(fpr, tpr)
            
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, label=f'ROC Curve (area = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], 'r--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'{model_name} ROC-AUC Curve')
            plt.legend(loc="lower right")
            plt.show()
    
            # Precision-Recall Curve
            precision, recall, _ = precision_recall_curve(self.y_test, y_pred_prob)
            
            plt.figure(figsize=(8, 6))
            plt.plot(recall, precision, label='Precision-Recall Curve')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title(f'{model_name} Precision-Recall Curve')
            plt.legend()
            plt.show()
        
        else:  # For multi-class classification
            # Compute ROC-AUC for each class
            plt.figure(figsize=(8, 6))
            for i in range(len(self.unique_classes)):
                fpr, tpr, _ = roc_curve(self.y_test == self.unique_classes[i], y_pred[:, i])
                plt.plot(fpr, tpr, label=f'Class {self.unique_classes[i]}')
    
            plt.title(f'ROC Curve for {model_name}')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.show()
    
            # Compute Precision-Recall for each class
            plt.figure(figsize=(8, 6))
            for i in range(len(self.unique_classes)):
                precision, recall, _ = precision_recall_curve(self.y_test == self.unique_classes[i], y_pred[:, i])
                plt.plot(recall, precision, label=f'Class {self.unique_classes[i]}')
    
            plt.title(f'Precision-Recall Curve for {model_name}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.legend()
            plt.show()
            
        


    def plot_model_architecture(self, model, model_name):
        """
        Plot the architecture of the given model without saving to a file.
        """
        plt.figure(figsize=(10, 8))
        plot_model(model, show_shapes=True, show_layer_names=True)
        
        plt.title(f'{model_name} Architecture')
        plt.axis('off')
        plt.show()


    def save_model(self, model_name, path=None):
        """
        Saves the model to the specified path. If no path is provided, saves it to the current directory.
        """
        model = self.models.get(model_name, None)
        if model is not None:
            if path is None:
                path = f"{model_name}.h5"
            model.save(path)
            print(f"Model {model_name} saved at {path}.")
        else:
            print(f"Model {model_name} not found.")


   

    def build_rnn(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Recurrent Neural Network (RNN) model.
        """
        inputs = layers.Input(shape=(1, input_shape))  # Reshaping input for RNN
        
        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()
        
        if layer_structure == 'L1':
            x = layers.SimpleRNN(64, activation=act_func)(inputs)
        elif layer_structure == 'L2':
            x = layers.SimpleRNN(64, activation=act_func, return_sequences=True)(inputs)
            x = layers.SimpleRNN(32, activation=act_func)(x)
        elif layer_structure == 'L3':
            x = layers.SimpleRNN(128, activation=act_func, return_sequences=True)(inputs)
            x = layers.SimpleRNN(64, activation=act_func, return_sequences=True)(x)
            x = layers.SimpleRNN(32, activation=act_func)(x)
        
        outputs = layers.Dense(output_shape, activation=output_activation)(x)
        
        model = models.Model(inputs=inputs, outputs=outputs)
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy',
                      metrics=['accuracy'])
        return model

    def build_lstm(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Long Short-Term Memory (LSTM) model.
        """
        inputs = layers.Input(shape=(1, input_shape)) 
        
        # model = models.Sequential()
        # model.add(layers.InputLayer(input_shape=(input_shape, 1)))  # Reshaping input for LSTM
    
        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()
    
        if layer_structure == 'L1':            
            x = layers.LSTM(64, activation=act_func)(inputs)
        elif layer_structure == 'L2':
            x = layers.LSTM(64, activation=act_func, return_sequences=True)(inputs)
            x = layers.LSTM(32, activation=act_func)(x)
        elif layer_structure == 'L3':
            x = layers.LSTM(128, activation=act_func, return_sequences=True)(inputs)
            x = layers.LSTM(64, activation=act_func, return_sequences=True)(x)
            x = layers.LSTM(32, activation=act_func)(x)

        outputs = layers.Dense(output_shape, activation=output_activation)(x)
    
        model = models.Model(inputs=inputs, outputs=outputs)
    
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy' if output_activation == 'softmax' else 'binary_crossentropy',
                      metrics=['accuracy'])
        return model


