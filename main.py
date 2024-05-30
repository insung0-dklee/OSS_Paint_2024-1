from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
window.mainloop()

from PIL import Image

# 이미지 확대 및 축소 함수
def resize_image(input_image_path, output_image_path, scale_factor):
    # 이미지 열기
    with Image.open(input_image_path) as image:
        # 원본 이미지의 크기를 가져옴
        width, height = image.size
        # 새로운 크기를 계산
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        # 이미지를 새로운 크기로 조정
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        # 조정된 이미지를 저장
        resized_image.save(output_image_path)
        print(f"Image resized and saved as '{output_image_path}', {new_width}x{new_height}.")

# 사용 예
input_path = "path/to/your/input/image.jpg" # 입력 이미지 경로
output_path = "path/to/your/output/image_resized.jpg" # 출력 이미지 경로
scale = 1.5 # 확대(>1) 또는 축소(<1)를 위한 스케일 인자

resize_image(input_path, output_path, scale)