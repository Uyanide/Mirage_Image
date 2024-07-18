import sys

# 读取命令行参数
if len(sys.argv) != 2:
    print('Usage: python set_transparency.py <image_path>')
    exit(1)
image_path = sys.argv[1]

from PIL import Image

# 打开图片，转为带有alpha通道的灰度图
img = Image.open(image_path).convert('LA')
pixels = img.load()
# 如果像素坐标的横纵坐标之和为偶数, 则将该像素的alpha通道值设为0
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if (i + j) % 2 == 0:
            r, a = pixels[i, j]
            pixels[i, j] = (r, 0)

# 保存图片
img.save('output.png')