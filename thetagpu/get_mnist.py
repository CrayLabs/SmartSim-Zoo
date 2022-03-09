from torchvision.datasets import MNIST

"""Download MNIST to disk.
"""

mnist_train = MNIST("mnist", train=True, download=True)
mnist_test = MNIST("mnist", train=False, download=True)
