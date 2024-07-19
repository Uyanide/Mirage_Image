from PIL import Image

# 常量定义
# merge默认参数
LIMIT_INNER = 32
LIMIT_COVER = 64
HIDING_RATE = 2
# 输出图像尺寸默认参数
MAX_SIZE = 1200
# 输出图像保存参数
JPEG_QUALITY = 95
JPEG_SUBSAMPLING = '4:4:4'


class Mirage_Image_Colored:
    @staticmethod
    def load_inner_image(image_path, max_size = MAX_SIZE):
        '''
        加载里图, 限制最大尺寸, 进行缩放
        :param image_path: 图片路径
        :param max_size: 最大尺寸
        :return: 图片对象
        '''
        img = Image.open(image_path).convert('RGB')
        # 限制最大尺寸，进行缩放
        img.thumbnail((max_size, max_size), Image.LANCZOS)
        return img

    @staticmethod
    def load_cover_image(image_path, target_size):
        '''
        加载表图, 根据里图尺寸裁剪并缩放
        :param image_path: 图片路径
        :param target_size: 目标尺寸
        :return: 图片对象
        '''
        img = Image.open(image_path).convert('RGB')
        # 比较表里图的宽高比，确定裁剪区域
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        if target_ratio > img_ratio:
            new_height = int(img.width / target_ratio)
            crop_area = (0, (img.height - new_height) // 2, img.width, (img.height + new_height) // 2)
        else:
            new_width = int(img.height * target_ratio)
            crop_area = ((img.width - new_width) // 2, 0, (img.width + new_width) // 2, img.height)
        # 裁剪并缩放
        cropped_img = img.crop(crop_area)
        resized_img = cropped_img.resize(target_size, Image.Resampling.LANCZOS)
        return resized_img

    def __init__(self, inner_path, cover_path, max_size = MAX_SIZE):
        self.inner_path = inner_path
        self.cover_path = cover_path
        self.inner_img = self.load_inner_image(inner_path, max_size)
        self.cover_img = self.load_cover_image(cover_path, self.inner_img.size)

    def get_pixels(self):
        return self.inner_img.load(), self.cover_img.load()

    def merge(self, limit_inner = LIMIT_INNER, limit_cover = LIMIT_COVER, hiding_rate = HIDING_RATE):
        '''
        生成隐写图
        :param inner_img: 里图对象
        :param cover_img: 表图对象
        :param limit_inner: 里图色阶限制
        :param hiding_rate: 表图色阶限制
        :param hiding_rate: 隐藏率, 即表图中每hiding_rate个像素隐藏一个里图像素, 越大隐写效果越明显
        :return output_img: 隐写图对象

        正向隐写(limit_inner <= limit_cover): 即里图向0偏移, 表图向255偏移
        反向隐写(limit_inner > limit_cover): 即里图向255偏移, 表图向0偏移
        '''
        pixels_inner, pixels_cover = self.get_pixels()
        output_img = Image.new('RGB', self.inner_img.size)
        pixels_output = output_img.load()

        if limit_inner <= limit_cover:
            compress_rate_inner = limit_inner / 255
            compress_rate_cover = (255 - limit_cover) / 255
            compress_inner = lambda x: int(x * compress_rate_inner)
            compress_cover = lambda x: int(x * compress_rate_cover + limit_cover)
        else:
            compress_rate_inner = (255 - limit_inner) / 255
            compress_rate_cover = limit_cover / 255
            compress_inner = lambda x: int(x * compress_rate_inner + limit_inner)
            compress_cover = lambda x: int(x * compress_rate_cover)

        for i in range(self.inner_img.size[0]):
            for j in range(self.inner_img.size[1]):
                # 表里图交替隐藏
                # 里图像素值向0偏移
                if (i + j) % hiding_rate == 0:
                    compress = compress_inner
                    r, g, b = pixels_inner[i, j]
                # 表图像素值向255偏移
                else:
                    compress = compress_cover
                    r, g, b = pixels_cover[i, j]
                pixels_output[i, j] = (compress(r), compress(g), compress(b))
        return output_img


class Mirage_Image_Gray(Mirage_Image_Colored):
    def get_pixels(self):
        return self.inner_img.load(), self.cover_img.convert('L').convert('RGB').load()


import sys


if len(sys.argv) < 4 or len(sys.argv) > 5:
    print('Usage: python mirage_img.py <option(GRAY or COLORED)> <inner_image_path> <cover_image_path> <output_file_prefix(optional)>')
    sys.exit(1)
option = sys.argv[1].upper()
inner_path = sys.argv[2]
cover_path = sys.argv[3]
if len(sys.argv) > 4:
    output_path = sys.argv[4]
else:
    output_path = 'output'

if option == 'GRAY':
    Mirage_Image_Gray(inner_path, cover_path).merge().save(output_path + '.jpg', 'JPEG', quality = JPEG_QUALITY, subsampling = JPEG_SUBSAMPLING)
elif option == 'COLORED':
    Mirage_Image_Colored(inner_path, cover_path).merge().save(output_path + '.jpg', 'JPEG', quality = JPEG_QUALITY, subsampling = JPEG_SUBSAMPLING)
else:
    print('Invalid option')
    sys.exit(1)

print('Output saved as', output_path + '.jpg')
