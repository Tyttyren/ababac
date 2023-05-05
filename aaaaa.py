import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import detect as de

class Application:
    def __init__(self, master, back=None, func="file", de=None):
        self.master = master
        self.master.title(func)

        self.video_player = None  # video_player 属性用于存储 VideoPlayer 对象
        self.master.geometry('1000x800')
        self.back = back
        self.de = de
        self.photo = None
        self.setup_widgets()

    def setup_widgets(self):
           # 创建文件按钮
        self.file_btn = tk.Button(self.master, text="choose image", command=self.select_file)
        self.file_btn.grid(row=0, column=0, sticky='w')

        # 创建回退按钮
        self.back_btn = tk.Button(self.master, text='<', command=self.back if self.back!=None else self.on_back_btn_clicked)
        self.back_btn.grid(row=1, column=0, sticky='w')

        # 创建画布用于展示视频/图片
        self.canvas = tk.Canvas(self.master, bg='white')
        self.canvas.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.master.grid_columnconfigure(1, weight=1, minsize=self.master.winfo_width() * 0.6)
        self.master.grid_rowconfigure(0, weight=1, minsize=self.master.winfo_height() * 0.8)

        # 将文件按钮放在下面
        self.file_btn.grid(row=2, column=1, sticky='w')

    def select_file(self):
        filetypes = [("Image files", "*.jpg;*.png"), ("Video files", "*.mp4")]

        file_path = filedialog.askopenfilename(title="choose file", filetypes=filetypes)

        if not file_path:
            return

        if file_path.lower().endswith(".jpg") or file_path.lower().endswith(".png"):
            self.show_image(file_path)
        elif file_path.lower().endswith(".mp4"):
            self.play_video(file_path)

    def show_image(self, file_path):
        if self.video_player:
            self.video_player.stop()
            self.video_player = None

        image = Image.open(file_path)
        w, h = image.size
        resize_factor = min(1, self.master.winfo_width() * 0.6 / w, self.master.winfo_height() * 0.6 / h)
        w = int(w * resize_factor)
        h = int(h * resize_factor)

        image = image.resize((w, h))
        image = self.de.rec(image)
        self.photo = ImageTk.PhotoImage(image=image)
        self.canvas.config(width=w, height=h)
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

    def play_video(self, file_path):
        if self.video_player:
            self.video_player.stop()

        self.video_player = VideoPlayer(file_path, self.canvas, self.de)
        self.video_player.play()

    def on_back_btn_clicked(self):
        messagebox.showinfo("tip", "back")


class VideoPlayer:
    def __init__(self, file_path, canvas, de):
        self.cap = cv2.VideoCapture(file_path)
        self.canvas = canvas
        self.stop_playing = False
        self.de = de

    def play(self):
        while not self.stop_playing:
            success, frame = self.cap.read()
            if not success:
                break
    
            b, g, r = cv2.split(frame)
            frame = cv2.merge((r, g, b))
            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im)
    
            # 计算缩放因子
            w_video, h_video = pil_im.size
            w_canvas, h_canvas = self.canvas.winfo_width(), self.canvas.winfo_height()
            factor_w = w_canvas / w_video
            factor_h = h_canvas / h_video
            factor = min(factor_w, factor_h)
    
            # 按比例缩小图片
            w_new, h_new = int(w_video*factor), int(h_video*factor)
            pil_im = pil_im.resize((w_new, h_new))
            photo = ImageTk.PhotoImage(image=self.rec(pil_im))
            self.canvas.create_image(w_canvas//2, h_canvas//2, image=photo)
    
            self.canvas.update()
    
    def rec(self,img):
        return self.de.rec(img)

    def stop(self):
        self.stop_playing = True


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()