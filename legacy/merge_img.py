from PIL import Image
import sys


def load_inner_image(image_path, max_size = 1200):
    '''
    加载里图, 限制最大尺寸, 进行缩放
    :param image_path: 图片路径
    :param max_size: 最大尺寸
    :return: 图片对象
    '''
    img = Image.open(image_path).convert('RGBA')
    # 限制最大尺寸，进行缩放
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    return img


def load_cover_image(image_path, target_size):
    '''
    加载表图, 根据里图尺寸裁剪并缩放
    :param image_path: 图片路径
    :param target_size: 目标尺寸
    :return: 图片对象
    '''
    img = Image.open(image_path).convert('RGBA')
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
    # 转换为灰度图
    return resized_img.convert('L')


def merge(inner_img, cover_img, div_rate = 6, hiding_rate = 2):
    '''
    生成隐写图
    :param inner_img: 里图对象
    :param cover_img: 表图对象
    :param div_rate: 分离率, 即里图占据色阶1/div_rate区间, 越大隐写效果越明显
    :param hiding_rate: 隐藏率, 即表图中每hiding_rate个像素隐藏一个里图像素, 越大隐写效果越明显
    :return output_img: 隐写图对象
    '''
    pixels_inner = inner_img.load()
    pixels_cover = cover_img.load()
    output_img = Image.new('RGBA', inner_img.size)
    pixels_output = output_img.load()
    for i in range(inner_img.size[0]):
        for j in range(inner_img.size[1]):
            # 表里图交替隐藏
            # 里图像素值向0偏移
            if (i + j) % hiding_rate == 0:
                r, g, b, a = pixels_inner[i, j]
                r, g, b = r // div_rate, g // div_rate, b // div_rate
                pixels_output[i, j] = (r, g, b, a)
            # 表图像素值向255偏移
            else:
                grey = pixels_cover[i, j] * (div_rate - 1) // div_rate + 255 // div_rate
                pixels_output[i, j] = (grey, grey, grey, 255)
    return output_img


if len(sys.argv) < 3:
    print('Usage: python merge_img.py <inner_image_path> <cover_image_path>')
    sys.exit(1)
inner_path = sys.argv[1]
cover_path = sys.argv[2]
inner = load_inner_image(inner_path)
cover = load_cover_image(cover_path, inner.size)
merge(inner, cover, 8).convert('RGB').save('output.jpg', 'JPEG', quality = 95)