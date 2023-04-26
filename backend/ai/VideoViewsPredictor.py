# coding=utf-8
""" A PyTorch neural network model for predicting video views based on various input features. """
import torch


# Define the model
class VideoViewsPredictor(torch.nn.Module):
    """
    A PyTorch neural network model for predicting video views based on various input features.
    """
    def __init__(self, number_of_features):
        """
        Initializes a new instance of the VideoViewsPredictor class with the specified number of input features.

        Arguments:
        - num_features: An integer value representing the number of input features.
        """
        super(VideoViewsPredictor, self).__init__()
        self.Dtype = torch.float
        self.Device = torch.device("cuda:0")
        self.NumberOfFeatures: int = number_of_features
        self.fc1 = torch.nn.Linear(self.NumberOfFeatures, 32, device=self.Device, dtype=self.Dtype)
        self.fc2 = torch.nn.Linear(32, 16, device=self.Device, dtype=self.Dtype)
        self.fc3 = torch.nn.Linear(16, 8, device=self.Device, dtype=self.Dtype)
        self.fc4 = torch.nn.Linear(8, 4, device=self.Device, dtype=self.Dtype)
        self.fc5 = torch.nn.Linear(4, 2, device=self.Device, dtype=self.Dtype)
        self.fc6 = torch.nn.Linear(2, 1, device=self.Device, dtype=self.Dtype)

    def forward(self, x):
        """
        Computes the forward pass of the neural network for a given input tensor.

        Arguments:
        - x: A PyTorch tensor of shape (batch_size, num_features) containing the input data.

        Returns:
        - A PyTorch tensor of shape (batch_size, 1) containing the predicted video views.
        """
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = torch.relu(self.fc5(x))
        x = self.fc6(x)
        return x
