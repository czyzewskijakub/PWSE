import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModel

from backend.ai.new.Net import Net

TEXT_FEATURES = ['channelTitle', 'description', 'publishedAt', 'tags', 'title', 'trending_date']
BOOL_FEATURES = ['comments_disabled', 'ratings_disabled']


def prepare_data():
    # Read dataset
    data = pd.read_csv('data/BR_youtube_trending_data.csv')

    # Remove unnecessary columns
    data = data.drop(['video_id', 'channelId', 'thumbnail_link'], axis=1)
    data = data.dropna()

    # Define model input and output
    o = data['view_count']
    i = data.drop(['view_count'], axis=1)

    # Load pre-trained tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    model = AutoModel.from_pretrained('bert-base-uncased')

    x1, x2, y1, y2 = train_test_split(i, o, random_state=42, test_size=0.9999, shuffle=True)

    feature_vector = []
    for col in x1:
        print(col)
        feature_vector.append(encode_string(tokenizer, model, x1, col) if col in TEXT_FEATURES else x1[col].tolist())

    return feature_vector, x1, x2, y1, y2


def encode_string(tokenizer, model, data, column_name):
    encoded_vectors = []
    for i, s in enumerate(data[column_name]):
        # Tokenize the input s
        print(f'Encoding {s}')
        tokens = tokenizer.encode(str(s), add_special_tokens=True, max_length=512, truncation=True, padding='max_length')

        # Convert the tokens to PyTorch tensors
        input_ids = torch.tensor([tokens])

        # Generate the vector representation using the pre-trained model
        with torch.no_grad():
            vectors = model(input_ids)[0]

        # Extract the vector representation of the first token (CLS token)
        sentence_vector = vectors[0]

        encoded_vectors.append(sentence_vector.tolist())
        print(f'{column_name} {i} / {len(data[column_name])}')

    return encoded_vectors


if __name__ == '__main__':

    input_features, x_train, x_test, y_train, y_test = prepare_data()

    dtype = torch.float
    device = torch.device("cpu")

    net = Net(input_size=x_train.shape[1])

    # Train the model
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)

    for epoch in range(1000):
        inputs = torch.autograd.Variable(torch.Tensor(input_features).float())
        targets = torch.autograd.Variable(torch.Tensor(y_train).float())

        optimizer.zero_grad()
        out = net(inputs)
        loss = criterion(out, targets)
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print('Epoch {}, Loss: {}'.format(epoch, loss.item()))

    # Evaluate the model
    net.eval()
    with torch.no_grad():
        inputs = torch.autograd.Variable(torch.Tensor(x_test).float())
        targets = torch.autograd.Variable(torch.Tensor(y_test).float())
        outputs = net(inputs)
        loss = criterion(outputs, targets)
        print('Test loss: {}'.format(loss.item()))
