
# Import necessary libraries
import pandas as pd
import numpy as np

import seaborn as sns
import re
import nltk
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline

from tensorflow import keras
from tensorflow.keras import layers, models


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D, SimpleRNN, LSTM, GRU
from tensorflow.keras.layers import Activation, LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.metrics import roc_curve, precision_recall_curve, auc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

nltk.download('punkt_tab') 

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


# Define the main class
class TextClassificationModel:
    def __init__(self, dataframe, target_variable, features=None, epochs=10, categorical_cols=None,
                 text_columns=None, test_size=0.2):
        self.df = dataframe
        self.target_variable = target_variable
        self.features = features
        self.epochs = epochs
        self.categorical_cols = categorical_cols
        self.text_columns = text_columns
        self.test_size = test_size
        self.columns_dropped = []
        self.label_encoder_dict = {}
        self.rows_dropped = 0
        self.models = {}
        self.vectorized_dfs = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.target_classes = None
        self.models = {}
        self.results_df = pd.DataFrame()
        self.best_model = None
        self.best_model_name = ""
        self.best_metrics = {}

    def train_module(self):
        # Step 1: Data preprocessing
        print("DataFrame columns:", self.df.columns.tolist())
        print("Text columns:", self.text_columns)
        self.data_preprocessing()

        # Step 2: Convert text columns to vectors using BOW and TF-IDF
        self.text_vectorization()

        # Step 3: Split the dataset
        self.split_data()

        self.target_classes = np.unique(self.y_train)

        self.build_and_train_models()

        # You can add more steps for model training and evaluation here as needed.

    def data_preprocessing(self):
        """
        Function to preprocess data: Handle missing values, numeric scaling, label encoding, and text processing.
        """
        # Step 1: Drop the index and rows with null values
        if 'index' in self.df.columns:
            self.df = self.df.drop(columns=['index'])

        initial_rows = self.df.shape[0]
        self.df = self.df.dropna()
        self.rows_dropped = initial_rows - self.df.shape[0]

        # Step 2: Preprocess text columns
        print("DataFrame columns:", self.df.columns.tolist())
        print("Text columns:", self.text_columns)

        # if self.text_columns:
        #     self.df[self.text_columns] = self.df[self.text_columns].applymap(self.text_preprocessing)

        if self.text_columns:
            for text_col in self.text_columns:
                self.df[text_col] = self.df[text_col].apply(self.text_preprocessing)


        # Step 3: Identify feature columns if not provided
        if self.features is None:
            self.features = [col for col in self.df.columns if col != self.target_variable]

        # Step 4: Drop datetime columns, handle categorical/object columns, and scale numeric features
        self.df, self.features = self.handle_feature_columns(self.df, self.features)

        # Step 5: Label encode target variable if necessary
        self.df[self.target_variable], self.label_encoder_dict = self.label_encode_target(self.df[self.target_variable])
        print(f"Target encoding: {self.label_encoder_dict}")

    def handle_feature_columns(self, df, features):
        """
        Function to handle feature columns: Scale numeric columns, encode categorical columns, and drop invalid columns.
        """
        for col in features.copy():
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                self.columns_dropped.append(col)
                df = df.drop(columns=[col])
                features.remove(col)

            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except ValueError:
                    unique_vals = df[col].nunique()
                    if unique_vals < 100 and (self.categorical_cols and col in self.categorical_cols):
                        le = LabelEncoder()
                        df[col] = le.fit_transform(df[col])
                    # else:
                    #     self.columns_dropped.append(col)
                    #     df = df.drop(columns=[col])
                    #     features.remove(col)

        # Scale numeric features
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        return df, features

    def label_encode_target(self, target_col):
        """
        Function to encode the target variable and store mappings.
        """
        le = LabelEncoder()
        encoded = le.fit_transform(target_col)
        label_encoder_dict = dict(zip(le.classes_, le.transform(le.classes_)))
        return encoded, label_encoder_dict

    def text_preprocessing(self, text):
        """
        Function to preprocess text data by expanding contractions, removing special characters,
        and performing lemmatization.
        """
        # Expand contractions (you can use contractions package here)
        text = re.sub(r"’", "'", text)

        # Remove URLs, HTML tags, punctuation, and special symbols
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^\w\s]', '', text)

        # Tokenize and lowercase
        text = text.lower()
        tokens = nltk.word_tokenize(text)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

        # Perform lemmatization
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(tokens)

   
    def text_vectorization(self):
        """
        Function to convert text columns into vectors using BOW and TF-IDF with both 1-gram and 2-gram.
        """
        vectorizers = {
            'BOW_1gram': CountVectorizer(ngram_range=(1, 1)),
            'BOW_2gram': CountVectorizer(ngram_range=(1, 2)),
            'TFIDF_1gram': TfidfVectorizer(ngram_range=(1, 1)),
            'TFIDF_2gram': TfidfVectorizer(ngram_range=(1, 2))
        }
    
        vectorized_dfs = []
    
        for vec_name, vec in vectorizers.items():
            for text_col in self.text_columns:
                # Fit and transform each text column separately, store vectorized DataFrame
                vectorized = vec.fit_transform(self.df[text_col])
                df_vectorized = pd.DataFrame(vectorized.toarray(), columns=vec.get_feature_names_out())
                self.vectorized_dfs[f"{vec_name}_{text_col}"] = df_vectorized
                vectorized_dfs.append(df_vectorized)
    
        # Concatenate all vectorized DataFrames with the original DataFrame
        if vectorized_dfs:
            self.df = pd.concat([self.df.reset_index(drop=True)] + vectorized_dfs, axis=1)
    
        # Drop original text columns to avoid confusion
        self.df.drop(columns=self.text_columns, inplace=True, errors='ignore')

        self.features = self.df.columns[self.df.columns != self.target_variable].tolist()


    def split_data(self):
        """
        Function to split data into training and testing sets based on user-defined or default test size.
        """
        X = self.df[self.features]
        # y = self.df[self.target_variable]
        y = self.df[self.target_variable].values.ravel() 

        # Use train_test_split from sklearn
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)
        print(f"Training data shape: {self.X_train.shape}")
        print(f"Test data shape: {self.X_test.shape}")
        return self.X_train, self.X_test, self.y_train, self.y_test


    def build_and_train_models(self):
        """
        Build, train, and evaluate CNN, RNN, LSTM, and GRU models with ReLU and LeakyReLU activations.
        """
        activations = ['relu', 'leaky_relu']
        layer_structures = ['L1', 'L2', 'L3']
        models_to_build = ['CNN', 'RNN', 'LSTM']
        # models_to_build = ['CNN']
        vectorization_techniques = ['BOW_1gram', 'BOW_2gram', 'TFIDF_1gram', 'TFIDF_2gram']

        self.X_test_rnn = self.X_test.values.reshape((self.X_test.shape[0], 1, self.X_test.shape[1]))  # Reshape for RNN/LSTM
        # self.X_test = X_test  # No reshaping for MLP/CNN
        # self.y_test = y_test
        output_shape = len(np.unique(self.y_train))
        output_activation = 'sigmoid' if output_shape > 2 else 'softmax'

        for model_type in models_to_build:
            for activation in activations:
                for layer_structure in layer_structures:
                    for vectorization in vectorization_techniques:



                        model_name = f"{model_type}_{activation.upper()}_{layer_structure}_{vectorization}"
                        print(f"Training {model_name}...")
                        # Adjust input shape based on model type
                        if model_type in ['RNN', 'LSTM']:
                            X_train_rnn = self.X_train.values.reshape((self.X_train.shape[0], 1, self.X_train.shape[1]))    
                            # X_test_rnn = self.X_test.values.reshape((self.X_test.shape[0], 1, self.X_test.shape[1])) 
                            # self.X_test = self.X_test.values.reshape((self.X_test.shape[0], 1, self.X_test.shape[1]))   # Reshape for sequence input

                            input_shape_rnn = X_train_rnn.shape[2]  # Number of features for RNN/LSTM
                            model = self.build_model(model_type, activation, layer_structure, input_shape_rnn, output_shape, output_activation)
                            history = model.fit(X_train_rnn, self.y_train, epochs=self.epochs, validation_split=0.2, verbose=0)
                        else:
                            input_shape = self.X_train.shape[1] 
                            model = self.build_model(model_type, activation, layer_structure, input_shape, output_shape, output_activation)
                            history = model.fit(self.X_train, self.y_train, epochs=self.epochs, validation_split=0.2, verbose=0)
                        
                        self.models[model_name] = model  # Store the model
                        # self.store_metrics(model_name, self.evaluate_model(model, model_name, history))

                        self.store_metrics(model_name, self.evaluate_model(model, model_name, history), history)

        self.select_best_model()
        

                


    def build_model(self, model_name, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds the desired deep learning model architecture based on the provided model type, activation function, and layer structure.
        """
        output_shape = len(np.unique(self.y_train))
        output_activation = 'sigmoid' if output_shape > 2 else 'softmax'

        if model_name == 'CNN':
            return self.build_cnn(activation_function, layer_structure, input_shape, output_shape, output_activation)
        elif model_name == 'RNN':
            return self.build_rnn(activation_function, layer_structure, input_shape, output_shape, output_activation)
        elif model_name == 'LSTM':
            return self.build_lstm(activation_function, layer_structure, input_shape, output_shape, output_activation)


    def build_cnn(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Convolutional Neural Network (CNN) model.
        
        """
        act_func = None
        if activation_function == 'ReLU':
            act_func = tf.keras.layers.ReLU()
        elif activation_function == 'LeakyReLU':
            act_func = tf.keras.layers.LeakyReLU()
            
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape, 1)))  # Input shape for CNN is different (image-like structure)
    
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


    def build_rnn(self, activation_function, layer_structure, input_shape, output_shape, output_activation):
        """
        Builds a Recurrent Neural Network (RNN) model.
        """
        act_func = None
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
        act_func = None
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






    def evaluate_model(self, model, model_name, history):

        print("Model_name In Evaluate:")
        print(model_name)

        if 'RNN' in model_name or 'LSTM' in model_name:
            y_pred_prob = model.predict(self.X_test_rnn)  # Get predicted probabilities
            y_pred_class = np.argmax(y_pred_prob, axis=1)  # Convert to class labels
        else: 
            y_pred_prob = model.predict(self.X_test)  # Get predicted probabilities
            y_pred_class = np.argmax(y_pred_prob, axis=1)
    
        # Ensure y_test is in the correct format
        print("Unique values in y_test:", np.unique(self.y_test))
        print("Unique values in y_pred_class:", np.unique(y_pred_class))
    
        # Calculate metrics
        accuracy = accuracy_score(self.y_test, y_pred_class)
        precision = precision_score(self.y_test, y_pred_class, average='weighted', zero_division=0)
        recall = recall_score(self.y_test, y_pred_class, average='weighted', zero_division=0)
        f1 = f1_score(self.y_test, y_pred_class, average='weighted', zero_division=0)
        
        # Calculate AUC if binary classification
        if len(np.unique(self.y_test)) == 2:
            auc_roc = roc_auc_score(self.y_test, y_pred_prob[:, 1])  # Positive class
        else:
            auc_roc = roc_auc_score(self.y_test, y_pred_prob, multi_class='ovr')
    
        # Store and return metrics
        metrics = {
            "model": model_name,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "auc_roc": auc_roc
        }
        return metrics

    


    def store_metrics(self, model_name, metrics, history):
        """
        Store the metrics of each model for later comparison.
        """
        # metrics['model'] = model_name
        metrics['history'] = history  # Save the history object
        metrics_df = pd.DataFrame([metrics])  # Create a DataFrame from metrics
        self.results_df = pd.concat([self.results_df, metrics_df], ignore_index=True)  # Concatenate
        # self.results_df = pd.concat([self.results_df, metrics], ignore_index=True)  # Concatenate


    def select_best_model(self):
        """
        Select the best model based on the highest F1 score.
        """


        # Adjust pandas display settings to show all rows and columns
        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns
        pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping
    
        # # Display results after all models are trained
        # display(self.results_df)
        # print("Second Method")
        # print(self.results_df)

        # Create a new DataFrame without the 'history' column

        results_without_history = self.results_df.drop(columns=['history'])     
        # Display the new DataFrame    
        # display(results_without_history)
        # print("Second Method")
        print(results_without_history)


        self.best_model_name = self.results_df.loc[self.results_df['f1'].idxmax()]['model']
        print(f"Best model is: {self.best_model_name}")
        self.best_metrics = self.results_df.loc[self.results_df['model'] == self.best_model_name].to_dict('records')[0]
        self.best_model = self.models[self.best_model_name]

        # Display plots for the best model
        self.plot_best_model_metrics()


    def plot_best_model_metrics(self):
        """
        Plot the metrics for the best model.
        """
        print(f"Displaying plots for best model: {self.best_model_name}")
    
        # Access the history from the best metrics
        history = self.best_metrics['history']
    
        # Get the model object
        model = self.models[self.best_model_name]
        
        # Get unique classes
        self.unique_classes = np.unique(self.y_train)
    
        # Display model architecture
        layers = model.layers
        plt.figure(figsize=(8, 3))
        for i, layer in enumerate(layers):
            plt.text(0.5, 1 - (i + 1) * 0.1, layer.name, fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
        plt.axis('off')
        plt.title(f'{self.best_model_name} Architecture')
        plt.show()
    
        # Plot Train/Validation Loss and Accuracy
        plt.figure(figsize=(10, 5))
    
        plt.subplot(1, 2, 1)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Train vs Validation Loss')
        plt.legend()
    
        plt.subplot(1, 2, 2)
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Train vs Validation Accuracy')
        plt.legend()
    
        plt.show()
    
        # Prepare predictions
        if 'RNN' in self.best_model_name or 'LSTM' in self.best_model_name:
            y_pred = model.predict(self.X_test_rnn)
        else:
            y_pred = model.predict(self.X_test)
    
        # Convert predictions to class labels
        y_pred_class = y_pred.argmax(axis=1)
    
        # Create confusion matrix
        conf_matrix = confusion_matrix(self.y_test, y_pred_class)
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title(f'{self.best_model_name} Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
    
        # ROC-AUC Curve
        if len(self.unique_classes) == 2:  # For binary classification
            y_pred_prob = y_pred[:, 1]  # Get the probability for the positive class
            fpr, tpr, _ = roc_curve(self.y_test, y_pred_prob)
            
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, label='ROC Curve')
            plt.title(f'ROC Curve for {self.best_model_name}')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.show()
        
            # Precision-Recall Curve
            precision, recall, _ = precision_recall_curve(self.y_test, y_pred_prob)
            plt.figure(figsize=(8, 6))
            plt.plot(recall, precision, label='Precision-Recall Curve')
            plt.title(f'Precision-Recall Curve for {self.best_model_name}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.legend()
            plt.show()
        else:  # For multi-class classification
            # Compute ROC curve for each class
            plt.figure(figsize=(8, 6))
            for i in range(len(self.unique_classes)):
                fpr, tpr, _ = roc_curve(self.y_test == self.unique_classes[i], y_pred[:, i])
                plt.plot(fpr, tpr, label=f'Class {self.unique_classes[i]}')
        
            plt.title(f'ROC Curve for {self.best_model_name}')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.show()
            
            # Compute Precision-Recall for each class
            plt.figure(figsize=(8, 6))
            for i in range(len(self.unique_classes)):
                precision, recall, _ = precision_recall_curve(self.y_test == self.unique_classes)
    
    def eval_models(self, model_name):
        """
        Display metrics and plots for a specified model.
        """
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return

        # Retrieve the metrics for the specified model
        model_metrics = self.results_df[self.results_df['model'] == model_name].to_dict('records')
        if not model_metrics:
            print(f"No metrics found for model {model_name}.")
            return

        model_metrics = model_metrics[0]  # Get the first (and should be the only) record

        # Print the metrics
        print(f"Metrics for {model_name}:")
        print(f"Accuracy: {model_metrics['accuracy']}")
        print(f"Precision: {model_metrics['precision']}")
        print(f"Recall: {model_metrics['recall']}")
        print(f"F1 Score: {model_metrics['f1']}")
        print(f"AUC-ROC: {model_metrics['auc_roc']}")

        # Access the history from the metrics
        history = model_metrics['history']

        # Get the model object
        model = self.models[model_name]

        mn = model_name
        # Display model architecture
        layers = model.layers
        plt.figure(figsize=(8, 3))
        for i, layer in enumerate(layers):
            plt.text(0.5, 1 - (i + 1) * 0.1, layer.name, fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
        plt.axis('off')
        plt.title(f'{mn} Architecture')
        plt.show()
    
        # self.plot_model_architecture(model)

        

        # Plot Train/Validation Loss and Accuracy
        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Train vs Validation Loss')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Train vs Validation Accuracy')
        plt.legend()

        plt.show()

        # Prepare predictions
        if 'RNN' in model_name or 'LSTM' in model_name:
            y_pred = model.predict(self.X_test_rnn)
        else:
            y_pred = model.predict(self.X_test)

        # Convert predictions to class labels
        y_pred_class = y_pred.argmax(axis=1)

        # Create confusion matrix
        conf_matrix = confusion_matrix(self.y_test, y_pred_class)
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title(f'{model_name} Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()

        # ROC-AUC Curve
        if len(np.unique(self.y_train)) == 2:  # For binary classification
            y_pred_prob = y_pred[:, 1]  # Get the probability for the positive class
            fpr, tpr, _ = roc_curve(self.y_test, y_pred_prob)

            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, label='ROC Curve')
            plt.title(f'ROC Curve for {model_name}')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.show()

            # Precision-Recall Curve
            precision, recall, _ = precision_recall_curve(self.y_test, y_pred_prob)
            plt.figure(figsize=(8, 6))
            plt.plot(recall, precision, label='Precision-Recall Curve')
            plt.title(f'Precision-Recall Curve for {model_name}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.legend()
            plt.show()
        else:  # For multi-class classification
            # Compute ROC curve for each class
            plt.figure(figsize=(8, 6))
            for i in range(len(np.unique(self.y_train))):
                fpr, tpr, _ = roc_curve(self.y_test == np.unique(self.y_train)[i], y_pred[:, i])
                plt.plot(fpr, tpr, label=f'Class {np.unique(self.y_train)[i]}')

            plt.title(f'ROC Curve for {model_name}')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.show()

            # Compute Precision-Recall for each class
            plt.figure(figsize=(8, 6))
            for i in range(len(np.unique(self.y_train))):
                precision, recall, _ = precision_recall_curve(self.y_test == np.unique(self.y_train)[i], y_pred[:, i])
                plt .plot(recall, precision, label=f'Class {np.unique(self.y_train)[i]}')

            plt.title(f'Precision-Recall Curve for {model_name}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.legend()
            plt.show()
    

    def save_model(self, model_name, path='./'):
        """
        Save a specific model to the given path.
        """
        model = self.models.get(model_name, None)
        if model is not None:
            model.save(f"{path}/{model_name}.h5")
            print(f"Model {model_name} saved at {path}/{model_name}.h5")
        else:
            print(f"Model {model_name} not found.")



    