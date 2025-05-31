import os
from rembg import remove
from PIL import Image
import numpy as np
import cv2

file_path = input("Enter the image file name or path: ")
directory = os.path.dirname(file_path)
file = os.path.basename(file_path)
filename, _ = os.path.splitext(file)

try:
    img = Image.open(file_path)
    no_bg = remove(img)
    cv_image = np.array(no_bg.convert("RGBA"))
    
    # Create mask for outline
    gray = cv2.cvtColor(cv_image, cv2.COLOR_RGBA2GRAY)
    _, alpha = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(alpha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create outline
    outline = np.zeros_like(cv_image)
    cv2.drawContours(outline, contours, -1, (255, 255, 255, 255), 10)  # White stroke of 10px
    
    # Composite stroke under original
    combined = Image.alpha_composite(Image.fromarray(outline), Image.fromarray(cv_image))

    output_dir = os.path.join(directory, f"sticker_output_{filename}")
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, f"{filename}.png")
    combined.save(png_path)

    print(f'Files saved in {output_dir}')
except FileNotFoundError:
    print('The specified file was not found. Please check the file path and try again.')
except IOError:
    print('The specified file is not a valid image or cannot be opened.')