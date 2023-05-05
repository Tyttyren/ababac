"""
生成电瓶车的车牌，以及图片
"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import cv2
import xml_read
import os

abs_path = os.path.abspath('./')
img_path = abs_path+'\images'
font_path = abs_path+'\fonts'

def random_select(data):
    return data[np.random.randint(len(data))]

def get_location():
    i = Image.open(img_path+'\948_0.jpg')
    # img = cv2.imread(img_path+'\948_0.jpg')
    img = np.asarray(i)
    height, width = img.shape[:2]
    collect_list = []
    size = height*width
    with open(abs_path+'/label.txt', 'r') as f:
        for i in f:
           line = i.split()
           x = float(line[1])
           y = float(line[2])
           w = float(line[3])
           h = float(line[4])

           x1 = int((x - w / 2) * width)
           y1 = int((y - h / 2) * height)
           x2 = int((x + w / 2) * width)
           y2 = int((y + h / 2) * height)
           img_w = x2 - x1
           img_h = y2 - y1
        #    计算占用比例
           char_ratio = img_w*img_h #字符占用比例
           r = (char_ratio)/size          
           
           font_size = int(img_h*img_w) #字体大小
           
           collect_list.append((x1,y1,img_w,img_h,font_size))
    return collect_list

def load_coco():
    img = cv2.imread(img_path+'/948_0.jpg')
    height, width = img.shape[:2]

def get_background(bool):
    if bool:
        return Image.open(abs_path+'/images/format.png')
    else:
        return Image.open(abs_path+'/images/format2.jpg')

numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
provinces = ["京", "津", "冀", "晋", "蒙", "辽", "吉", "黑", "沪",
             "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘",
             "粤", "桂", "琼", "渝", "川", "贵", "云", "藏", "陕",
             "甘", "青", "宁", "新"]

dict_arr = ['t1','t2','b1','b2','b3','b4','b5','b6']
class Electornic_Motor(object):
   

    def __init__(self) -> None:
        self.font_ch = abs_path+"/fonts/platech.ttf"  # 中文字体格式
        self.font_en = abs_path+'/fonts/platechar.ttf'
        self.round = abs_path+'/fonts/round.ttf'
        self.font_l = abs_path+'/fonts/CNLicense-A.otf'
        self.font_t = abs_path+'/fonts/t.ttf'
        self.font_nh = abs_path+'/fonts/nh.otf'

        self.plate = self.generate_plate()

        # self.plate = self.generate_plate()

        self.font_color1 = (173,42,37)
        self.font_color2 = (255,255,255)
        self.style = get_location() #每个字符的中心点坐标，宽高，和字符大小
    
    def gen2(self, plate=None):
        bg = get_background(False)
        path = abs_path+'/ori.xml'
        if plate != None:
            self.plate = plate
        size1,content1 = xml_read.get_xml_label(path)
        bg1 = bg
        content = content1
        color = self.font_color2
        for i,c in enumerate(self.plate):
             x,y,w,h = content[dict_arr[i]]
            
            # 计算左上角的x,y点
            # left_x = int(float(x) - float(w) / 2)
            # left_y = int(float(y) - float(h) / 2)
            #生成一张图片
             if i == 0:
                 #生成汉字
                 font = ImageFont.truetype(self.font_ch, 120)
                 draw = ImageDraw.Draw(bg1)
 
                 draw.text((x-5,y-15), c, font=font, fill=color)
                 
             elif i == 1:
                 ##生成字母
                 font = ImageFont.truetype(self.font_nh, 180)
                 draw = ImageDraw.Draw(bg1)
 
                 draw.text((x+15,y-50), c, font=font, fill=color)
             elif i>1:
                 font = ImageFont.truetype(self.font_l, 240)
                 draw = ImageDraw.Draw(bg1)
                 draw.text((x,y), c, font=font, fill=color)
        return bg1


    def generate_all(self, plate=None):
        bg1= get_background(True)
        bg_path1 = './label.xml'
        bg_path2 = './ori.xml'
        if plate != None:
            self.plate = plate

        size1,content1 = xml_read.get_xml_label(bg_path1)
        # size2,content2 = xml_read.get_xml_label(bg_path2)
        content = content1

        bg1 = bg1

        for i,c in enumerate(self.plate):
            # x,y,w,h,font_size = self.style[i]
            x,y,w,h = content[dict_arr[i]]
            
            # 计算左上角的x,y点
            # left_x = int(float(x) - float(w) / 2)
            # left_y = int(float(y) - float(h) / 2)
            #生成一张图片
            if i == 0:
                #生成汉字
                font = ImageFont.truetype(self.font_ch, 70)
                draw = ImageDraw.Draw(bg1)

                draw.text((x-5,y-15), c, font=font, fill=self.font_color1)
                
            elif i == 1:
                ##生成字母
                font = ImageFont.truetype(self.font_nh, 100)
                draw = ImageDraw.Draw(bg1)

                draw.text((x+15,y-30), c, font=font, fill=self.font_color1)
            elif i>1:
                font = ImageFont.truetype(self.font_l, 110)
                draw = ImageDraw.Draw(bg1)
                draw.text((x,y), c, font=font, fill=self.font_color1)
        return bg1       



    def generate_plate(self):
        _provinces = random_select(provinces)
        _provinces += random_select(alphabet)

        for i in range(6):
            _provinces += random_select(numerals)
        return _provinces

if __name__=="__main__":
   e = Electornic_Motor()
   out = e.generate_all("川A6678A3")
   out.show()