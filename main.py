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

import pyautogui
import time

def insert_text_in_paint(text):
    # 그림판 내에서 도형의 위치를 찾기 (여기서는 예시로 100, 100 위치를 사용)
    shape_position = (100, 100)
    
    # 도형 클릭
    pyautogui.click(shape_position)
    
    # 글자 삽입 모드 활성화를 위한 단축키, 그림판 버전에 따라 다를 수 있음 (여기서는 'T' 키를 사용)
    pyautogui.press('t')
    
    # 잠시 대기
    time.sleep(1)  # 필요에 따라 대기 시간 조정
    
    # 텍스트 입력
    pyautogui.typewrite(text)
    
    # 저장 또는 추가 조작을 위해 더 많은 pyautogui 함수를 여기에 추가할 수 있습니다.

if __name__ == '__main__':
    insert_text_in_paint('안녕하세요!')
