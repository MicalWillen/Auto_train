from pydantic import Field
import torch
from torchtext.datasets import IMDB

import torch.nn as nn
import torch.optim as optim

# 定义文本字段和标签字段
TEXT = Field(tokenize='spacy', lower=True)
LABEL = Field(sequential=False, use_vocab=False)

# 定义数据集和迭代器
train_data, test_data = IMDB.splits(TEXT, LABEL)
train_iterator, test_iterator = BucketIterator.splits(
    (train_data, test_data), 
    batch_size=64, 
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
)

# 加载预训练词向量
TEXT.build_vocab(train_data, max_size=10000, vectors="glove.6B.100d", unk_init=torch.Tensor.normal_)

class RNN(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(input_dim, embedding_dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, text):
        # 将文本转化为词嵌入
        embedded = self.embedding(text)
        # 对词嵌入应用RNN
        output, hidden = self.rnn(embedded)
        # 取RNN的最后一个输出
        assert torch.equal(output[-1,:,:], hidden.squeeze(0))
        # 通过全连接层进行分类
        return self.fc(hidden.squeeze(0))

INPUT_DIM = len(TEXT.vocab)
EMBEDDING_DIM = 100
HIDDEN_DIM = 256
OUTPUT_DIM = 1

model = RNN(INPUT_DIM, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM)
predictor = model.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

optimizer = optim.Adam(predictor.parameters())
criterion = nn.BCEWithLogitsLoss()

def train(model, iterator, optimizer, criterion):
    model.train()
    epoch_loss = 0
    for batch in iterator:
        text, labels = batch.text.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu')), batch.label.float().unsqueeze(1).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        optimizer.zero_grad()
        predictions = model(text).squeeze(1)
        loss = criterion(predictions, labels)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    return epoch_loss / len(iterator)

N_EPOCHS = 5
for epoch in range(N_EPOCHS):
    train_loss = train(predictor, train_iterator, optimizer, criterion)
    print(f'Epoch: {epoch+1:02}, Train Loss: {train_loss:.3f}')