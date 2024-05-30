from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
from PIL import ImageGrab
import os


def paint(event):
    x1, y1 = (event.x - brush_size.get()), (event.y - brush_size.get())
    x2, y2 = (event.x + brush_size.get()), (event.y + brush_size.get())
    canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color)


def clear_paint():
    canvas.delete("all")


def choose_color():
    color = askcolor()[1]
    if color:
        global current_color
        current_color = color


def save_paint():
    file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        # Append a number to the filename if it already exists
        base, ext = os.path.splitext(file_path)
        counter = 1
        new_file_path = file_path
        while os.path.exists(new_file_path):
            new_file_path = f"{base}_{counter}{ext}"
            counter += 1

        x = window.winfo_rootx() + canvas.winfo_x()
        y = window.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(new_file_path)


window = Tk()
window.title("그림판")

current_color = "black"

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<B1-Motion>", paint)

button_frame = Frame(window)
button_frame.pack(fill=X)

button_delete = Button(button_frame, text="All Clear", command=clear_paint)
button_delete.pack(side=LEFT, padx=5, pady=5)

color_button = Button(button_frame, text="Choose Color", command=choose_color)
color_button.pack(side=LEFT, padx=5, pady=5)

save_button = Button(button_frame, text="Save", command=save_paint)
save_button.pack(side=LEFT, padx=5, pady=5)

brush_size = IntVar(value=1)
size_slider = Scale(button_frame, from_=1, to=10, orient=HORIZONTAL, variable=brush_size, label="Brush Size")
size_slider.pack(side=LEFT, padx=5, pady=5)

window.mainloop()
