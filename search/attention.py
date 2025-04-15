import tensorflow as tf
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.python.keras import layers, models

# 定义一个简单的自注意力层
class SelfAttention(layers.Layer):
    def __init__(self):
        super(SelfAttention, self).__init__()

    def build(self, input_shape):
        self.Wq = self.add_weight(shape=(input_shape[-1], input_shape[-1]), initializer='random_normal', trainable=True)
        self.Wk = self.add_weight(shape=(input_shape[-1], input_shape[-1]), initializer='random_normal', trainable=True)
        self.Wv = self.add_weight(shape=(input_shape[-1], input_shape[-1]), initializer='random_normal', trainable=True)

    def call(self, inputs):
        Q = tf.matmul(inputs, self.Wq)  # Query
        K = tf.matmul(inputs, self.Wk)  # Key
        V = tf.matmul(inputs, self.Wv)  # Value

        # 计算注意力权重
        attention_weights = tf.nn.softmax(tf.matmul(Q, K, transpose_b=True) / tf.sqrt(tf.cast(tf.shape(inputs)[-1], tf.float32)), axis=-1)

        # 根据权重加权平均Value
        output = tf.matmul(attention_weights, V)
        return output

# 加载预训练的GloVe词向量
def load_glove_embeddings(filepath, word_index, embedding_dim=100):
    embeddings_index = {}
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

    embedding_matrix = np.zeros((len(word_index) + 1, embedding_dim))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return embedding_matrix

# 示例评论数据
texts = [
    "This book is amazing, very interesting and captivating.",
    "I found the book boring and dull, I couldn't finish it.",
    "The plot was really engaging, I enjoyed reading it.",
    "It was a waste of time, very boring and uninteresting.",
]

# 对应的标签（1表示正面情感，0表示负面情感）
labels = [1, 0, 1, 0]

# 使用Tokenizer对文本进行分词和向量化
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(texts)

# 将文本转换为数字序列
sequences = tokenizer.texts_to_sequences(texts)

# 填充序列，使其具有相同的长度
X = pad_sequences(sequences, padding='post', maxlen=20)

# 将标签转化为numpy数组
y = np.array(labels)

# 加载GloVe词向量
embedding_dim = 100
embedding_matrix = load_glove_embeddings(r'D:\Document\desktop\1\search\glove.6B.100d.txt', tokenizer.word_index, embedding_dim)

# 构建模型
model = models.Sequential([
    layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim, weights=[embedding_matrix], input_length=20, trainable=False),
    SelfAttention(),
    layers.GlobalAveragePooling1D(),  # 对每个序列的输出进行池化
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')  # 输出0或1
])

# 编译模型
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# 训练模型
model.fit(X, y, epochs=1000, batch_size=2)

# 测试数据
test_texts = [
    "This movie was fantastic, I loved it!",
    "It was the worst movie I have ever watched."
]

# 对测试文本进行相同的预处理
test_sequences = tokenizer.texts_to_sequences(test_texts)
test_X = pad_sequences(test_sequences, padding='post', maxlen=20)

# 进行预测
predictions = model.predict(test_X)

for i, text in enumerate(test_texts):
    sentiment = "Positive" if predictions[i] > 0.5 else "Negative"
    print(f"Review: {text}")
    print(f"Sentiment: {sentiment}")