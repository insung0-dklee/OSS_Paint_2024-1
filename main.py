"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

class LayerdCanvas : 캔버스의 레이어 기능을 추가하며, 기존 기능을 묶음.
add_layer : 새로운 캔버스를 추가하는 기능
delete_layer : 현재 캔버스를 삭제하는 기능
select_layer : add_layer와 delete_layer에서 사용하는 함수. 특정 레이어만이 화면에 표시되도록 하는 기능

"""

from tkinter import *


class LayeredCanvas:

    def __init__(self, master):
        self.layers = []
        self.master = master
        self.frame = Frame(master)
        self.frame.pack()

        self.canvas = Canvas(self.frame, bg='white')
        self.canvas.pack()

        # 레이어 추가 버튼
        self.add_layer_button = Button(self.master, text="Add Layer", command=self.add_layer)
        self.add_layer_button.pack()

        # 레이어 삭제 버튼
        self.delete_layer_button = Button(self.master, text="Delete Layer", command=self.delete_layer)
        self.delete_layer_button.pack()

        # 현재 레이어
        self.current_layer = None

        # 초기에 레이어 생성
        self.add_layer()

    def add_layer(self):
        layer = Canvas(self.frame, bg='white', width=300, height=300)
        layer.pack()
        self.layers.append(layer)
        self.select_layer(len(self.layers) - 1)

    def delete_layer(self):
        if self.layers:
            layer_to_delete = self.layers.pop()
            layer_to_delete.destroy()
            self.select_layer(len(self.layers) - 1)

    def select_layer(self, layer_index):
        if 0 <= layer_index < len(self.layers):
            self.current_layer = self.layers[layer_index]
            for layer in self.layers:
                layer.pack_forget()
            self.current_layer.pack()

    def paint(self, event):
        if self.current_layer:
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            self.current_layer.create_oval(x1,
                                           y1,
                                           x2,
                                           y2,
                                           fill="black",
                                           outline="black")

    def clear_paint(self):
        if self.current_layer:
            self.current_layer.delete("all")


# 메인 윈도우 설정
window = Tk()
window.title("Layered Paint")

# 레이어드 캔버스 인스턴스 생성
layered_canvas = LayeredCanvas(window)

# 이벤트 바인딩
window.bind("<B1-Motion>", layered_canvas.paint)
clear_button = Button(window,
                      text="Clear Layer",
                      command=layered_canvas.clear_paint)
clear_button.pack()

window.mainloop()
