import pandas as pd
import numpy as np
import copy
import math
import matplotlib.pyplot as plt

class LinearRegressor:
    """
    Class to fit a linear regression model to data using gradient descent.
    """
    def __init__(self, alpha=0.01, iterations=1_000, lambda_=0.01):
        """
        Initializes the linear regression model.

        Parameters:
        alpha (float): The learning rate for gradient descent.
        iterations (int): The number of iterations to run gradient descent.
        lambda_ (float): The regularization parameter.
        """
        self.alpha = alpha
        self.iterations = iterations
        self.lambda_ = lambda_
        self.w = None
        self.b = None

    def fit(self, X, y):
        """
        Fits the linear regression model to the data using gradient descent.

        Parameters:
        X (numpy.ndarray): The input features for the training data.
        y (numpy.ndarray): The target values for the training data.

        The function will store the learned weights and bias in the class variables self.w and
        self.b. It will also store the cost history in the class variable self.cost_history.
        """

        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        w_in = np.random.rand(X.shape[1])-0.5
        b_in = 1.
        self.w, self.b = self.gradient_descent(X, y, w_in, b_in) 

    def predict(self, X):


        """
        Predict whether the label is 0 or 1 using learned linear
        regression parameters w
        
        Args:
        X : (ndarray Shape (m,n)) data, m examples by n features
        w : (ndarray Shape (n,))  values of parameters of the model      
        b : (scalar)              value of bias parameter of the model

        Returns:
        p : (ndarray (m,)) The predictions for X using a threshold at 0.5
        """
        # number of training examples

        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        m, n = X.shape   
        p = np.zeros(m)
        
        f_wb = np.dot(X, self.w)+self.b        
        return f_wb
    
    def compute_regularized_cost(self, X, y, w, b):
        """
        Computes the regularized cost over all examples.
        X : ndarray, shape (m, n)
            Data, m examples by n features.
        y : ndarray, shape (m,)
            Target values.
        w : ndarray, shape (n,)
            Values of parameters of the model.
        b : scalar
            Value of bias parameter of the model.
        lambda_ : scalar, float, optional, default=1
            Controls the amount of regularization.
        total_cost : scalar
            The regularized cost.
        """

        m, n = X.shape
        
        # Cost without regularization


        f_wb = np.dot(X, w)+b
        squared_error_residuals = np.power(y - f_wb,2)
        avg_cost = np.sum(squared_error_residuals)/(2*m)
        cost_without_reg = avg_cost
        
        reg_cost = (self.lambda_/(2*m)) * np.sum(w**2)
        
        total_cost = cost_without_reg + reg_cost

        return total_cost

    def compute_regularized_gradient(self, X, y, w, b): 
        """
        Computes the gradient for linear regression with regularization
    
        Args:
        X : (ndarray Shape (m,n)) data, m examples by n features
        y : (ndarray Shape (m,))  target value 
        w : (ndarray Shape (n,))  values of parameters of the model      
        b : (scalar)              value of bias parameter of the model
        lambda_ : (scalar,float)  regularization constant
        Returns
        dj_db : (scalar)             The gradient of the cost w.r.t. the parameter b. 
        dj_dw : (ndarray Shape (n,)) The gradient of the cost w.r.t. the parameters w. 

        """
        m, n = X.shape
        
        dj_dw = np.zeros(w.shape)
        dj_db = 0.
        
        # Get gradient for b (the gradient with regularization for b is not calculated in practice, it's effect is negligible is null) 
        f_wb = np.dot(X, w)+b
        losses = f_wb-y
        dj_db = np.mean(losses)
        
        # Get gradient for weights
        f_wb = np.dot(X, w)+b
        losses = f_wb-y
        w_gradients = losses * np.transpose(X)    
        dj_dw = np.mean(w_gradients, axis=1)
        
        # Gradient for weights with regularization
        dj_dw += (self.lambda_/m)*w
            
        return dj_db, dj_dw

    def gradient_descent(self, X, y, w, b): 
        """
        Performs batch gradient descent to learn theta. Updates theta by taking 
        num_iters gradient steps with learning rate alpha
        
        Args:
        X :    (ndarray Shape (m, n) data, m examples by n features
        y :    (ndarray Shape (m,))  target value 
        
        Returns:
        w : (ndarray Shape (n,)) Updated values of parameters of the model after
            running gradient descent
        b : (scalar)                Updated value of parameter of the model after
            running gradient descent
        """
        
        # number of training examples
        m = len(X)
        
        
        for i in range(self.iterations):

            # Calculate the gradient and update the parameters
            dj_db, dj_dw = self.compute_regularized_gradient(X, y, w, b)   

            # Update Parameters using w, b, alpha and gradient
            w = w - self.alpha * dj_dw               
            b = b - self.alpha * dj_db              
        
            cost =  self.compute_regularized_cost(X, y, w, b)

            # Print cost at intervals of iterations/10
            if i% math.ceil(self.iterations/10) == 0 or i == (self.iterations-1):
                print(f"Iteration {i:4}: Cost {float(cost):8.2f}   ")
            
        return w, b


if __name__ == "__main__":
    # load dataset
    column_names = ["Var1", "Var2"]
    data = pd.read_csv("../data/ex_linear_regression_data1.csv", header=None, names=column_names)
    X_train = data.iloc[:, [0]].to_numpy() 
    y_train = data.iloc[:, 1].to_numpy()

    # column_names = ["Population", "Var", "Profit"]
    # data = pd.read_csv("data/ex1data2.csv", header=None, names=column_names)
    # X_train = data.iloc[:, [0,1]].to_numpy() 
    # y_train = data.iloc[:, 2].to_numpy()

    # Scale the data
    X_train_scaled = (X_train-np.mean(X_train, axis=0) - np.min(X_train, axis=0))/(np.max(X_train, axis=0)-np.min(X_train, axis=0))
    y_train_scaled = (y_train-np.mean(y_train))/np.std(y_train)

    # Use dlpml LinearRegressor
    model = LinearRegressor(alpha=0.01, iterations=10*1_000, lambda_=0.01)
    model.fit(X_train_scaled, y_train_scaled)
    y_pred = model.predict(X_train_scaled)
    # Rescale the output data
    y_pred = y_pred*np.std(y_train)+np.mean(y_train)

    # Use numpy polyfit
    m_numpy, b_numpy = np.polyfit(X_train_scaled.flatten(), y_train_scaled, 1)
    y_pred_np = m_numpy*X_train_scaled+b_numpy
    # Rescale the output data
    y_pred_np = y_pred_np*np.std(y_train)+np.mean(y_train)

    # Plot the linear fit
    sample_idx = list(np.arange(0, len(y_train), 1))
    plt.scatter(y_train, y_train, marker='o', c='r', label='Training Data') 
    plt.scatter(y_train, y_pred, marker='x', c = 'b', label='Linear Regression')
    plt.scatter(y_train, y_pred_np, marker='*', c = 'orange', label='Numpy Linear Regression')
    plt.legend()
    plt.waitforbuttonpress()
    plt.close()
