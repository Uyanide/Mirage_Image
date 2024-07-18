import sys
from PIL import Image

if len(sys.argv) < 2:
    print('Usage: python convert_png.py <image_path>')
    sys.exit(1)

image_path = sys.argv[1]
img = Image.open(image_path)
img.save(image_path[:image_path.rfind('.')] + '.png', 'PNG')