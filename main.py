"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()

#도형회전기능 추가

def rotate_shapes():
    angle = math.radians(45)  # 45도 회전
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    objects = canvas.find_all()
    for obj in objects:
        coords = canvas.coords(obj)
        new_coords = []
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i + 1]
            # 원점 기준 회전
            new_x = center_x + (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle)
            new_y = center_y + (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle)
            new_coords.extend([new_x, new_y])
        canvas.coords(obj, *new_coords)


# 도형크기조절(1.5배 증가) 기능 추가
import tkinter as tk
import math

def resize_shapes(scale=1.5):
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    objects = canvas.find_all()
    for obj in objects:
        coords = canvas.coords(obj)
        new_coords = []
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i + 1]
            # 원점 기준 크기 조절
            new_x = center_x + (x - center_x) * scale
            new_y = center_y + (y - center_y) * scale
            new_coords.extend([new_x, new_y])
        canvas.coords(obj, *new_coords)

def initialize_paint_app():
    root = tk.Tk()
    root.title("그림판")
    root.geometry("800x600")
    return root

def create_canvas(root):
    canvas = tk.Canvas(root, bg="white", width=800, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)
    return canvas

def create_sample_shapes(canvas):
    canvas.create_rectangle(100, 100, 300, 200, outline="black", fill="red", tags="movable")
    canvas.create_oval(400, 100, 500, 200, outline="black", fill="blue", tags="movable")

def run_paint_app():
    global canvas
    root = initialize_paint_app()
    canvas = create_canvas(root)
    create_sample_shapes(canvas)
    
    # 버튼으로 크기 조절 기능 실행
    resize_button = tk.Button(root, text="크기 조절", command=resize_shapes)
    resize_button.pack()
    
    root.mainloop()

if __name__ == "__main__":
    run_paint_app()


# 색상추출 기능
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        show_image(image)

def show_image(image):
    # 이미지 크기 조정
    image.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo  # 이미지가 garbage-collected 되는 것을 방지하기 위해 저장
    return image

def extract_color(event):
    x, y = event.x, event.y
    rgb_color = current_image.getpixel((x, y))
    hex_color = '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])
    color_label.config(text=f"Color: {hex_color}")

root = tk.Tk()
root.title("Color Extractor")

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

color_label = tk.Label(root, text="Color: ")
color_label.pack()

current_image = None  # 현재 이미지를 저장할 변수

canvas.bind("<Button-1>", extract_color)

root.mainloop()


