from tkinter import *

def paint(event):
    x, y = event.x, event.y
    if selected_stamp.get():
        canvas.create_text(x, y, text=selected_stamp.get(), font=("Arial", brush_size.get() * 10))
    else:
        x1, y1 = (x - brush_size.get() // 2), (y - brush_size.get() // 2)
        x2, y2 = (x + brush_size.get() // 2), (y + brush_size.get() // 2)
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
window = Tk()
# ALL CLEAR 기능 추가
"""
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
"""
def clear_paint():
    canvas.delete("all")

def set_stamp(char):
    selected_stamp.set(char)
button_delete = Button(window, text="All Clear", command=clear_paint)
button_delete.pack()

canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True)

# 브러쉬 사이즈 조절 기능 추가
'''
brush_size.set     : 기본값
size.pack           : 툴바
Scale	         : brush_size를 결정짓는 변수
'''
brush_size = Scale(window, from_=1, to=20, orient=HORIZONTAL, label="Size")
brush_size.set(5)
brush_size.pack()

# STEAP 기능 추가
'''
set_stamp(char)     : 스탬프 문자 설정
selected_stamp      : 현재 선택된 스탬프 문자를 저장

paint 함수에서 stamp를 가지고 있다면 텍스트를 생성
'''
selected_stamp = StringVar()

stamp_frame = Frame(window)
stamp_frame.pack()

for char in "A B C D F + -".split():
    Button(stamp_frame, text=char, command=lambda ch=char: set_stamp(ch)).pack(side=LEFT)

# 브러쉬 모드로 전환하는 버튼
Button(stamp_frame, text="Brush", command=lambda: set_stamp("")).pack(side=LEFT)



canvas.bind("<B1-Motion>", paint)

window.mainloop()
