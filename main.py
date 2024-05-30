"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

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