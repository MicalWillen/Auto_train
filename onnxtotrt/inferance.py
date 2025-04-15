import cv2
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

# 加载 TensorRT 模型
def load_engine(trt_file_path):
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    with open(trt_file_path, 'rb') as f, trt.Runtime(TRT_LOGGER) as runtime:
        engine = runtime.deserialize_cuda_engine(f.read())
    return engine

# 分配内存缓冲区
def allocate_buffers(engine):
    inputs = []
    outputs = []
    bindings = []
    stream = cuda.Stream()
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        host_mem = cuda.pagelocked_empty(size, dtype)
        dev_mem = cuda.mem_alloc(host_mem.nbytes)
        bindings.append(int(dev_mem))
        if engine.binding_is_input(binding):
            inputs.append((host_mem, dev_mem))
        else:
            outputs.append((host_mem, dev_mem))
    return inputs, outputs, bindings, stream

# 图像预处理
def preprocess_image(image_path, input_width, input_height):
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (input_width, input_height))
    # BGR -> RGB, normalization
    image_resized = image_resized.transpose((2, 0, 1)).astype(np.float32) / 255.0
    return image_resized, image  # 返回原始图像用于绘制框

# 推理函数
def infer(context, bindings, inputs, outputs, stream, image):
    np.copyto(inputs[0][0], image.ravel())
    [cuda.memcpy_htod_async(inp[1], inp[0], stream) for inp in inputs]
    context.execute_async(bindings=bindings, stream_handle=stream.handle)
    [cuda.memcpy_dtoh_async(out[0], out[1], stream) for out in outputs]
    stream.synchronize()
    return [out[0] for out in outputs]

# 绘制边界框
def draw_boxes(image, results, conf_threshold=0.5):
    # 假设 results 是模型推理结果，包含 [x_min, y_min, x_max, y_max, confidence, class_id] 
    for result in results:
        x_min, y_min, x_max, y_max, confidence, class_id = result
        if confidence > conf_threshold:
            # 绘制矩形框
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            # 绘制置信度
            label = f"{class_id}: {confidence:.2f}"
            cv2.putText(image, label, (int(x_min), int(y_min)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

# 主函数
def main():
    trt_file_path = r'D:\Document\desktop\1\onnxtotrt\model.trt'  # TensorRT 模型文件路径
    image_path = r'D:\Document\desktop\1\onnxtotrt\2024-12-20-16-54-04-054_1_2.bmp'  # 待推理的图像文件路径

    engine = load_engine(trt_file_path)
    context = engine.create_execution_context()
    inputs, outputs, bindings, stream = allocate_buffers(engine)
    input_shape = engine.get_binding_shape(0)
    input_width, input_height = input_shape[2], input_shape[3]

    # 预处理图像
    processed_image, original_image = preprocess_image(image_path, input_width, input_height)

    # 推理
    results = infer(context, bindings, inputs, outputs, stream, processed_image)

    # 假设模型的结果包含边界框信息：[x_min, y_min, x_max, y_max, confidence, class_id]
    # 例如，推理结果是一个包含多个检测框的列表
    # 这里的结果应根据你的模型格式来解析
    # 注意：你需要根据模型的输出格式修改这里的代码
    boxes = results[0]  # 假设这是模型的输出结果
    detections = []
    max_confidence=[]
    for i in range(0, len(boxes), 6):  # 假设每个框包含 6 个值：x_min, y_min, x_max, y_max, confidence, class_id
        if boxes[i+4]>2500:
            x_min = boxes[i]
            y_min = boxes[i+1]
            x_max = boxes[i+2]
            y_max = boxes[i+3]
            max_confidence.append(boxes[i+4])
            confidence = boxes[i+4]
            class_id = int(boxes[i+5])
            detections.append([x_min, y_min, x_max, y_max, confidence, class_id])
    print(max(max_confidence))
    # 绘制框在原始图像上
    result_image = draw_boxes(original_image, detections)

    # 显示结果
    cv2.imshow('Detection Result', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
