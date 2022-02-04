import torch
import torch.nn as nn

from smartredis import Client

from time import sleep
from time import time

from torchvision.models import resnet18

import io

"""This is the trainer code for the `launch_mnist.py` example. It
   it is launched through SmartSim, and the Orchestrator is up and
   running.
"""

# Taken from https://github.com/marrrcin/pytorch-resnet-mnist/blob/master/pytorch-resnet-mnist.ipynb
class ResNetMNIST(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = resnet18(num_classes=10)
        self.model.conv1 = nn.Conv2d(
            1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
        )
        self.loss = nn.CrossEntropyLoss()

    def forward(self, x):
        return self.model(x)


model = ResNetMNIST().cuda()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.005)

client = Client(None, False)

while not client.dataset_exists("MNIST_train"):
    print("Waiting for batches to be available")
    sleep(5)

mnist_data = client.get_dataset("MNIST_train")

train_samples = torch.tensor(mnist_data.get_tensor("samples")).cuda()
train_labels = torch.tensor(mnist_data.get_tensor("labels")).cuda()

torch_ds = torch.utils.data.TensorDataset(train_samples, train_labels)
torch_dl = torch.utils.data.DataLoader(torch_ds, batch_size=256)


start_time = time()
for epoch in range(1):
    print(f"Epoch {epoch}")
    for t, (batch, targets) in enumerate(torch_dl):

        # Forward pass: Compute predicted y by passing x to the model
        y_pred = model(batch)

        # Compute and print loss
        loss = criterion(y_pred, targets)

        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        acc = (
            torch.mean((torch.argmax(y_pred, dim=1) == targets).float()).cpu().numpy()
            * 100
        )
        end_time = time()
        print(
            f"batch {t+1}/{len(torch_dl)}",
            f"Loss: {loss.item()}",
            f"Batch time: {end_time-start_time} seconds",
            f"Accuracy: {acc}%",
        )
        start_time = time()

compiled_model = torch.jit.script(model)
buffer = io.BytesIO()
torch.jit.save(compiled_model, buffer)

client.set_model("trained_model", buffer.getvalue(), "TORCH", device="GPU")

print("Training completed.")
