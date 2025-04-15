import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score

# 获取独热编码和标准化的数据集
df_encode_standed = pd.read_excel(r'D:\Document\desktop\1\test\result_final_machine_encode_standed.xlsx')  # 放入实际路径
# 划分特征和目标变量（标准化+独热编码）
X = df_encode_standed.drop('Churn', axis=1)
y = df_encode_standed['Churn']
# 划分训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# 应用SMOTE算法添加样本（标准化+独热编码）
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# 完整定义人工蜂鸟算法函数
def artificial_hummingbird_algorithm(pop_size, dim, lb, ub, max_iter, fitness_function):
    """
    人工蜂鸟算法函数

    参数:
    pop_size (int): 种群大小，即蜂鸟个体的数量
    dim (int): 问题的维度，也就是每个个体的参数数量
    lb (list or tuple or np.ndarray): 每个维度的下限值，可以是列表、元组或数组形式
    ub (list or tuple or np.ndarray): 每个维度的上限值，与lb对应，维度相同
    max_iter (int): 最大迭代次数
    fitness_function (function): 适应度函数，用于评估每个个体的优劣

    返回:
    best_position (np.ndarray): 找到的最优个体的位置（即最优参数组合）
    best_fitness (float): 最优个体对应的适应度值
    """
    # 初始化种群位置，确保每个维度的取值在上下界范围内
    positions = np.random.uniform(lb, ub, (pop_size, dim))
    # 初始化每个个体的速度（用于位置更新，模拟飞行速度，这里简单初始化为0向量，后续可调整更新策略）
    velocities = np.zeros((pop_size, dim))
    # 初始化每个个体的适应度值
    fitness = np.zeros(pop_size)
    # 记录全局最优个体的位置和适应度值
    global_best_position = positions[0].copy()
    global_best_fitness = -np.inf

    # 开始迭代
    for iter in range(max_iter):
        # 计算当前种群中每个个体的适应度值
        for i in range(pop_size):
            fitness[i] = fitness_function(positions[i])
            # 更新全局最优个体
            if fitness[i] > global_best_fitness:
                global_best_fitness = fitness[i]
                global_best_position = positions[i].copy()

        # 个体位置更新（模拟蜂鸟飞行过程中的位置变化，这里简单示例，可根据实际优化调整）
        for i in range(pop_size):
            # 这里可以模拟不同的飞行策略，比如借鉴粒子群算法等的速度更新和位置更新思路
            # 惯性权重，控制历史速度对当前速度的影响，可调整
            w = 0.5
            # 认知部分权重，个体自身经验对速度的影响权重，可调整
            c1 = 1.5
            # 社会部分权重，群体中其他个体对速度的影响权重，可调整
            c2 = 1.5
            # 随机生成两个影响因子，用于更新速度
            r1 = np.random.rand(dim)
            r2 = np.random.rand(dim)
            # 更新速度
            velocities[i] = w * velocities[i] + c1 * r1 * (global_best_position - positions[i]) + c2 * r2 * (
                    positions[np.random.choice(pop_size)] - positions[i])
            # 根据速度更新位置，同时确保位置在上下界范围内
            positions[i] = positions[i] + velocities[i]
            positions[i] = np.clip(positions[i], lb, ub)

    return global_best_position, global_best_fitness


# 定义随机森林模型
rf_model = RandomForestClassifier(random_state=42)

# 定义人工蜂鸟算法的适应度函数，这里以随机森林在验证集上的准确率为例
def fitness_function(params):
    n_estimators, max_depth, max_features = params
    # 对max_features进行额外验证和处理，确保其符合要求
    if isinstance(max_features, float):
        max_features = max(0.1, min(1.0, max_features))  # 将其限制在合法的浮点数范围内
    elif isinstance(max_features, int):
        max_features = max(1, min(int(len(X_resampled[0])), max_features))  # 根据数据特征数量限制整数范围
    else:
        max_features = 'sqrt'  # 如果是其他不合法类型，设置为默认合法取值'sqrt'

    rf_model.set_params(n_estimators=int(n_estimators), max_depth=int(max_depth), max_features=max_features)
    rf_model.fit(X_resampled, y_resampled)
    return rf_model.score(X_test, y_test)

# 人工蜂鸟算法的参数范围
param_bounds = [(10, 100), (5, 20), (0.1, 1.0)]

# 运行人工蜂鸟算法进行参数优化
best_params, best_fitness = artificial_hummingbird_algorithm(pop_size=20, dim=3, lb=[bound[0] for bound in param_bounds], ub=[bound[1] for bound in param_bounds],
                                                             max_iter=50, fitness_function=fitness_function)

# 输出最佳参数
print("# 最佳参数")
print("最佳估计器数量（n_estimators）:", best_params[0])
print("最佳最大深度（max_depth）:", best_params[1])
print("最佳最大特征数（max_features）:", best_params[2])

# 使用优化后的参数重新训练随机森林模型
best_n_estimators, best_max_depth, best_max_features = best_params
rf_model.set_params(n_estimators=int(best_n_estimators), max_depth=int(best_max_depth), max_features=best_max_features)
rf_model.fit(X_resampled, y_resampled)

# 在测试集上进行预测
y_pred = rf_model.predict(X_test)

# 准确率
accuracy = accuracy_score(y_test, y_pred)
print("# 准确率")
print(accuracy)

# 混淆矩阵
conf_mat = confusion_matrix(y_test, y_pred)
print("# 混淆矩阵")
print(conf_mat)

# 分类报告
class_report = classification_report(y_test, y_pred)
print("# 分类报告")
print(class_report)

# 计算 AUC 值
y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred_proba)
print("# 计算 AUC 值")
print(auc)