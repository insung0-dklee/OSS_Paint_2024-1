from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

        
window = Tk()
window.geometry("640x400+100+100")
#윈도우 창의 (너비)x(높이)+(초기 화면 위치의 x좌표)+(초기 화면 위치의 Y좌표)로
#초기 윈도우 창의 크기와 위치를 설정
window.resizable(True,True)
#윈도우 창의 창 크기 조절여부를 (상하,좌우) 모두 True로 하여 윈도우 창의 크기를
#조절할 수 있도록 함
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
window.mainloop()
