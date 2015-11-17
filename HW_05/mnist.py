import pickle

import numpy as np

np.random.seed(1) # DO NOT MODIFY THIS LINE!

# NEURAL NETWORK CONFIGURATION
size_of_layers = [
    28 * 28, # a size of the input layer (MNIST digit data consist of 28x28 pixels)
    50, # [4.E] a size of the hidden layer
    10, # a size of the output layer
]

layers =[
    np.ones((1, size_of_layers[0])), # the input layer 
    np.ones((1, size_of_layers[1])), # the hidden layer
    np.ones((1, size_of_layers[2])), # the output layer
]

weights = [
    (2 * np.random.random((size_of_layers[0], size_of_layers[1]))) - 1, # weights between the input layer and the hidden layer
    (2 * np.random.random((size_of_layers[1], size_of_layers[2]))) - 1, # weights between the hidden layer and the output layer
]

learning_rate = 0.1 # [4.E] a learning rate


def sigmoid(x):
    # a sigmoid of x

    # [4.A] FILL YOUR CODE HERE
    from scipy.special import expit
    return expit(x)


def propagate(x):
    # propagate an input x to the output layer

    # [4.B] FILL YOUR CODE HERE
    # input activations
    layers[0] = x
    # hidden activations
    layers[1] = sigmoid(layers[0].dot(weights[0]))
    # output activations
    layers[2] = sigmoid(layers[1].dot(weights[1]))

    return layers[2]


def backpropagate(y_true, learning_rate):
    # backpropagate an error from the output layer and update weights

    # [4.C] FILL YOUR CODE HERE
    # the given y is already sigmoided
    sigmoid_grad = lambda y: y * (1.0 - y)
    # calculate errors for output layer
    errors = -(y_true - layers[2])
    output_deltas = sigmoid_grad(layers[2]) * errors
    # calculate errors for hidden layer
    errors = output_deltas.dot(weights[1].transpose())
    hidden_deltas = sigmoid_grad(layers[1]) * errors
    # update the weights connecting hidden to output
    weights[1] -= learning_rate * layers[1].transpose().dot(output_deltas)
    # update the weights connecting input to hidden
    weights[0] -= learning_rate * layers[0].transpose().dot(hidden_deltas)


# EVALUATION - DO NOT MODIFY THIS FUNCTION!
def evaluate(X, Y):
    # calculate an error of the network

    error = []
    for i in range(0, len(X)):
        x =  X[i, np.newaxis]
        y =  Y[i, np.newaxis]

        y_predicted = propagate(x)

        error.append(np.mean(np.abs(y_predicted - y)))
    
    return np.mean(error)

# SAMPLING CONFIGURATION
np.random.seed(1) # DO NOT MODIFY THIS LINE!

# READING DATA
with open('training.pickle', 'rb') as input_file:
    X_train, Y_train = pickle.load(input_file)
    X_train = np.array(X_train)
    Y_train = np.array(Y_train)
    print('training data loaded')

with open('validation.pickle', 'rb') as input_file:
    X_valid, Y_valid = pickle.load(input_file)
    X_valid = np.array(X_valid)
    Y_valid = np.array(Y_valid)
    print('validation data loaded')

# TRAINING
for iteration in range(50000):
    # choose a random sample of X_train and Y_train
    i = np.random.randint(0, len(X_train))
    x =  X_train[i, np.newaxis]
    y_true =  Y_train[i, np.newaxis]

    # propagate an input x
    y_predicted = propagate(x)
    # backpropagate an error and update weights
    backpropagate(y_true, learning_rate)

    if (iteration % 1000) == 0:
        print('iteration: {0:5d} / error on validation data: {1:.15f} / y_true: {2} / y_predicted: {3}'.format(
            iteration, 
            evaluate(X_valid, Y_valid),
            np.argmax(y_true), 
            np.argmax(y_predicted)
        ))

# EVALUATION - DO NOT MODIFY THIS SECTION!
with open('test.pickle', 'rb') as input_file:
    X_test, Y_test = pickle.load(input_file)
    X_test = np.array(X_test)
    Y_test = np.array(Y_test)

    print('test data loaded')

print('error on validation data: {0:.15f}'.format(evaluate(X_valid, Y_valid)))
print('error on test data: {0:.15f}'.format(evaluate(X_test, Y_test)))
