import tkinter as tk
from PIL import Image, ImageTk

# 创建窗口
root = tk.Tk()
root.geometry("1000x800")

# 打开图像
image = Image.open("111.jpg")

# 如果图像高宽超过 800x600，就进行缩放
if image.size[0] > 800 or image.size[1] > 600:
    ratio = min(800 / image.size[0], 600 / image.size[1])
    new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    image = image.resize(new_size)

# 把图像转换成 tkinter 可以显示的格式
tk_image = ImageTk.PhotoImage(image)

# 创建标签，显示图像
label = tk.Label(root, image=tk_image)
label.pack(side="bottom")

label2 = tk.Label(root, text="Label")
label2.pack(side="top", padx=10, pady=10)

# 创建按钮和标签，显示在窗口顶部
button1 = tk.Button(root, text="Button 1")
button1.pack(side="top", padx=10, pady=10)

button2 = tk.Button(root, text="Button 2")
button2.pack(side="top", padx=10, pady=10)



# 运行窗口
root.mainloop()