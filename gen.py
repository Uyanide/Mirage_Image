from mirage_img import Mirage_Image_Colored
from mirage_img import Mirage_Image_Gray
from argparse import ArgumentParser

# 默认参数
# merge
LIMIT_INNER = 32
LIMIT_COVER = 64
HIDING_RATE = 2
# 输出图像尺寸
MAX_SIZE = 1200
# 输出图像保存
JPEG_QUALITY = 95
JPEG_SUBSAMPLING = '4:4:4'

# 创建命令行参数解析器
parser = ArgumentParser(description = 'Generate mirage image')

# 位置参数
parser.add_argument('option', choices=['gray', 'colored'], help = 'select gray or colored cover image')
parser.add_argument('inner_image_path', help = 'inner image path')
parser.add_argument('cover_image_path', help = 'cover image path')
parser.add_argument('output_file_prefix', nargs = '?', default = 'output', help = 'output file prefix')

# 可选参数
parser.add_argument('--max_size', '-s', type = int, default = MAX_SIZE, help = 'max size of inner image')
parser.add_argument('--limit_inner', '-i', type = int, default = LIMIT_INNER, help = 'limit of inner image')
parser.add_argument('--limit_cover', '-c', type = int, default = LIMIT_COVER, help = 'limit of cover image')
parser.add_argument('--hiding_rate', '-r', type = int, default = HIDING_RATE, help = 'hiding rate')

args = parser.parse_args()

option = args.option
inner_path = args.inner_image_path
cover_path = args.cover_image_path
output_path = args.output_file_prefix
MAX_SIZE = args.max_size
LIMIT_INNER = args.limit_inner
LIMIT_COVER = args.limit_cover
HIDING_RATE = args.hiding_rate

if option == 'gray':
    Mirage_Image_Gray(inner_path, cover_path, MAX_SIZE).merge(LIMIT_INNER, LIMIT_COVER, HIDING_RATE).save(output_path + '.jpg', 'JPEG', quality = JPEG_QUALITY, subsampling = JPEG_SUBSAMPLING)
elif option == 'colored':
    Mirage_Image_Colored(inner_path, cover_path, MAX_SIZE).merge(LIMIT_INNER, LIMIT_COVER, HIDING_RATE).save(output_path + '.jpg', 'JPEG', quality = JPEG_QUALITY, subsampling = JPEG_SUBSAMPLING)

print('Output saved as', output_path + '.jpg')