# 도형색상 그라데이션 채우기 기능
import tkinter as tk
import math

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.selected_object = None
        self.create_sample_shapes()

        # 그라데이션 버튼 추가
        gradient_button = tk.Button(root, text="그라데이션 채우기", command=self.apply_gradient_fill)
        gradient_button.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.select_shape)

    def create_sample_shapes(self):
        self.canvas.create_rectangle(100, 100, 300, 200, outline="black", fill="red", tags="movable")
        self.canvas.create_oval(400, 100, 500, 200, outline="black", fill="blue", tags="movable")

    def select_shape(self, event):
        # 클릭한 위치의 도형 선택
        x, y = event.x, event.y
        self.selected_object = self.canvas.find_overlapping(x, y, x, y)
        if self.selected_object:
            self.selected_object = self.selected_object[0]
            print(f"Selected object ID: {self.selected_object}")

    def apply_gradient_fill(self):
        if self.selected_object:
            coords = self.canvas.coords(self.selected_object)
            item_type = self.canvas.type(self.selected_object)
            self.canvas.delete(self.selected_object)  # 기존 도형 삭제
            self.gradient_fill(coords, item_type)

    def gradient_fill(self, coords, item_type):
        # 도형의 영역 계산
        min_x = min(coords[::2])
        max_x = max(coords[::2])
        min_y = min(coords[1::2])
        max_y = max(coords[1::2])

        # 그라데이션 색상 범위 설정
        start_color = (255, 0, 0)  # 빨간색
        end_color = (0, 0, 255)  # 파란색

        # 그라데이션 단계 수
        steps = 20
        color_step = tuple((end_color[i] - start_color[i]) / steps for i in range(3))

        if item_type == "rectangle":
            for i in range(steps):
                current_color = tuple(int(start_color[j] + color_step[j] * i) for j in range(3))
                hex_color = f'#{current_color[0]:02x}{current_color[1]:02x}{current_color[2]:02x}'

                # 그라데이션 영역 계산
                x1 = min_x + (max_x - min_x) * i / steps
                x2 = min_x + (max_x - min_x) * (i + 1) / steps
                self.canvas.create_rectangle(x1, min_y, x2, max_y, outline="", fill=hex_color)
        elif item_type == "oval":
            for i in range(steps):
                current_color = tuple(int(start_color[j] + color_step[j] * i) for j in range(3))
                hex_color = f'#{current_color[0]:02x}{current_color[1]:02x}{current_color[2]:02x}'

                # 그라데이션 영역 계산
                y1 = min_y + (max_y - min_y) * i / steps
                y2 = min_y + (max_y - min_y) * (i + 1) / steps
                self.canvas.create_oval(min_x, y1, max_x, y2, outline="", fill=hex_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()


# r,g,b키를 눌러 도형 색상 변경하는 기능
import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.selected_object = None
        self.create_sample_shapes()

        self.canvas.bind("<Button-1>", self.select_shape)
        self.root.bind("<Key>", self.change_color)

    def create_sample_shapes(self):
        self.canvas.create_rectangle(100, 100, 300, 200, outline="black", fill="red", tags="movable")
        self.canvas.create_oval(400, 100, 500, 200, outline="black", fill="blue", tags="movable")

    def select_shape(self, event):
        # 클릭한 위치의 도형 선택
        x, y = event.x, event.y
        self.selected_object = self.canvas.find_closest(x, y)[0]
        print(f"Selected object ID: {self.selected_object}")

    def change_color(self, event):
        if self.selected_object:
            color = ""
            if event.char == 'r':
                color = "red"
            elif event.char == 'g':
                color = "green"
            elif event.char == 'b':
                color = "blue"
            if color:
                self.canvas.itemconfig(self.selected_object, fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()


# 숫자 키를 이용하여 브러쉬 굵기 변경 기능
import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.brush_size = 1  # 브러쉬 기본 굵기
        self.selected_color = "black"

        self.root.bind_all("<KeyPress>", self.adjust_brush_size)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

    def adjust_brush_size(self, event):
        try:
            size = int(event.char)
            if size > 0:  # 숫자 키를 누르면 브러쉬 굵기 변경
                self.brush_size = size
                print(f"Brush size set to {self.brush_size}")
        except ValueError:
            print(f"Invalid key: {event.char}")

    def start_drawing(self, event):
        self.canvas.create_oval(event.x, event.y, event.x, event.y, outline="", fill=self.selected_color, width=self.brush_size)

    def draw(self, event):
        self.canvas.create_line(event.x, event.y, event.x, event.y, fill=self.selected_color, width=self.brush_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()


# 팔레트에 브러쉬 색상 저장 기능
import tkinter as tk
from tkinter.colorchooser import askcolor

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.brush_size = 1
        self.selected_color = "black"
        self.favorite_colors = []

        # UI 요소 추가
        self.color_button = tk.Button(root, text="색상 선택", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.save_color_button = tk.Button(root, text="현재 색상 저장", command=self.save_color)
        self.save_color_button.pack(side=tk.LEFT)

        self.color_palette = tk.Frame(root)
        self.color_palette.pack(side=tk.LEFT)

        self.root.bind("<KeyPress>", self.adjust_brush_size)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

        # 초기 마우스 좌표 설정
        self.previous_x = None
        self.previous_y = None

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.selected_color = color

    def save_color(self):
        if self.selected_color not in self.favorite_colors:
            self.favorite_colors.append(self.selected_color)
            self.update_color_palette()

    def update_color_palette(self):
        for widget in self.color_palette.winfo_children():
            widget.destroy()

        for color in self.favorite_colors:
            color_button = tk.Button(self.color_palette, bg=color, width=2, command=lambda col=color: self.set_color(col))
            color_button.pack(side=tk.LEFT)

    def set_color(self, color):
        self.selected_color = color

    def adjust_brush_size(self, event):
        try:
            size = int(event.char)
            if size > 0:
                self.brush_size = size
                print(f"Brush size set to {self.brush_size}")
        except ValueError:
            pass  # 숫자가 아닌 키 입력은 무시

    def start_drawing(self, event):
        self.previous_x, self.previous_y = event.x, event.y

    def draw(self, event):
        if self.previous_x is not None and self.previous_y is not None:
            self.canvas.create_line(self.previous_x, self.previous_y, event.x, event.y, fill=self.selected_color, width=self.brush_size)
        self.previous_x, self.previous_y = event.x, event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()


# 이미지 모자이크 블러 처리 기능
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageFilter

class MosaicBlurApp:
    def __init__(self, root):
        self.root = root
        self.root.title("모자이크 블러 앱")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.tk_image = None
        self.image_on_canvas = None
        self.selection_start = None
        self.selection_rect = None

        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.apply_mosaic_blur)

        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="이미지 열기", command=self.open_image)
        file_menu.add_command(label="저장", command=self.save_image)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            try:
                self.image = Image.open(file_path).convert("RGBA")
                self.display_image()
            except Exception as e:
                messagebox.showerror("Error", f"이미지를 여는데 실패했습니다: {e}")

    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        if self.image_on_canvas:
            self.canvas.delete(self.image_on_canvas)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def start_selection(self, event):
        if self.image:
            self.selection_start = (event.x, event.y)
            if self.selection_rect:
                self.canvas.delete(self.selection_rect)
            self.selection_rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", dash=(2, 2))

    def update_selection(self, event):
        if self.selection_start:
            self.canvas.coords(self.selection_rect, self.selection_start[0], self.selection_start[1], event.x, event.y)

    def apply_mosaic_blur(self, event):
        if self.selection_start and self.image:
            x0, y0 = self.selection_start
            x1, y1 = event.x, event.y

            # Ensure coordinates are within image bounds
            x0 = max(0, min(x0, self.image.width))
            x1 = max(0, min(x1, self.image.width))
            y0 = max(0, min(y0, self.image.height))
            y1 = max(0, min(y1, self.image.height))

            if x0 > x1:
                x0, x1 = x1, x0
            if y0 > y1:
                y0, y1 = y1, y0

            # Ensure the selected region is not too small
            if x0 != x1 and y0 != y1:
                bbox = (x0, y0, x1, y1)
                region = self.image.crop(bbox)

                # Apply mosaic blur
                small = region.resize((10, 10), resample=Image.NEAREST)
                mosaic = small.resize(region.size, Image.NEAREST)
                self.image.paste(mosaic, bbox)
                self.display_image()

            if self.selection_rect:
                self.canvas.delete(self.selection_rect)
            self.selection_start = None

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                try:
                    self.image.save(file_path)
                    print(f"이미지를 저장했습니다: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"이미지를 저장하는데 실패했습니다: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MosaicBlurApp(root)
    root.mainloop()
