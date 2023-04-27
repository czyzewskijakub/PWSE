# coding=utf-8
import datetime
import time
from typing import Dict

import pandas as pd
import torch
from torch import optim, nn


class VideoViewsPredictorTrainer:

    def __init__(self, model, scaler, learning_rate=0.01):
        self.Model = model
        self.Scaler = scaler
        self.LearningRate = learning_rate
        self.LossFunction = nn.MSELoss()
        self.Optimizer = optim.Adam(self.Model.parameters(), lr=learning_rate)

    def train(self, train_data, train_labels, num_epochs=1000, verbose: bool = True):
        x_train = torch.tensor(train_data, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True)
        y_train = torch.tensor(train_labels, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True)

        inputs = torch.autograd.Variable(x_train.float())
        targets = torch.autograd.Variable(y_train.float())
        for epoch in range(num_epochs):
            self.Optimizer.zero_grad()
            out = self.Model(inputs)
            loss = self.LossFunction(out, targets)
            loss.backward()
            self.Optimizer.step()

            if verbose:
                if (epoch + 1) % 100 == 0:
                    print(f'Epoch [{epoch + 1:{len(str(num_epochs))}}/{num_epochs}], Loss: {loss.item():12.0f}')

    def evaluate(self, x, y):
        self.Model.eval()
        with torch.no_grad():
            inputs = torch.autograd.Variable(
                torch.tensor(x, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True).float())
            targets = torch.autograd.Variable(
                torch.tensor(y, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True).float())
            outputs = self.Model(inputs)
            loss = self.LossFunction(outputs, targets)
            print(f'Test loss: {loss.item():14.0f}')

    def predict(self, data: Dict):
        timestamp = time.mktime(datetime.datetime.strptime(data['VPublishedDate'], "%Y-%m-%d").timetuple())
        data['VPublishedDate'] = timestamp
        dataframe = pd.DataFrame(data, index=[0])
        numpyarray = self.Scaler.transform(dataframe)
        inputs = torch.autograd.Variable(
            torch.tensor(numpyarray, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True).float())
        result = self.Model(inputs)
        return [x.item() for x in result]

    def quick_predict(self, x, y, amount):
        for i in range(amount):
            res = self.predict(x[i])
            ocz = y[i]
            print(f'{res[0]:.2f} {ocz[0]:.2f} {(ocz - res)[0]:.2f} |{(ocz / res * 100)[0]:.2f}%')

    def compute_accuracy(self, input_data, targets, accuracy_threshold=20):
        self.Model.eval()
        with torch.no_grad():
            input_tensor = torch.tensor(input_data, device=self.Model.Device, dtype=self.Model.Dtype,
                                        requires_grad=True)
            model_output = self.Model(input_tensor)

            predictions = model_output.tolist()

            correct = 0

            for pred, label in zip(predictions, targets):
                if abs(100 - (label[0] * 100 / pred[0])) <= accuracy_threshold:
                    correct += 1

            accuracy = (correct / len(predictions)) * 100.0

            return accuracy

    def save(self, filepath):
        torch.save({
            'model_state_dict': self.Model.state_dict(),
            'optimizer_state_dict': self.Optimizer.state_dict(),
            'scaler_mean': self.Scaler.mean_,
            'scaler_scale': self.Scaler.scale_,
        }, filepath)

    def load(self, filepath):
        checkpoint = torch.load(filepath, map_location=torch.device("cpu"))

        self.Model.load_state_dict(checkpoint['model_state_dict'])
        self.Optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.Scaler.mean_ = checkpoint['scaler_mean']
        self.Scaler.scale_ = checkpoint['scaler_scale']

    def predict2(self, data):
        inputs = torch.autograd.Variable(
            torch.tensor(data, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True).float())
        result = self.Model(inputs)
        return [x.item() for x in result]

    def quick_predict2(self, x, y, amount):
        for i in range(amount):
            res = self.predict2(x[i])
            ocz = y[i]
            print(f'{res[0]:.2f} {ocz[0]:.2f} {(ocz - res)[0]:.2f} |{(ocz / res * 100)[0]:.2f}%')