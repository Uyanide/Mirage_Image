# 利用色阶分离和像素交错实现新世代幻影坦克

## 导入库
Pillow

## 模块列表
| 文件名 | 实现功能 | 包含类 |
|-------|-------|-------|
| mirage_img.py |  加载表里图，合成一张隐写图，可选择表图是否保留色彩 | Mirage_Image_Gray, Mirage_Image_Colored |

## 脚本列表
| 文件名 | 实现功能 | 输出文件 |
|-------|-------|-------|
| gen.py | 将表里图合成一张隐写图，并可指定部分参数 | output.jpg (默认) |

### 脚本功能介绍：
1. usage：
```
python gen.py {gray,colored} inner_image_path cover_image_path [output_file_prefix] ...
```
2. positional arguments:

| | |
|-------|-------|
| {gray,colored} | 选择表图是否保留色彩 |
| inner_image_path | 里图路径 |
| cover_image_path | 表图路径 |
  output_file_prefix(可选) | 输出文件名前缀，可指定路径 |

3. options:

| | | | 默认值 |
|-------|-------|-------|-------|
| --help | -h  | 显示帮助信息 | - |
| --max_size VALUE | -s VALUE | 设置输出图像最大尺寸 | 1200 |
| --limit_inner VALUE | -i VALUE | 里图色阶区间端点 | 32 |
| --limit_cover VALUE | -c VALUE | 表图色阶区间端点 | 64 |
| --hiding_rate VALUE | -r VALUE | 每VALUE个像素隐藏一个里图像素 | 2 |
<small>(VALUE均为正整数)</small>

3. 使用说明
    1. 如果limit_inner参数不大于limit_cover，里图色阶区间限制为 [0, limit_inner]，表图色阶区间限制为 [limit_cover, 255]。
    2. 如果limit_inner参数大于limit_cover，则相反，里图色阶区间限制为 [limit_inner, 255]，表图色阶区间限制为 [0, limit_cover]。
    3. 不需要预先处理图像大小，程序会根据里图尺寸自动裁剪缩放表图以保证完整覆盖。


## 过往脚本
| 文件名 | 实现功能 | 使用说明 | 输出文件 |
|-------|-------|-------|-------|
| legacy/merge_img.py | 将表里图合成一张隐写图，表图不保留色彩 | python merge_img.py <里图路径> <表图路径> | output.jpg |
| legacy/set_transparency.py | 将灰度图片中像素间隔设置为透明 | python set_transparency.py <图片路径> | output.png |
| legacy/convert_png.py | 将图片转为png | python convert_png.py <原图路径> | 原图名.png |

## 说明
详情见 [百度贴吧 - 开个贴细说新式高科技坦克](https://tieba.baidu.com/p/9093709508)

## 简陋的显形小工具
[光棱坦克显形](https://uyanide.github.io/Mirage_Decode/)