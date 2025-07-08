import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_yoloseg_polygon(txt_path, image_shape):
    h, w = image_shape[:2]
    with open(txt_path, 'r') as f:
        line = f.readline().strip().split()
        class_id = int(line[0])
        points = np.array(line[1:], dtype=np.float32).reshape(-1, 2)
        points[:, 0] *= w
        points[:, 1] *= h
        return points.astype(np.int32)

def create_mask_from_polygon(polygon, image_shape):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], 255)
    return mask

def draw_rotated_rect(img, rect, color=(0, 255, 0), thickness=2):
    x, y, w, h, angle = rect
    box = cv2.boxPoints(((x, y), (w, h), angle))
    box = box.astype(np.int32)
    cv2.drawContours(img, [box], 0, color, thickness)
    return box

def get_max_inner_rectangles(matrix_np: np.ndarray, rectangle_bbox: list, area_value: int, result_list: list,
                             cur_area: float = float('inf')) -> list:
    """
    递归获取空间的多个内接矩形
    Args:
        matrix_np: 包含空间的底图
        rectangle_bbox: 空间的外接矩形
        area_value: 最小面积阈值
        result_list: 内接矩形列表
        cur_area: 当前矩形的面积
    Returns:
        result_list: 内接矩形列表
    """
    xmin, ymin, xmax, ymax = rectangle_bbox
    crop_img = matrix_np[ymin:ymax, xmin:xmax]  # 通过最大外接矩形，crop包含该空间的区域，优化速度
    matrix_list = crop_img.tolist()

    row = len(matrix_list)
    col = len(matrix_list[0])
    height = [0] * (col + 2)
    res = 0  # 记录矩形内像素值相加后的最大值
    bbox_rec = None  # 最大内接矩形bbox
    for i in range(row):
        stack = []  # 利用栈的特性获取最大矩形区域
        for j in range(col + 2):
            if 1 <= j <= col:
                if matrix_list[i][j - 1] == 255:
                    height[j] += 1
                else:
                    height[j] = 0
            # 精髓代码块 计算最大内接矩形 并计算最大值
            while stack and height[stack[-1]] > height[j]:
                cur = stack.pop()
                if res < (j - stack[-1] - 1) * height[cur]:
                    res = (j - stack[-1] - 1) * height[cur]
                    bbox_rec = [stack[-1], i - height[cur], j, i]
            stack.append(j)

    # 递归停止条件，1.最大内接矩形面积小于阈值；2. 没有最大内接矩形
    if cur_area < area_value or not bbox_rec:
        return result_list
    # 映射到原图中的位置
    src_min_x = xmin + bbox_rec[0]
    src_min_y = ymin + bbox_rec[1]
    src_max_x = xmin + bbox_rec[2]
    src_max_y = ymin + bbox_rec[3]
    bbox_src_position = [src_min_x, src_min_y, src_max_x, src_max_y]
    # 转成np格式，并将已经找到的最大内接矩形涂黑
    bbox_cnt = [[bbox_src_position[0], bbox_src_position[1]], 
                [bbox_src_position[2], bbox_src_position[1]], 
                [bbox_src_position[2], bbox_src_position[3]], 
                [bbox_src_position[0], bbox_src_position[3]]]
    contour_cur_np = np.array(bbox_cnt).reshape(-1, 1, 2)
    cv2.polylines(matrix_np, [contour_cur_np], 1, 0)
    cv2.fillPoly(matrix_np, [contour_cur_np], 0)
    cur_area =  (bbox_rec[2] - bbox_rec[0]) * (bbox_rec[3] - bbox_rec[1])
    if cur_area > area_value:
        result_list.append(bbox_src_position)
    # 递归获取剩下的内接矩形
    get_max_inner_rectangles(matrix_np, rectangle_bbox, area_value, result_list, cur_area)

    return result_list

def get_largest_inner_rect(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("未找到任何轮廓")
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour.reshape(-1, 1, 2))
    cnt_bbox = [x, y, x + w, y + h]
    res_list = get_max_inner_rectangles(mask, cnt_bbox, 100, [])
    res_list = sorted(res_list, key=lambda _: (_[2] - _[0]) * (_[3] - _[1]), reverse=True)
    res = res_list[0]
    return (res[0] + (res[2] - res[0]) / 2, res[1] + (res[3] - res[1]) / 2, res[2] - res[0], res[3] - res[1], 0)

def main(image_path, txt_path, save_path="output.jpg"):
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"图像读取失败: {image_path}")
    
    # 读取多边形
    polygon = load_yoloseg_polygon(txt_path, img.shape)
    
    # 构造 mask
    mask = create_mask_from_polygon(polygon, img.shape)
    
    # 查找最大内接矩形
    try:
        rect = get_largest_inner_rect(mask)
    except Exception as e:
        print(f"计算最大内接矩形失败: {e}")
        return

    # 可视化
    vis_img = img.copy()
    cv2.polylines(vis_img, [polygon.reshape(-1, 1, 2)], isClosed=True, color=(255, 0, 0), thickness=2)
    draw_rotated_rect(vis_img, rect, color=(0, 255, 0), thickness=2)
    
    # 保存图片
    cv2.imwrite(save_path, vis_img)
    print(f"结果已保存为: {save_path}")

# 替换为你的图像路径和txt路径
main("opencv/labels/sharpened.jpg", "opencv/labels/sharpened.txt", "opencv/labels/result.jpg")