from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

# 定义意图类别
intent_labels = ["Check the weather", "Restaurant Reservations", "play music","Asking for price"]

# 加载预训练的 RoBERTa 模型和分词器
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=len(intent_labels))

# 输入文本
text = "How much is this lollipop?"
inputs = tokenizer(text, return_tensors='pt')

# 进行预测
outputs = model(**inputs)
logits = outputs.logits

# 计算概率
probs = torch.softmax(logits, dim=1)
predicted_intent_idx = torch.argmax(probs, dim=1).item()
predicted_intent = intent_labels[predicted_intent_idx]

# 输出结果
print(f"Predicted Intent: {predicted_intent}")