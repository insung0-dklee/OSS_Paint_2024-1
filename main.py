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

import os
import subprocess

def open_recent_file_with_paint():
    # Windows 최근 문서 폴더 경로 (Windows 10 기준, 버전에 따라 다를 수 있음)
    recent_folder = os.path.join(os.environ['USERPROFILE'], 'AppData\\Roaming\\Microsoft\\Windows\\Recent')
    
    # 최근 폴더에서 가장 최근에 사용된 파일 찾기
    recent_files = [os.path.join(recent_folder, f) for f in os.listdir(recent_folder)]
    recent_files = [f for f in recent_files if os.path.isfile(f)]
    recent_files.sort(key=os.path.getmtime, reverse=True)  # 수정 시간 기준으로 정렬
    
    if recent_files:
        # 가장 최근 파일을 그림판으로 열기
        latest_file = recent_files[0]
        # 실제 파일 경로를 얻기 위해 바로 가기를 해석
        target_file = subprocess.check_output(['powershell', '-Command', f'(Get-Item -Path "{latest_file}").Target']).decode().strip()
        subprocess.run(['mspaint', target_file], check=True)
    else:
        print("최근 문서를 찾을 수 없습니다.")

if __name__ == '__main__':
    open_recent_file_with_paint()
