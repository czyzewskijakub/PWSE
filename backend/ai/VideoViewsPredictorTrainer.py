# coding=utf-8
import torch
from torch import optim, nn


class VideoViewsPredictorTrainer:
    """
    A class for training and evaluating the VideoViewsPredictor model.
    """

    def __init__(self, model, learning_rate=0.01):
        """
        Initializes a new instance of the VideoViewsPredictorTrainer class with the specified number of input features
        and learning rate.

        Arguments:
        - model: A PyTorch neural network model for predicting video views based on various input features.
        - learning_rate: A float value representing the learning rate for the optimizer.
        """
        self.Model = model
        self.LearningRate = learning_rate
        self.LossFunction = nn.MSELoss()
        self.Optimizer = optim.Adam(self.Model.parameters(), lr=learning_rate)

    def train(self, train_data, train_labels, num_epochs=1000, verbose: bool = True):
        """
        Trains the VideoViewsPredictor model on the given input data and targets for a specified number of epochs
        using mini-batch stochastic gradient descent.

        Arguments:
        - input_data: A PyTorch tensor of shape (n_samples, num_features) containing the input data.
        - targets: A PyTorch tensor of shape (n_samples,) containing the target values.
        - num_epochs: An integer value representing the number of epochs to train the model for.
        - verbose: A flag, when set print information about training.
        """
        # Training data
        x_train = torch.tensor(train_data, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True)
        y_train = torch.tensor(train_labels, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True)

        inputs = torch.autograd.Variable(x_train.float())
        targets = torch.autograd.Variable(y_train.float())
        # Train the model
        for epoch in range(num_epochs):
            # Zero the gradients
            self.Optimizer.zero_grad()
            # Forward pass
            out = self.Model(inputs)
            # Compute the loss
            loss = self.LossFunction(out, targets)
            # Backward pass and update weights
            loss.backward()
            self.Optimizer.step()

            # Print progress
            if verbose:
                if (epoch + 1) % 100 == 0:
                    print(f'Epoch [{epoch + 1:{len(str(num_epochs))}}/{num_epochs}], Loss: {loss.item():18.0f}')

    def evaluate(self, x, y, threshold=0.5):
        """
        Evaluates the VideoViewsPredictor model on the given input data and targets using a specified threshold value
        for the model's predictions.

        Arguments:
        - input_data: A PyTtorch tensor of shape (n_samples, num_features) containing the input data.
        - targets: A PyTorch tensor of shape (n_samples,) containing the target values.
        - threshold: A float value representing the threshold value to use for the model's predictions.
        Returns:
            - A float value representing the percentage of correct predictions for the given input data and targets.
            """
        # Evaluate the model
        self.Model.eval()
        with torch.no_grad():
            inputs = torch.autograd.Variable(
                torch.tensor(x, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True).float())
            targets = torch.autograd.Variable(
                torch.tensor(y, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True).float())
            outputs = self.Model(inputs)
            loss = self.LossFunction(outputs, targets)
            print(f'Test loss: {loss.item():14.0f}')
            # predictions = (outputs >= threshold).float().squeeze()
            # num_correct = torch.sum(predictions == targets)
            # accuracy = num_correct / len(y)
            # return accuracy.item()

    def predict(self, data):
        inputs = torch.autograd.Variable(
            torch.tensor(data, device=self.Model.Device, dtype=self.Model.Dtype, requires_grad=True).float())
        result = self.Model(inputs)
        return [x.item() for x in result]

    def quick_predict(self, x, y, amount):
        for i in range(amount):
            res = self.predict(x[i])
            ocz = y[i]
            print(f'{res[0]:.2f} {ocz[0]:.2f} {(ocz - res)[0]:.2f} |{(ocz / res * 100)[0]:.2f}%')

    def compute_accuracy(self, input_data, targets, accuracy_threshold=20):
        """
        Computes the percentage of correct responses for a given input data and targets using a threshold
        value for the model's predictions.

        Arguments:
        - model: The trained VideoViewsPredictor model.
        - input_data: A tensor containing the input data of shape (n_samples, n_features).
        - targets: A tensor containing the target values of shape (n_samples,).
        - accuracy_threshold: A float value representing the percentage threshold value between correct value and result.

        Returns:
        - The percentage of correct responses as a float value.
        """

        # Get the model predictions
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
        """
        Saves the current state of the VideoViewsPredictor model to a file.

        Arguments:
        - filepath: A string value representing the path to save the model to.
        """
        torch.save({
            'model_state_dict': self.Model.state_dict(),
            'optimizer_state_dict': self.Optimizer.state_dict(),
        }, filepath)

    def load(self, filepath):
        """
        Loads the state of the VideoViewsPredictor model from a file.

        Arguments:
        - filepath: A string value representing the path to load the model from.
        """
        checkpoint = torch.load(filepath, map_location=torch.device("cpu"))

        self.Model.load_state_dict(checkpoint['model_state_dict'])
        self.Optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
