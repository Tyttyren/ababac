from PIL import Image
import math
import glob
import os

def rec(path, angle, save_path):
    img = Image.open(path)
    w,h = img.size
    img2 = img.rotate(angle, expand=True)   # 自定义旋转度数
    ## 新图像高度
    # n_h = math.sin(angle)*w+math.cos(angle)*h
    # n_w = math.cos(angle)*w+math.sin(angle)*h
    # n_h = math.fabs(n_h)
    # n_w = math.fabs(n_w)
    img2.crop(img2.getbbox())

    # img2 = img2.resize((int(n_h),int(n_w)))   # 改变图片尺寸
    img2.save(save_path)

if __name__=="__main__":
    path = 'D:/BaiduNetdiskDownload/git_plate/CCPD_CRPD_OTHER_ALL'
    save_path = 'D:/BaiduNetdiskDownload/90'
    list = glob.glob(path+'/*.jpg')
    
    for i in list:
        base = os.path.basename(i)
        rec(i, 90, save_path+'/'+base)

