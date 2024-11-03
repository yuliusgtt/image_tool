import os
from PIL import Image
import base64
import svgwrite

file_path = input("Enter the image file name or path: ")
directory = os.path.dirname(file_path)
file = os.path.basename(file_path)
filename, _ = os.path.splitext(file)

try:
    img = Image.open(file_path)
    aspect_ratio = img.width / img.height
    if aspect_ratio > 1:
        new_width = 512
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = 512
        new_width = int(new_height * aspect_ratio)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    background = Image.new('RGBA', (512, 512), (255, 255, 255, 0))
    offset = ((512 - new_width) // 2, (512 - new_height) // 2)
    background.paste(img, offset, img.convert('RGBA'))

    output_dir = os.path.join(directory, f"logo_output_{filename}")
    os.makedirs(output_dir, exist_ok=True)

    png_path = os.path.join(output_dir, f"{filename}.png")
    background.save(png_path)
    
    ico_path = os.path.join(output_dir, f"{filename}.ico")
    background.save(ico_path, format='ICO', sizes=[(48, 48)])
    
    svg_path = os.path.join(output_dir, f"{filename}.svg")
    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(512, 512))
    
    with open(png_path, "rb") as image_file:
        encoded_png = base64.b64encode(image_file.read()).decode()

    dwg.add(dwg.image(href=f"data:image/png;base64,{encoded_png}", insert=(0, 0), size=("512px", "512px")))
    dwg.save()

    print(f'Files saved in {output_dir}')
except FileNotFoundError:
    print('The specified file was not found. Please check the file path and try again.')
except IOError:
    print('The specified file is not a valid image or cannot be opened.')