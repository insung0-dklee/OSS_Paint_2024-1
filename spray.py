import random #무작위 수를 추출하기 위해 import

class SprayBrush:
    def __init__(self, canvas, brush_color):
        self.canvas = canvas
        self.brush_color = brush_color
        self.brush_size = 10

    def set_brush_color(self, brush_color):
        self.brush_color = brush_color

    def set_brush_size(self, brush_size):
        self.brush_size = brush_size

    def spray_paint(self, event):
        radius = self.brush_size  
        dot = 50  
        for _ in range(dot):
            offset_x = random.randint(-radius, radius)
            offset_y = random.randint(-radius, radius)
            if offset_x**2 + offset_y**2 <= radius**2:
                x = event.x + offset_x
                y = event.y + offset_y
                self.canvas.create_oval(x, y, x + 1, y + 1, fill=self.brush_color, outline=self.brush_color)
"""
#class Spray Brush
  @fun()
    __init__: 생성자로 canvas와 brush_color을 인자로 받아 변수를 초기화. bruch_color은 spray에 컬러가 된다.
    spray_paint: spray 동작 구현
              radius : 스프레이의 너비
              dot : 점의 개수(반복 횟수로 사용)
              offset_x:지정한 너비 사이의 무작위 정수 값을 추출
              self.canvas.create_ova: 계산된 x와 y 좌표를 기준으로 하여 원 모양의 점을 생성한다. 
                                      이 때 색상은 매개변수로 받은 brush_color을 그대로 사용한다.
"""