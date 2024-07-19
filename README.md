# 利用色阶分离和像素交错实现新世代幻影坦克

## 导入库
Pillow

## 模块列表
| 文件名 | 实现功能 | 包含类 |
|-------|-------|-------|
| mirage_img.py |  加载表里图，合成一张隐写图，可选择表图是否保留色彩 | Mirage_Image_Gray, Mirage_Image_Colored |

## 脚本列表
| 文件名 | 实现功能 | 使用说明 | 输出文件 |
|-------|-------|-------|-------|
| gen.py | 将表里图合成一张隐写图，并可指定部分参数 | (参照 python gen.py -h) | output.jpg (默认) |

## 过往脚本
| 文件名 | 实现功能 | 使用说明 | 输出文件 |
|-------|-------|-------|-------|
| legacy/merge_img.py | 将表里图合成一张隐写图，表图不保留色彩（早期版本） | python merge_img.py <里图路径> <表图路径> | output.jpg |
| legacy/set_transparency.py | 将灰度图片中像素间隔设置为透明 | python set_transparency.py <图片路径> | output.png |
| legacy/convert_png.py | 将图片转为png | python convert_png.py <原图路径> | 原图名.png |

## 说明
详情见 [百度贴吧 - 开个贴细说新式高科技坦克](https://tieba.baidu.com/p/9093709508)