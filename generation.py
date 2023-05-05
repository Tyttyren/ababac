import cv2
import numpy as np
from PIL import Image
from ggg import generate_plate_number_funcs as gf
import ggg
from license_generation.ele_char import random_select as rs

def approve(img):
    mean = 0  # 均值
    var = 0.5  # 方差
    sigma = var**0.5
    gaussian = np.random.normal(mean, sigma, img.shape)
    gaussian = gaussian.reshape(img.shape).astype('uint8')
    noisy_img = cv2.add(img, gaussian)
    return noisy_img



def c(img):
    rows, cols = img.shape[:2]

# 设定旋转角度和缩放比例
    degree = 30  # 旋转角度
    scale = 1.0  # 缩放比例
    
    # 构建旋转矩阵
    M = cv2.getRotationMatrix2D((cols/2, rows/2), degree, scale)
    
    # 进行旋转变换
    rotated = cv2.warpAffine(img, M, (cols, rows))
    return rotated

def small(img):
    scale_ratio = 0.5

# 计算变换后的图像大小（等比例缩放）
    new_size = tuple([int(x * scale_ratio) for x in img.shape[:2]])
    
    # 进行缩放变换
    resized = cv2.resize(img, (new_size[1], new_size[0]))
    return resized

def type_detect(plate):
    if '警' in plate:
        return 'white'
    elif '学' in plate:
        return 'yellow'
    elif '挂' in plate:
        return ''

def a_plate():
    num = rs([a for a in len(gf)])
    fun = gf(num)
    plate = fun()
    



if __name__=="__main__":
    im = cv2.imread('./111.jpg')
    out = small(im)
    Image.fromarray(out).show()