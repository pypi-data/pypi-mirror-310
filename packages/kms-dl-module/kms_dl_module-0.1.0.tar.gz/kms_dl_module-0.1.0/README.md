

# KMS Deep Learning Module

KMS Deep Learning Module is a Python library designed for deep learning tasks, such as regression, classification, and text classification. It offers an intuitive API for building, training, and evaluating machine learning models, making deep learning more accessible to all developers.
Features

    Regression: Build and train deep learning models for regression tasks. Supports various configurations and hyperparameter tuning.
    Classification: Handle both binary and multi-class classification with customizable architectures, including support for activation functions, optimizers, and metrics.
    Text Classification: Preprocess and vectorize text data, and train models for text-based classification tasks with built-in text handling tools.

## Installation

To install the kms_dl_module, you can use pip:

```
pip install kms_dl_module
```
## Usage

Here’s a quick guide to get started with the library:

### Regression

For training a regression model:

```
from kms_dl_module.regression import RegressionModel

# Initialize the RegressionModel with your dataframe and target column

target_variable = 'target'
features=['List of features']
categorical_cols = None  # optional
epochs = 5  # optional
test_size = 0.3  # optional

model = RegressionModel(dataframe, target_variable, features, epochs, categorical, test_size)


# Train the model
model.train_module_regression()

# Evaluate the model to get result for a specific model from the list of avaiable models
model.evaluate("model_name")
Ex: model.evaluate("RNN_LEAKY_RELU_L1")

```

### Classification

For building and training a classification model (binary or multi-class):

```
from kms_dl_module.classification import ClassificationModel

# Create an instance of the ClassificationModel class
model = ClassificationModel()

#Initialize the ClassificationModel with your dataframe and target column

target_variable = 'target'
features=['List of features']
categorical_cols = None  # optional
epochs = 5  # optional
test_size = 0.3  # optional


# Train the model
model.train_module(df, target_variable, features, epochs, categorical_cols)



# Evaluate the model
model.evaluate('model_name')
model.evaluate("MLP_ReLU_L2")
```

### Text Classification

For text classification tasks:

```
from kms_dl_module.text_classification import TextClassificationModel

# Initialize the TextClassificationModel with your dataframe, target column, and text column(s)

target_variable = 'target'
text_columns=['List of text columns']
features = ['List of other features']
categorical_cols = None  # optional
epochs = 5  # optional
test_size = 0.3  # optional


model = TextClassificationModel(dataframe, target_variable, features, epochs, categorical_cols,
                 text_columns, test_size)

# Train the model
model.train()

# Evaluate the model
model.evaluate()

```

## Documentation

### Regression

The RegressionModel class is used for regression tasks. It provides functions for model training, evaluation, and model tuning.

### Classification

The ClassificationModel class handles both binary and multi-class classification tasks. It supports configurable activation functions, optimizers, and loss functions for greater flexibility.

### Text Classification

The TextClassificationModel class simplifies the process of handling text data, including text preprocessing, vectorization, and model training for text-based classification problems.

### Contributing

We welcome contributions! Feel free to fork the repository and submit pull requests. Please make sure to follow the existing code style and write tests for new features.

### License

This library is licensed under the MIT License.
