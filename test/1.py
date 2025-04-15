import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint as cp
from torch.jit.annotations import List
from timm.models.layers import BatchNormAct2d
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 设置随机种子以便复现
torch.manual_seed(0)

# 超参数
batch_size = 64
learning_rate = 0.001
num_epochs = 5

# 数据预处理
transform = transforms.Compose([
    transforms.ToTensor(),  # 将图像转换为张量
    transforms.Normalize((0.5,), (0.5,))  # 归一化
])

# 下载 MNIST 数据集
train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
test_dataset = datasets.MNIST(root='./data', train=False, transform=transform, download=True)

# 创建数据加载器
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)
class DenseLayer(nn.Module):
    def __init__(
            self, int_numss, gr, bs, norm_layer=BatchNormAct2d,
            drop_rate=0., memory_efficient=False):
        super(DenseLayer, self).__init__()
        self.add_module('norm1', norm_layer(int_numss)),
        self.add_module('conv1', nn.Conv2d(
            int_numss, bs * gr, kernel_size=1, stride=1, bias=False)),
        self.add_module('norm2', norm_layer(bs * gr)),
        self.add_module('conv2', nn.Conv2d(
            bs * gr, gr, kernel_size=3, stride=1, padding=1, bias=False)),
        self.drop_rate = float(drop_rate)
        self.memory_efficient = memory_efficient

    def bottleneck_fn(self, xs):
        concated_features = torch.cat(xs, 1)
        bottleneck_output = self.conv1(self.norm1(concated_features))  # noqa: T484
        return bottleneck_output

    def any_requires_grad(self, x):
        for tensor in x:
            if tensor.requires_grad:
                return True
        return False

    @torch.jit.unused  # noqa: T484
    def call_checkpoint_bottleneck(self, x):
        def closure(*xs):
            return self.bottleneck_fn(xs)

        return cp.checkpoint(closure, *x)

    @torch.jit._overload_method  # mango noqa: F811
    def forward(self, x):
        pass

    @torch.jit._overload_method  # noqa: F811
    def forward(self, x):
        pass

    def forward(self, x):  # noqa: F811 iscyy/mango
        if isinstance(x, torch.Tensor):
            prev_features = [x]
        else:
            prev_features = x
        if self.memory_efficient and self.any_requires_grad(prev_features):
            if torch.jit.is_scripting():
                raise Exception("Memory Efficient not supported in JIT")
            bottleneck_output = self.call_checkpoint_bottleneck(prev_features)
        else:
            bottleneck_output = self.bottleneck_fn(prev_features)
        new_features = self.conv2(self.norm2(bottleneck_output))
        if self.drop_rate > 0:
            new_features = F.dropout(new_features, p=self.drop_rate, training=self.training)
        return new_features
    


# 初始化网络、损失函数和优化器
model = DenseLayer(gr=32,int_numss=10,bs=2)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 训练模型
for epoch in range(num_epochs):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()  # 清零梯度
        outputs = model(images)  # 向前传播
        loss = criterion(outputs, labels)  # 计算损失
        loss.backward()  # 反向传播
        optimizer.step()  # 更新参数

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# 测试模型
model.eval()  # 切换到评估模式
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f'Accuracy of the model on the test images: {100 * correct / total:.2f}%')