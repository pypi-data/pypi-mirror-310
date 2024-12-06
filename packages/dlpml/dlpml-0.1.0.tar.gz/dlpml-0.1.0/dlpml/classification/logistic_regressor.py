import pandas as pd
import numpy as np
import copy
import math
import matplotlib.pyplot as plt

class LogisticRegressor:
    """
    Class to fit a logistic regression model to data using gradient descent.
    """
    def __init__(self, alpha=0.01, iterations=1_000, lambda_=0.01):
        """
        Initializes the logistic regression model.

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
        Fits the logistic regression model to the data using gradient descent.

        Parameters:
        X (numpy.ndarray): The input features for the training data.
        y (numpy.ndarray): The target values for the training data.

        The function will store the learned weights and bias in the class variables self.w and
        self.b. It will also store the cost history in the class variable self.cost_history.
        """
        # Initialize fitting parameters
        w_in = np.random.rand(X.shape[1])-0.5
        b_in = 1.
        self.w, self.b = self.gradient_descent(X, y, w_in, b_in) 

    def predict(self, X):


        """
        Predict whether the label is 0 or 1 using learned logistic
        regression parameters w
        
        Args:
        X : (ndarray Shape (m,n)) data, m examples by n features
        w : (ndarray Shape (n,))  values of parameters of the model      
        b : (scalar)              value of bias parameter of the model

        Returns:
        p : (ndarray (m,)) The predictions for X using a threshold at 0.5
        """
        # number of training examples
        m, n = X.shape   
        p = np.zeros(m)
        
        z = np.dot(X, self.w)+self.b
        f_wb = self.sigmoid(z)
        p = (f_wb > 0.5).astype(float)
        
        return p
    

    def sigmoid(self, z):
        """
        Computes the sigmoid of z.

        Parameters:
        z (numpy.ndarray or scalar): The input value or array of values.

        Returns:
        numpy.ndarray or scalar: The sigmoid of the input.
        """
        g = 1 / (1 + np.exp(-z))
        return g

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
        z = np.dot(X, w)+b
        f_wb = self.sigmoid(z)
        loss_a = -y*np.log(f_wb)
        loss_b = (1-y)*np.log(1-f_wb)
        loss = loss_a - loss_b
        cost_without_reg = np.mean(loss)       
        
        reg_cost = (self.lambda_/(2*m)) * np.sum(w**2)
        
        total_cost = cost_without_reg + reg_cost

        return total_cost

    def compute_regularized_gradient(self, X, y, w, b): 
        """
        Computes the gradient for logistic regression with regularization
    
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
        z = np.dot(X, w)+b
        f_wb = self.sigmoid(z)
        losses = f_wb-y
        dj_db = np.mean(losses)
        
        # Get gradient for weights
        z = np.dot(X, w)+b
        f_wb = self.sigmoid(z)
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
    data = pd.read_csv("../data/ex_logistic_regression_data2.csv")
    X_train = data.iloc[:,0:2].to_numpy()
    y_train = data.iloc[:,2].to_numpy()

    # Use dlpml Logistic Regressor
    model = LogisticRegressor(alpha=0.01, iterations=10*1_000, lambda_=0.01)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_train)

    print('Train Accuracy: %f'%(np.mean(y_pred == y_train) * 100))
    pass
