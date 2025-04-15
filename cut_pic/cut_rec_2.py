import os
from PIL import Image


def crop_to_grid(input_image_folder, input_label_folder, output_image_folder, output_label_folder, grid_size=1024,
                 overlap=200):
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)
    if not os.path.exists(output_label_folder):
        os.makedirs(output_label_folder)

    for filename in os.listdir(input_image_folder):
        if filename.endswith(".bmp"):
            image_path = os.path.join(input_image_folder, filename)
            label_path = os.path.join(input_label_folder, filename.replace(".bmp", ".txt"))

            # Load image
            with Image.open(image_path) as img:
                width, height = img.size

                # Calculate step size (taking overlap into account)
                step_size = grid_size - overlap

                # Iterate over image grid
                for i in range(0, width, step_size):
                    for j in range(0, height, step_size):
                        # Define the cropping area
                        left = i
                        top = j
                        right = min(i + grid_size, width)
                        bottom = min(j + grid_size, height)

                        # Crop the image
                        cropped_img = img.crop((left, top, right, bottom))
                        cropped_width, cropped_height = cropped_img.size

                        # Generate new filename with suffix
                        suffix = f"_x{i}_y{j}"
                        cropped_filename = filename.replace(".bmp", f"{suffix}.bmp")
                        cropped_img.save(os.path.join(output_image_folder, cropped_filename))

                        # Adjust and save labels for the cropped image
                        if os.path.exists(label_path):
                            with open(label_path, 'r') as label_file:
                                labels = label_file.readlines()

                            new_labels = []
                            for label in labels:
                                parts = label.strip().split()
                                if len(parts) == 5:
                                    class_id, cx, cy, w, h = parts
                                    cx = float(cx) * width
                                    cy = float(cy) * height
                                    w = float(w) * width
                                    h = float(h) * height

                                    # Check if the center of the bounding box is within the current crop
                                    if (left <= cx <= right) and (top <= cy <= bottom):
                                        # Adjust the bounding box for the cropped image
                                        new_cx = (cx - left) / cropped_width
                                        new_cy = (cy - top) / cropped_height
                                        new_w = w / cropped_width
                                        new_h = h / cropped_height

                                        new_labels.append(
                                            f"{class_id} {new_cx:.6f} {new_cy:.6f} {new_w:.6f} {new_h:.6f}")

                            # Save new labels
                            new_label_filename = filename.replace(".bmp", f"{suffix}.txt")
                            new_label_path = os.path.join(output_label_folder, new_label_filename)
                            with open(new_label_path, 'w') as new_label_file:
                                new_label_file.write("\n".join(new_labels))


if __name__ == "__main__":
    input_image_folder = r"D:\xinwu\241022\G41\img\15-1\cut1"
    input_label_folder = r"D:\xinwu\241022\G41\img\15-1\cut1"
    output_image_folder = r"D:\xinwu\241022\G41\img\15-1\cut2"
    output_label_folder = r"D:\xinwu\241022\G41\img\15-1\cut2"

    grid_size = 1024  # Size of the grid for cropping
    overlap = 200  # Overlap between crops

    crop_to_grid(input_image_folder, input_label_folder, output_image_folder, output_label_folder, grid_size, overlap)
