from PIL import Image

class Mirage_Image_Colored:
    def load_inner_image(self, image_path, max_size):
        '''
        加载里图, 限制最大尺寸, 进行缩放
        :param image_path: 图片路径
        :param max_size: 最大尺寸
        :return: 图片对象
        '''
        img = Image.open(image_path).convert('RGB')
        # 限制最大尺寸，进行缩放
        img.thumbnail((max_size, max_size), Image.LANCZOS)
        self.inner_img = img

    def load_cover_image(self, image_path, target_size):
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
        self.cover_img = resized_img

    def _get_pixels(self):
        '''
        获取表里图像素访问对象
        :return: 表里图像素访问对象 (均为RGB模式)
        '''
        return self.inner_img.load(), self.cover_img.load()

    def merge(self, limit_inner, limit_cover, hiding_rate):
        '''
        生成隐写图
        :param limit_inner: 里图色阶限制
        :param limit_cover: 表图色阶限制
        :param hiding_rate: 隐藏率, 即表图中每hiding_rate个像素隐藏一个里图像素, 越大隐写效果越明显
        :return output_img: 隐写图对象

        正向隐写(limit_inner <= limit_cover): 即里图向0偏移, 表图向255偏移
        反向隐写(limit_inner > limit_cover): 即里图向255偏移, 表图向0偏移
        '''
        pixels_inner, pixels_cover = self._get_pixels()
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

    def __init__(self, inner_path, cover_path, max_size, limit_inner, limit_cover, hiding_rate):
        '''
        构造函数, 直接加载里图和表图, 生成隐写图
        :param inner_path: 里图路径
        :param cover_path: 表图路径
        :param max_size: 最大尺寸
        '''
        self.load_inner_image(inner_path, max_size)
        self.load_cover_image(cover_path, self.inner_img.size)
        self.result = self.merge(limit_inner, limit_cover, hiding_rate)

    def save(self, output_path, format, quality, subsampling):
        '''
        保存隐写图
        :param output_path: 输出路径
        :param format: 输出格式
        :param quality: 输出质量
        :param subsampling: 输出子采样
        '''
        self.result.save(output_path, format, quality = quality, subsampling = subsampling)

class Mirage_Image_Gray(Mirage_Image_Colored):
    def _get_pixels(self):
        '''
        获取表里图像素访问对象
        :return: 表里图像素访问对象 (表图为RGB模式的灰度图)
        '''
        return self.inner_img.load(), self.cover_img.convert('L').convert('RGB').load()
