import numpy as np
import random

# \frac{\partial Cost}{\partial a} = a - label, where a is the last layer of activations

# \frac{\partial a'}{\partial a} = (\sigma' (z) * w)^T, where * is numpy broadcasting
# elementwise multiplication, a' is the activated layer after the other activated layer a,
# w is the weight matrix between them, and z is the unactivated layer result (whatever it's called)

# \frac{\partial a'}{\partial w} = \sigma' (z) a^T (with normal matrix multiplication)
# \frac{\partial a'}{\partial b} = \sigma' (z)

# now multiply everything and we win!


def cost(a, label):
    return sum([(ai - ans)**2 for ai, ans in zip(a, label)]) / 2


# derivative wrt a
def cost_prime(a, label):
    return (a - label)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))


class NeuralNetwork:
    def __init__(self, layer_sizes):
        weight_shapes = [(second, first) for second, first in zip(
            layer_sizes[1:], layer_sizes[:-1])]

        self.weights = [np.random.standard_normal(
            s) / s[1]**0.5 for s in weight_shapes]  # ??? ok

        self.biases = [np.zeros((s, 1)) for s in layer_sizes[1:]]

    def predict(self, a):
        for w, b in zip(self.weights, self.biases):
            a = sigmoid(np.matmul(w, a) + b)
        return a

    def accuracy(self, images, labels):
        predictions = self.predict(images)
        return sum([np.argmax(a) == np.argmax(b)
                    for a, b in zip(predictions, labels)])

    def stochastic_gradient_descent(self, training_data, epochs, batch_size, eta, test_data=None):
        n = len(training_data)
        m = len(test_data)

        for ep in range(epochs):
            random.shuffle(training_data)
            batches = [training_data[i:i + batch_size]
                       for i in range(0, n, batch_size)]

            for batch in batches:
                self.update_batch(batch, eta)

            if test_data:
                accuracy = self.accuracy(*zip(*test_data))
                print(f"Epoch {ep}: {accuracy} / {m}, {accuracy / m * 100}%.")
            else:
                print(f"Epoch {ep} complete.")

    def update_batch(self, batch, eta):
        for image, label in batch:
            del_w, del_b = self.get_gradient(image, label)
            self.weights = [w - dw * eta /
                            len(batch) for w, dw in zip(self.weights, del_w)]
            self.biases = [b - db * eta /
                           len(batch) for b, db in zip(self.biases, del_b)]

    def get_gradient(self, image, label):
        del_w = [np.zeros(w.shape) for w in self.weights]
        del_b = [np.zeros(b.shape) for b in self.biases]

        layer_transitions = len(self.weights)

        a = image
        zs = [a]

        for w, b in zip(self.weights, self.biases):
            z = np.matmul(w, a) + b
            zs.append(z)
            a = sigmoid(z)

        delta = cost_prime(a, label)

        for i in reversed(range(0, layer_transitions)):
            z = zs[i + 1]
            spz = sigmoid_prime(z)
            del_w[i] = delta * np.matmul(spz, sigmoid(zs[i]).transpose())
            del_b[i] = delta * spz
            delta = np.matmul((spz * self.weights[i]).transpose(), delta)
        return (del_w, del_b)
