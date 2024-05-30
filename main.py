"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""
from tkinter import *

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def clear_paint():
    canvas.delete("all")

def add_text():
    text = text_entry.get()
    x = int(x_entry.get())
    y = int(y_entry.get())
    size = int(size_entry.get())
    style = ""
    if bold_var.get():
        style += "bold "
    if italic_var.get():
        style += "italic"
    canvas.create_text(x, y, text=text, fill="black", font=("Helvetica", size, style.strip()))

window = Tk()
window.title("Paint Application")

canvas = Canvas(window, bg="white", width=600, height=400)
canvas.pack()

canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="All Clear", command=clear_paint)
button_delete.pack()

# 텍스트 삽입을 위한 입력 필드와 버튼
text_entry = Entry(window)
text_entry.pack()

x_entry = Entry(window)
x_entry.pack()
x_entry.insert(0, "X 좌표")

y_entry = Entry(window)
y_entry.pack()
y_entry.insert(0, "Y 좌표")

# 글자 크기 입력 필드
size_entry = Entry(window)
size_entry.pack()
size_entry.insert(0, "12")  # 기본 글자 크기 설정

# 글자 스타일 선택을 위한 체크버튼
bold_var = BooleanVar()
italic_var = BooleanVar()
bold_check = Checkbutton(window, text="Bold", variable=bold_var)
italic_check = Checkbutton(window, text="Italic", variable=italic_var)
bold_check.pack()
italic_check.pack()

button_text = Button(window, text="Add Text", command=add_text)
button_text.pack()

window.mainloop()