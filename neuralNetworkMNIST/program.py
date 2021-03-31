import neuralNetwork as nn
import numpy as np

with np.load('neuralNetworkMNIST/mnist.npz') as data:
    training_images = data['training_images']
    training_labels = data['training_labels']
    test_images = data['test_images']
    test_labels = data['test_labels']

layer_sizes = (784, 25, 10)

net = nn.NeuralNetwork(layer_sizes)
prediction = net.predict(training_images)

net.stochastic_gradient_descent(
    list(zip(training_images, training_labels)), 30, 10, 2.0, list(zip(test_images, test_labels)))
