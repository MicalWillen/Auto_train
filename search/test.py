import numpy as np
import matplotlib.pyplot as plt

def positional_encoding(position, d_model):
    """
    生成位置编码矩阵。

    位置编码用于为序列中的每个位置添加唯一的表示，以便模型能够区分不同位置的元素。
    位置编码矩阵的计算公式如下：

    PE(pos, 2i) = sin(pos / 10000^(2i / d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))

    参数:
    position (int): 序列中的位置。
    d_model (int): 位置编码的维度。

    返回:
    numpy.ndarray: 位置编码矩阵。
    """
    """生成位置编码矩阵。"""
    angle_rads = position / np.power(10000, (2 * (np.arange(d_model) // 2)) / np.float32(d_model))
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
    return angle_rads

# 设置参数
position = np.arange(80)[:, np.newaxis] #位置
d_model = 128 #维度

# 生成位置编码
pos_encoding = positional_encoding(position, d_model)

# 保存为numpy数组
np.save('positional_encoding.npy', pos_encoding)

# 打印具体的数值
print(pos_encoding)

# 可视化
plt.figure(figsize=(10, 6))
plt.pcolormesh(pos_encoding, cmap='RdBu')
plt.xlabel('Dimension')
plt.xlim((0, d_model))
plt.ylabel('Position')
plt.colorbar()
plt.show()