import tensorrt as trt
import os

# 加载 ONNX 模型并将其转换为 TensorRT 引擎
def convert_onnx_to_trt(onnx_model_path, trt_model_path, max_workspace_size=1 << 28, fp16_mode=False):
    # 创建日志记录器
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    
    # 加载 ONNX 模型并解析
    with open(onnx_model_path, 'rb') as onnx_file:
        # 创建 TensorRT 构建器
        builder = trt.Builder(TRT_LOGGER)
        network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))  # 显式批次
        parser = trt.OnnxParser(network, TRT_LOGGER)
        
        # 解析 ONNX 模型
        if not parser.parse(onnx_file.read()):
            print("ERROR: Failed to parse the ONNX model.")
            for error in range(parser.num_errors):
                print(parser.get_error(error))
            return None
        
        # 设置构建器配置
        config = builder.create_builder_config()
        
        # 设置最大工作空间大小
        config.max_workspace_size = max_workspace_size
        
        # 启用 FP16 精度（如果支持）
        if fp16_mode and builder.platform_has_fast_fp16:
            config.set_flag(trt.BuilderFlag.FP16)
        
        # 构建 TensorRT 引擎
        engine = builder.build_engine(network, config)
        
        if engine is None:
            print("ERROR: Failed to build the engine.")
            return None
        
        # 序列化并保存 TensorRT 引擎
        with open(trt_model_path, "wb") as trt_file:
            trt_file.write(engine.serialize())
            print(f"TensorRT engine saved to {trt_model_path}")
        
        return engine

# 主函数
def main():
    # ONNX 模型文件路径
    onnx_model_path = r'D:\Document\desktop\1\onnxtotrt\station6_back_v4.onnx'  # 替换为实际路径
    # 输出的 TensorRT 引擎文件路径
    trt_model_path = r'D:\Document\desktop\1\onnxtotrt\model.trt'  # 替换为实际路径
    
    # 转换 ONNX 模型为 TensorRT 引擎
    convert_onnx_to_trt(onnx_model_path, trt_model_path)

if __name__ == '__main__':
    main()
