from tkinter import *
from PIL import Image

def paint(event):
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def clear_paint():
    canvas.delete("all")

def resize_image(input_image_path, output_image_path, scale_factor):
    with Image.open(input_image_path) as image:
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        resized_image.save(output_image_path)
        print(f"Image resized and saved as '{output_image_path}', {new_width}x{new_height}.")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()

# 이미지 조정 및 저장 예
# input_path = "path/to/your/input/image.jpg" # 입력 이미지 경로
# output_path = "path/to/your/output/image_resized.jpg" # 출력 이미지 경로
# scale = 1.5 # 확대(>1) 또는 축소(<1)를 위한 스케일 인자
# resize_image(input_path, output_path, scale)
