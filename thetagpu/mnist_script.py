import torch


def check_accuracy(inferred, labels):
    check = torch.argmax(inferred, dim=1) == labels

    return torch.mean(check.float()).unsqueeze(0)
