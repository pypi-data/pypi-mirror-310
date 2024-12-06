# dlpml

`dlpml` is a minimalist machine learning library implemented in Python. It provides simple and efficient tools for data analysis and machine learning, including linear regression and logistic regression models.

## Features

- Linear Regression
- Logistic Regression
- Regularization
- Gradient Descent Optimization

## Installation

To install the required dependencies, use [Poetry](https://python-poetry.org/):

```sh
poetry install
```

## Usage (check notebooks)
### Linear Regression
```python
import pandas as pd
from dlpml.regression.linear_regressor import LinearRegressor

# Load dataset
data = pd.read_csv("data/ex_linear_regression_data1.csv", header=None)
X_train = data.iloc[:, [0]].to_numpy()
y_train = data.iloc[:, 1].to_numpy()

# Initialize and fit the model
model = LinearRegressor(alpha=0.01, iterations=10000, lambda_=0.01)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_train)
```
### Logistic Regression
```python
import pandas as pd
from dlpml.classification.logistic_regressor import LogisticRegressor

# Load dataset
data = pd.read_csv("data/ex_logistic_regression_data1.csv")
X_train = data.iloc[:, 0:2].to_numpy()
y_train = data.iloc[:, 2].to_numpy()

# Initialize and fit the model
model = LogisticRegressor(alpha=0.01, iterations=10000, lambda_=0.01)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_train)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
