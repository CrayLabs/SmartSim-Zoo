from smartredis import Client, Dataset
from time import sleep
from torchvision.datasets import MNIST
from torchvision.transforms.functional import to_tensor
import numpy as np


"""This is the loader code for the `launch_mnist.py` example. It 
   it is launched through SmartSim, and the Orchestrator is up and
   running. 
"""

mnist_train = MNIST("mnist", train=True, download=True)
mnist_test = MNIST("mnist", train=False, download=True)

# NCHW
mnist_train_samples = np.stack([to_tensor(sample) for sample in mnist_train.data.numpy()])
mnist_train_labels = mnist_train.targets.detach().numpy()

print(f"MNIST train shape: {mnist_train_samples.shape}")
print(f"MNIST labels shape: {mnist_train_labels.shape}")

mnist_dataset = Dataset("MNIST_train")
mnist_dataset.add_tensor("samples", mnist_train_samples)
mnist_dataset.add_tensor("labels", mnist_train_labels)


client = Client(None, False)
client.put_dataset(mnist_dataset)

print("MNIST dataset put on DB")

while not client.model_exists("trained_model"):
    print("Waiting for model to be available")
    sleep(10)

mnist_test_samples = np.stack([to_tensor(sample) for sample in mnist_test.data.numpy()])
mnist_test_labels = mnist_test.targets.detach().numpy()

mnist_dataset = Dataset("MNIST_test")
mnist_dataset.add_tensor("samples", mnist_test_samples)
mnist_dataset.add_tensor("labels", mnist_test_labels)

client.put_dataset(mnist_dataset)

client.run_model("trained_model", inputs=["{MNIST_test}.samples"], outputs=["{MNIST_test}.inferred"])

client.set_script_from_file("mnist_script", "./mnist_script.py")

client.run_script("mnist_script", "check_accuracy", inputs=["{MNIST_test}.inferred", "{MNIST_test}.labels"], outputs=["{MNIST_test}.accuracy"])

accuracy = client.get_tensor("{MNIST_test}.accuracy")[0]*100
print(f"Accuracy is {accuracy}%")