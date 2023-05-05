import sys
from tkinter import *
from tkinter.filedialog import askopenfilename

import torch
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
from tensorflow import keras

from tool import locate_and_correct
import detect as de
from aaaaa import Application


def get_second(capture):
    if capture.isOpened():
        rate = capture.get(5)   # 帧速率
        FrameNumber = capture.get(7)  # 视频文件的帧数
        duration = FrameNumber/rate  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
        return int(rate),int(FrameNumber),int(duration)    

def has_image(canvas, item):
    image_id = canvas.itemcget(item, 'image')
    return image_id is not None

class DefaultDetect:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_detect = de.load_model('./model/best.pt', device=self.device)
        self.model_rec = de.init_model(self.device,'./model/plate_rec_color.pth', False)
    
    def rec(self,img):
        cv_img = np.asarray(img)
        dict_list = de.detect_Recognition_plate(self.model_detect, cv_img, self.device,self.model_rec, 640,False)
        ori_img = de.draw_result(cv_img,dict_list)
        return Image.fromarray(cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB))

class Window:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))  # 界面启动时的初始位置
        self.win.title("License Detection")
        self.img_src_path = None

        self.cav = Canvas(self.win, width=400, height=400, bg='white', relief='solid', borderwidth=1)
        
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # self.model_detect = de.load_model('./model/best.pt', device=self.device)
        # self.model_rec = de.init_model(self.device,'./model/rec.pth', False)
        self.dr = DefaultDetect()

        self.is_index = True

        self.index()

        # Label(self.win, text='原图:', font=('微软雅黑', 16)).place(x=0, y=0)
        # # Label(self.win, text='车牌区域:', font=('微软雅黑', 18)).place(x=600, y=125)
        # Label(self.win, text='识别结果:', font=('微软雅黑', 18)).place(x=600, y=220)
         
        # # 画布的上半边
        # can_src_pady = 0.1*wh
        # self.factor = 0.7
        # self.can_src = Canvas(self.win, width=ww*0.7, height=wh*0.7, bg='white', relief='solid', borderwidth=1)  # 原图画布
        # self.can_src.pack(pady=can_src_pady,fill=X)
        # # self.can_src.place(x=50, y=0)
        # # self.can_lic1 = Canvas(self.win, width=245, height=85, bg='white', relief='solid', borderwidth=1)  # 车牌区域1画布
        # # self.can_lic1.place(x=710, y=100)
        # self.can_pred1 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)  # 车牌识别1画布
        # # self.can_pred1.place(x=710, y=200)
        # self.can_pred1.pack(side=LEFT)
        # # self.can_pred1.grid(row=0,column=0)
        
        # self.button1 = Button(self.win, text='选择文件', width=15, height=2, command=self.load_show_img)  # 选择文件按钮
        # self.button1.pack(side=LEFT)
        # self.button2 = Button(self.win, text='识别车牌', width=15, height=2, command=self.display)  # 识别车牌按钮
        # self.button2.pack(side=LEFT)
        # self.button3 = Button(self.win, text='清空', width=15, height=2, command=self.clear)  # 清空所有按钮
        # self.button3.pack(side=LEFT)
        # self.unet = keras.models.load_model('model\\unet.h5')
        # self.cnn = keras.models.load_model('model\\cnn.h5')
        # print('正在启动中,请稍等...')
        # cnn_predict(self.cnn, [np.zeros((80, 240, 3))])
        # print("已启动,开始识别吧！")

    def load_show_img(self):
        # self.clear()
        sv = StringVar()
        sv.set(askopenfilename())
        # print(type(sv))
        self.img_src_path = Entry(self.win, state='readonly', textvariable=sv).get()  # 获取到所打开的图片
        path = self.img_src_path
        # print(self.img_src_path)
        path_appendix = os.path.basename(path).split('.')[1]
        if path_appendix == 'jpg':
            self.img(path)
        elif path_appendix == 'mp4':
            self.video(path)
    

    def video(self, video_name):
        capture=cv2.VideoCapture(video_name)
        fourcc = cv2.VideoWriter_fourcc(*'MP4V') 
        fps = capture.get(cv2.CAP_PROP_FPS)  # 帧数
        width, height = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 宽高
        out = cv2.VideoWriter('result.mp4', fourcc, fps, (width, height))  # 写入视频
        frame_count = 0
        fps_all=0
        rate,FrameNumber,duration=get_second(capture)
        if capture.isOpened():
            while True:
                t1 = cv2.getTickCount()
                frame_count+=1
                print(f"{frame_count} frame",end=" ")
                ret,img=capture.read()
                if not ret:
                    break
                self.rec(img)
                # if frame_count%rate==0:
                # img0 = copy.deepcopy(img)
                # dict_list=detect_Recognition_plate(detect_model, img, device,plate_rec_model,opt.img_size,is_color=opt.is_color)
                # ori_img=draw_result(img,dict_list)
                t2 =cv2.getTickCount()
                infer_time =(t2-t1)/cv2.getTickFrequency()
                fps=1.0/infer_time
                fps_all+=fps
                str_fps = f'fps:{fps:.4f}'
                
                # cv2.putText(ori_img,str_fps,(20,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                # cv2.imshow("haha",ori_img)
                # cv2.waitKey(1)
                # out.write(ori_img)  
    
    def index(self):
        title = Label(self.win, text='License Plate Recognition System for \n Traditional Vehicles and Electric Vehicles',
                      font=('宋体',20, 'bold italic'))
        title.pack(ipadx=40,ipady=100)

        license_rec = Button(self.win,text='Car License Recognize',height=10,width=25, command=self.car_rec)
        license_rec.pack(side=LEFT,padx=30)

        motor_rec = Button(self.win, text='MotorBike Recognize',height=10,width=25, command=self.motor_rec1)
        motor_rec.pack(side=LEFT,padx=30)
        
        # gen = Button(self.win, text='Generate Plate',height=10,width=25, command=self.gen)
        # gen.pack(side=LEFT,padx=30)

    def car_rec(self):
        self.clear()
        self.basic_info('car')
        return
    
    def motor_rec1(self):
        self.clear()
        self.basic_info("motor")
        return
    
    def back_index(self):
        self.clear()
        self.index()
    
    def gen(self):
        back = Button(self.win, text='back', height=2,width=4, command=self.back_index)
        back.pack(anchor=NW,padx=3,pady=3)

        self.canvas = Canvas(self.frame, width=300, height=300)
        self.canvas.pack(anchor=CENTER)
        self.btn = Button(self.frame, text="Generate Image", command=self.open_image)
        self.btn.pack(pady=10)



    def basic_info(self,name):
        window = self.win
        # back = Button(window, text='back', height=2,width=4, command=self.back_index)
        # back.pack(anchor=NW,padx=3,pady=3)
        # title = Label(window, text=name)
        # title.pack(ipadx=40,ipady=50)


        # button1 = Button(window, text='select image', height=5,width=10, command=self.load_show_img)
        
        # button1.pack(side=LEFT,padx=30)
        Application(window, self.back_index, name, de=self.dr)
    

    def img(self, img_path):
        img_open = Image.open(self.img_src_path)
        # if img_open.size[0] * img_open.size[1] > 240 * 80:
        #     img_open = img_open.resize((512, 512), Image.ANTIALIAS)
        # self.img_Tk = ImageTk.PhotoImage(img_open)
        self.rec(img_open)
        
    
    def rec(self, img_path):
        # item_without_img = self.cav.create_rectangle(0,0,150,150, fill='blue')
        # if not has_image(self.cav, item_without_img):
        #     self.cav.delete("all")
        # self.cav.pack(X=100,Y=100)

        img = np.asarray(img_path)
        if img.shape[-1]==4:
            img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
        dict_list = de.detect_Recognition_plate(self.model_detect, img, self.device,self.model_rec, 640,False)
        ori_img = de.draw_result(img,dict_list)
        if ori_img[:1] != (400,400):
            cv2.resize(ori_img, (400,400))
        i = Image.fromarray(ori_img)
        img1 = ImageTk.PhotoImage(i)
        # Canvas(self.win, width=ww*0.7, height=wh*0.7, bg='white', relief='solid', borderwidth=1)
        cav = Canvas(self.win, width=600, height=600, bg='white', relief='solid', borderwidth=1)
        cav.create_image(400,400, image=img1, anchor='center')
        cav.pack(anchor=S)
        return

    def clear(self):
        for i in self.win.winfo_children():
            i.destroy()

    @staticmethod
    def closeEvent():  # 关闭前清除session(),防止'NoneType' object is not callable
        keras.backend.clear_session()
        sys.exit()


if __name__ == '__main__':
    win = Tk()
    win.config(background='pink')
    screen_hight = win.winfo_screenheight()
    screen_width = win.winfo_screenwidth()
    ww = 1000  # 窗口宽设定1000
    wh = 800  # 窗口高设定600
    Window(win, ww, wh)
    win.protocol()
    win.mainloop()
