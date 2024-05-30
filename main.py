from tkinter import *
from tkinter.colorchooser import askcolor #색상을 선택하기 위한 대화상자를 사용하기위해 askcolor함수를 불러옴

def paint(event):
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def change_bg_color():
    color = askcolor()[1]  # 사용자가 선택한 색상을 얻어옴.
    if color: #사용자가 색상을 선택하는 대화상자에서 '취소'를 누르지 않은 경우에는
        canvas.config(bg=color) #config:Tkinter위젯의 속성 변경, bg: 위젯의 배경 color: color변수에 저장된 색으로 변경

window = Tk()
canvas = Canvas(window, bg="white")
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button = Button(window, text="배경색 변경", command=change_bg_color) #button: 생성된 버튼 저장할 변수 이름, Button: Tkinter에서 버튼 생성하는 클래스, window: 버튼 배치할 Tkinter창, text="배경색 변경": 버튼에 표시될 텍스트, command=change_bg_color: 버튼 클릭시 실행될 함수 저장
button.pack() #버튼을 Tkinter에서 위젯을 화면에 배치하는 메서드

window.mainloop()
