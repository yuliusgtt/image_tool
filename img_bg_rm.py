import os
from rembg import remove
from PIL import Image
import subprocess

file_path = input("Enter the image file name or path: ")
directory = os.path.dirname(file_path)
file = os.path.basename(file_path)
filename, _ = os.path.splitext(file)

try:
    img = Image.open(file_path)
    no_bg = remove(img)

    output_dir = os.path.join(directory, f"img_bg_rm_{filename}")
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, f"{filename}.png")
    no_bg.save(png_path, optimize=True)

    print(f'Files saved in {output_dir}')
except FileNotFoundError:
    print('The specified file was not found. Please check the file path and try again.')
except IOError:
    print('The specified file is not a valid image or cannot be opened.')