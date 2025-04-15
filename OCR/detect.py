import onnxruntime as ort
import numpy as np
import cv2
import time

def inference(model_path, input_tensor):
    start = time.perf_counter()

    # 加载ONNX模型
    session = ort.InferenceSession(model_path, providers=ort.get_available_providers())

    # 获取输入和输出名称
    input_names = [model_inputs.name for model_inputs in session.get_inputs()]
    output_names = [model_outputs.name for model_outputs in session.get_outputs()]

    # 运行模型推理
    outputs = session.run(output_names, {input_names[0]: input_tensor})

    print(f"Inference time: {(time.perf_counter() - start) * 1000:.2f} ms")
    return outputs

def postprocess(outputs):
    """
    根据模型的输出格式，将其转换为可读文本。
    假设模型输出是字符索引序列。
    """
    # 示例：假设输出是一个字符索引的概率分布
    char_map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # 假设字符映射表
    detected_text = ""
    for output in outputs[0]:  # 遍历输出序列
        char_index = np.argmax(output)  # 获取概率最大的索引
        if char_index < len(char_map):  # 确保索引有效
            detected_text += char_map[char_index]
    return detected_text

# 示例：加载图像并进行推理
model_path = "/home/ps/AB/Code/1/OCR/ch_PP-OCRv4_det_infer.onnx"
image_path = "/home/ps/Desktop/test/微信图片_2025-04-11_143722_215.png"

# 加载图像并预处理
input_data = cv2.imread(image_path)
input_data = cv2.cvtColor(input_data, cv2.COLOR_BGR2RGB)
input_data = cv2.resize(input_data, (224, 224))
input_data = input_data.transpose(2, 0, 1)
input_data = input_data[np.newaxis, :]
input_data = input_data.astype(np.float32)

# 进行推理
outputs = inference(model_path, input_data)

# 后处理并输出结果
detected_text = postprocess(outputs)
print("Detected Text:", detected_text)