import tensorflow as tf
from tensorflow import keras
import numpy as np
from utils.ModelUtils import *





class Mymodel:
    def fit(self, Y, R, lambda_=1, iterations=200):
        """
        Args:
            Y: (ndarray (num_movies,num_users)    : matrix of user ratings of movies
            R: (ndarray (num_movies,num_users)    : matrix, where R(i, j) = 1 if the i-th movies was rated by the j-th user
            lambda_: regularization parameter
            iterations: gradient descent times
        Returns:

        """
        num_movies, num_users = Y.shape
        Ynorm, self.Ymean = normalizeRatings(Y, R)
        num_features = 100
        tf.random.set_seed(1234)  # for consistent results
        self.W = tf.Variable(tf.random.normal((num_users, num_features), dtype=tf.float64), name='W')
        self.X = tf.Variable(tf.random.normal((num_movies, num_features), dtype=tf.float64), name='X')
        self.b = tf.Variable(tf.random.normal((1, num_users), dtype=tf.float64), name='b')
        optimizer = keras.optimizers.Adam(learning_rate=1e-1)

        for iter in range(iterations):
            # Use TensorFlow’s GradientTape
            # to record the operations used to compute the cost
            with tf.GradientTape() as tape:

                # Compute the cost (forward pass included in cost)
                cost_value = cofi_cost_func(self.X, self.W, self.b, Ynorm, R, lambda_)
            # Use the gradient tape to automatically retrieve
            # the gradients of the trainable variables with respect to the loss
            grads = tape.gradient(cost_value, [self.X, self.W, self.b])

            # Run one step of gradient descent by updating
            # the value of the variables to minimize the loss.
            optimizer.apply_gradients(zip(grads, [self.X, self.W, self.b]))

            # Log periodically.
            if iter % 20 == 0:
                print(f"Training loss at iteration {iter}: {cost_value:0.1f}")

    def predict(self, userid):
        # Make a prediction using trained weights and biases
        p = np.matmul(self.X.numpy(), np.transpose(self.W.numpy())) + self.b.numpy()

        # restore the mean
        pm = p + self.Ymean

        my_predictions = pm[:, 0]
        return my_predictions
