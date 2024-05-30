"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def paint(event):
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def clear_paint():
    canvas.delete("all")
"""
그림을 저장할 수 있는 기능 구현
캔버스 이미지 캡쳐하기: tkinter.Canvas.postscript() 메서드를 사용하여 캔버스의 내용을 PostScript 형식으로 캡처
이미지 파일로 저장하기: 캡처한 PostScript 이미지를 PIL.Image 모듈을 사용하여 PNG 또는 JPEG 파일로 저장
저장 대화상자 표시하기: tkinter.filedialog.asksaveasfilename() 함수를 사용하여 사용자가 파일 이름과 저장 경로를 선택할 수 있는 대화상자를 표시

"""
def save_drawing():
    # 캔버스의 내용을 PostScript 형식으로 캡처하여 "drawing.eps" 파일에 저장. colormode="color"를 설정하여 컬러 이미지로 저장.
    canvas.postscript(file="drawing.eps", colormode="color")
    
    img = Image.open("drawing.eps")
    img.save("drawing.png", "PNG")
    
    # defaultextension=".png"를 설정하여 기본적으로 PNG 파일 형식으로 저장.
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        img.save(file_path, "PNG")
        print(f"그림이 '{file_path}'에 저장되었습니다.")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

save_button = Button(window, text="Save Drawing", command=save_drawing)
save_button.pack()

window.mainloop()

