import os
import cv2
import numpy as np

import os
import cv2
import numpy as np
from shapely.geometry import Polygon, box, MultiPolygon
from shapely.validation import explain_validity, make_valid # Import make_valid
# import matplotlib.pyplot as plt # For visualization

def is_inside_mask(label_mask_points, region):
    x1, y1, x2, y2 = region
    polygon = np.array(label_mask_points, dtype=np.float32).reshape(-1, 2)
    # Check if centroid is within the region
    if polygon.shape[0] < 1: # Handle empty polygons
        return False
    cx, cy = np.mean(polygon[:, 0]), np.mean(polygon[:, 1])
    return x1 <= cx <= x2 and y1 <= cy <= y2

def crop_and_adjust_seg_label(label, crop_region, img_width, img_height, crop_w, crop_h):
    crop_x1, crop_y1, crop_x2, crop_y2 = crop_region
    class_id = int(label[0])
    mask_points = list(map(float, label[5:]))

    # Convert to absolute image coordinates
    abs_points = np.array([
        [mask_points[i] * img_width, mask_points[i + 1] * img_height]
        for i in range(0, len(mask_points), 2)
    ], dtype=np.float32)

    if len(abs_points) < 3: # A polygon needs at least 3 points
        # print(f"Skipping label due to too few points: {len(abs_points)}")
        return None

    # Convert to Shapely Polygon
    try:
        original_polygon_shapely = Polygon(abs_points)
    except Exception as e:
        print(f"Error creating Shapely Polygon from points: {abs_points}")
        print(f"Error: {e}")
        return None

    # --- Debugging: Check Validity BEFORE Intersection ---
    if not original_polygon_shapely.is_valid:
        validity_explanation = explain_validity(original_polygon_shapely)
        print(f"--- Invalid Polygon Detected! ---")
        print(f"Original points: {abs_points}")
        print(f"Validity reason: {validity_explanation}")
        print(f"Coordinates in error message: {crop_region}") # These are crop coordinates, not error points.
        # Plot the invalid polygon to see the issue
        # fig, ax = plt.subplots()
        x, y = original_polygon_shapely.exterior.xy
        # ax.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=1)
        # ax.set_title(f"Invalid Polygon: {validity_explanation}")
        # ax.set_aspect('equal', adjustable='box')
        # plt.show()
        # plt.close(fig)

        # Attempt to make the polygon valid
        original_polygon_shapely = make_valid(original_polygon_shapely)
        if not original_polygon_shapely.is_valid:
            print(f"Failed to make polygon valid. Skipping label.")
            return None
        else:
            print(f"Successfully made polygon valid!")
            if isinstance(original_polygon_shapely, MultiPolygon):
                 # make_valid might return MultiPolygon if it fixes self-intersections by splitting
                print(f"make_valid returned MultiPolygon. Taking largest.")
                largest_polygon = None
                max_area = 0
                for p in original_polygon_shapely.geoms:
                    if p.area > max_area:
                        max_area = p.area
                        largest_polygon = p
                original_polygon_shapely = largest_polygon
                if original_polygon_shapely is None or original_polygon_shapely.is_empty:
                    return None
            if not isinstance(original_polygon_shapely, Polygon):
                print(f"make_valid returned unexpected type after trying to fix: {type(original_polygon_shapely)}. Skipping.")
                return None


    # Check if the center is in the crop region (your existing logic)
    cx, cy = original_polygon_shapely.centroid.x, original_polygon_shapely.centroid.y
    if not (crop_x1 <= cx <= crop_x2 and crop_y1 <= cy <= crop_y2):
        return None

    # Define the cropping rectangle as a Shapely box
    cropping_bbox_shapely = box(crop_x1, crop_y1, crop_x2, crop_y2)

    # Perform the intersection (clipping)
    try:
        clipped_polygon_shapely = original_polygon_shapely.intersection(cropping_bbox_shapely)
    except Exception as e:
        print(f"Error during shapely intersection. Original polygon was valid: {original_polygon_shapely.is_valid}")
        print(f"Cropping bbox: {cropping_bbox_shapely}")
        print(f"Error: {e}")
        return None


    # Handle cases where clipping results in an empty geometry or MultiPolygon
    if clipped_polygon_shapely.is_empty:
        return None
    elif isinstance(clipped_polygon_shapely, Polygon):
        new_polygon_coords = np.array(clipped_polygon_shapely.exterior.coords)
    elif isinstance(clipped_polygon_shapely, MultiPolygon):
        largest_polygon = None
        max_area = 0
        for p in clipped_polygon_shapely.geoms:
            if p.area > max_area:
                max_area = p.area
                largest_polygon = p
        if largest_polygon is None or largest_polygon.is_empty:
            return None
        new_polygon_coords = np.array(largest_polygon.exterior.coords)
    else:
        # Handle other unexpected geometry types if necessary
        print(f"Clipping resulted in unexpected geometry type: {type(clipped_polygon_shapely)}")
        return None

    # Remove the last point if it's a duplicate of the first (Shapely often closes polygons)
    if len(new_polygon_coords) > 1 and np.allclose(new_polygon_coords[0], new_polygon_coords[-1]):
        new_polygon_coords = new_polygon_coords[:-1]

    # Check if the clipped polygon has enough points to form a valid polygon (e.g., at least 3 for a triangle)
    if len(new_polygon_coords) < 3:
        # print(f"Skipping clipped label due to too few points: {len(new_polygon_coords)}")
        return None

    # Offset to the cropped image's local coordinates
    new_polygon_coords[:, 0] -= crop_x1
    new_polygon_coords[:, 1] -= crop_y1

    # Normalize coordinates to the cropped image dimensions (0-1 range)
    norm_polygon_coords = new_polygon_coords.copy()
    # Ensure no division by zero if crop_w or crop_h is 0 (shouldn't happen with valid crop_region)
    if crop_w == 0 or crop_h == 0:
        return None

    norm_polygon_coords[:, 0] = np.clip(norm_polygon_coords[:, 0] / crop_w, 0, 1)
    norm_polygon_coords[:, 1] = np.clip(norm_polygon_coords[:, 1] / crop_h, 0, 1)

    # Recalculate bbox (x_center, y_center, w, h) based on the normalized clipped polygon
    xmin = np.min(norm_polygon_coords[:, 0])
    xmax = np.max(norm_polygon_coords[:, 0])
    ymin = np.min(norm_polygon_coords[:, 1])
    ymax = np.max(norm_polygon_coords[:, 1])
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    w = xmax - xmin
    h = ymax - ymin

    # Ensure bbox dimensions are positive (can be 0 for a line or point from extreme clipping)
    if w <= 0 or h <= 0:
        return None

    flat_polygon = norm_polygon_coords.flatten().tolist()
    return [class_id] + flat_polygon

