import os
from pathlib import Path
import time

from tqdm import tqdm

def split_line(line, separator):
    """Split a line by the given separator."""
    return line.strip().split(separator)

def main():
    change_label = False
    turn_around = True
    enhance_num = 5

    source_path = Path(r"D:\FR\test\crush1\3")

    if not source_path.exists():
        print(f"Source path does not exist: {source_path}")
        return

    for file in tqdm(source_path.iterdir()):
        if file.suffix != ".bmp":
            continue

        txt_file = source_path / f"{file.stem}.txt"
        if not txt_file.exists():
            print(f"Fail to open the label: {txt_file}")
            continue

        with open(txt_file, 'r') as myfile:
            lines = myfile.readlines()

        point_x = []
        point_y = []
        temp_AnC, temp_C, temp_H, temp_R, temp_V = "", "", "", "", ""
        class_idx = ""

        for line in lines:
            label = split_line(line, ' ')
            class_idx = label[0]

            for i in range(1, len(label)):
                if i % 2 == 1:
                    point_x.append(float(label[i]))
                else:
                    point_y.append(float(label[i]))

        temp_AnC += class_idx
        temp_C += class_idx
        temp_H += class_idx
        temp_R += class_idx
        temp_V += class_idx

        for i in range(len(point_x)):
            temp_AnC += f" {point_y[i]} {1 - point_x[i]}"
            temp_C += f" {1 - point_y[i]} {point_x[i]}"
            temp_H += f" {point_x[i]} {1 - point_y[i]}"
            temp_R += f" {1 - point_x[i]} {1 - point_y[i]}"
            temp_V += f" {1 - point_x[i]} {point_y[i]}"

        temp_AnC += "\n"
        temp_C += "\n"
        temp_H += "\n"
        temp_R += "\n"
        temp_V += "\n"

        output_files = {
            "anticlockwise90": temp_AnC,
            "clockwise": temp_C,
            "horizontal": temp_H,
            "rotate180": temp_R,
            "vertical": temp_V
        }

        for suffix, content in output_files.items():
            output_file = source_path / f"{file.stem}_{suffix}.txt"
            with open(output_file, 'w') as outfile:
                outfile.write(content)

       

if __name__ == "__main__":
    main()
