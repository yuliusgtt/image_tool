import os
from rembg import remove
from PIL import Image
import subprocess

file_path = input("Enter the image file name or path: ")
directory = os.path.dirname(file_path)
file = os.path.basename(file_path)
filename, _ = os.path.splitext(file)

def compress_png_with_pngquant(png_path):
    try:
        subprocess.run([
            'pngquant',
            '--quality=65-90',
            '--ext', '.png',
            '--force',
            png_path
        ], check=True)
        print(f"Compressed {png_path} successfully.")
    except subprocess.CalledProcessError:
        print(f"Error compressing {png_path}.")
        
try:
    img = Image.open(file_path)
    no_bg = remove(img)

    output_dir = os.path.join(directory, f"img_bg_rm_{filename}")
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, f"{filename}.png")
    no_bg.save(png_path)
    compress_png_with_pngquant(png_path)

    print(f'Files saved in {output_dir}')
except FileNotFoundError:
    print('The specified file was not found. Please check the file path and try again.')
except IOError:
    print('The specified file is not a valid image or cannot be opened.')