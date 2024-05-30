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

#세 점을 이용하여 삼각형을 그리는 기능 추가
class TriangleDrawer:
    """
    삼각형을 그리기 위한 클래스.
    
    사용자가 클릭한 세 점을 사용하여 삼각형을 그림.
    
    Attributes:
    canvas (tkinter.Canvas): 삼각형을 그릴 캔버스.
    triangle_points (list): 사용자가 클릭한 점들을 저장할 리스트.
    """
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.triangle_points = []
    
    def add_point(self, event):    
        """
        사용자가 캔버스를 클릭할 때마다 점을 추가.
        세 점이 모두 모이면 삼각형을 그림.
        
        @param
            event: tkinter 이벤트 객체
        @return
            None
        """
        if len(self.triangle_points) < 3:
            self.triangle_points.append((event.x, event.y))
            self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="#d2b48c", outline="black")
            if len(self.triangle_points) == 3:
                self.draw_triangle(self.triangle_points)
                self.triangle_points.clear()
        
    def draw_triangle(self, points):      
        """
        주어진 세 점을 사용하여 삼각형을 그림.
        
        @param
            points: 삼각형을 그릴 세 점의 리스트        
        @return
            None
        """
        self.canvas.create_polygon(points, outline="black", fill="")
    
    def enable_triangle_mode(self):
        """
        삼각형 모드를 활성화하여 캔버스 클릭 시 add_point 메서드를 호출하도록 설정.
        
        @param
            None
        @return
            None
        """
        self.canvas.bind("<Button-1>", self.add_point)

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

triangle_drawer = TriangleDrawer(canvas)
button_draw_triangle = Button(window, text="draw triangle", command=triangle_drawer.enable_triangle_mode)
button_draw_triangle.pack()

window.mainloop()