def process_seg_image(image_path, label_path, output_image_folder, output_label_folder, crop_region):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return

    crop_x1, crop_y1, crop_x2, crop_y2 = crop_region
    crop = image[crop_y1:crop_y2, crop_x1:crop_x2]
    crop_h, crop_w = crop.shape[:2]

    output_labels = []

    # Check if label file exists before processing
    if os.path.exists(label_path):
        img_height, img_width = image.shape[:2]
        with open(label_path, 'r') as f:
            labels = [line.strip().split() for line in f if line.strip()]
        for label in labels:
            new_label = crop_and_adjust_seg_label(label, crop_region, img_width, img_height, crop_w, crop_h)
            if new_label is not None:
                output_labels.append(new_label)
    else:
        print(f"Label file does not exist: {label_path}")
        # If label file doesn't exist, you could either:
        # 1. Skip this image, or
        # 2. Create an empty label file (depending on your use case).

    # Save cropped image
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_image_path = os.path.join(output_image_folder, f"{base_name}_crop.png")
    output_label_path = os.path.join(output_label_folder, f"{base_name}_crop.txt")

    cv2.imwrite(output_image_path, crop)

    # Save labels if any exist
    if output_labels:
        with open(output_label_path, 'w') as f:
            for label in output_labels:
                f.write(" ".join(f"{x:.6f}" if isinstance(x, float) else str(x) for x in label) + '\n')
    else:
        # If no labels, you can either skip saving the label or create an empty label file
        with open(output_label_path, 'w') as f:
            pass  # Empty label file

def process_seg_folder(image_folder, label_folder, output_image_folder, output_label_folder, crop_region):
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_label_folder, exist_ok=True)

    for file in os.listdir(image_folder):
        if file.lower().endswith(".png"):
            image_path = os.path.join(image_folder, file)
            label_path = os.path.join(label_folder, file.replace(".png", ".txt"))
            process_seg_image(image_path, label_path, output_image_folder, output_label_folder, crop_region)

# 示例调用
if __name__ == "__main__":
    image_folder = r"/home2/item/jinlong/DCFZ/每日存/0610/20250609-61"
    label_folder = r"/home2/item/jinlong/DCFZ/每日存/0610/20250609-61"
    output_image_folder = r"/home2/item/jinlong/DCFZ/每日存/0610/l"
    output_label_folder = r"/home2/item/jinlong/DCFZ/每日存/0610/l"

    crop_region = (0, 640, 1080, 1920)  # x1, y1, x2, y2
    process_seg_folder(image_folder, label_folder, output_image_folder, output_label_folder, crop_region)
