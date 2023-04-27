# coding=utf-8
""" A PyTorch neural network model for predicting video views based on various input features. """
import torch

class VideoViewsPredictor(torch.nn.Module):

    def __init__(self, number_of_features):
        super(VideoViewsPredictor, self).__init__()
        self.Dtype = torch.float
        self.Device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.NumberOfFeatures: int = number_of_features
        self.fc1 = torch.nn.Linear(self.NumberOfFeatures, 256, device=self.Device, dtype=self.Dtype)
        self.fc2 = torch.nn.Linear(256, 128, device=self.Device, dtype=self.Dtype)
        self.fc3 = torch.nn.Linear(128, 64, device=self.Device, dtype=self.Dtype)
        self.fc4 = torch.nn.Linear(64, 32, device=self.Device, dtype=self.Dtype)
        self.fc5 = torch.nn.Linear(32, 16, device=self.Device, dtype=self.Dtype)
        self.fc6 = torch.nn.Linear(16, 8, device=self.Device, dtype=self.Dtype)
        self.fc7 = torch.nn.Linear(8, 4, device=self.Device, dtype=self.Dtype)
        self.fc8 = torch.nn.Linear(4, 2, device=self.Device, dtype=self.Dtype)
        self.fc9 = torch.nn.Linear(2, 1, device=self.Device, dtype=self.Dtype)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = torch.relu(self.fc5(x))
        x = torch.relu(self.fc6(x))
        x = torch.relu(self.fc7(x))
        x = torch.relu(self.fc8(x))
        x = self.fc9(x)
        return x
