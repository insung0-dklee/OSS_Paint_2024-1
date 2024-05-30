# 선 굵기를 조절하는 기능을 담은 파일

# 선의 굵기 초기값
line_thickness = 2

# 선 굵기를 증가시키는 함수
def increase_thickness():
    global line_thickness
    line_thickness += 1
    print(f"Current line thickness: {line_thickness}")  # 현재 선 굵기를 출력

# 선 굵기를 감소시키는 함수
def decrease_thickness():
    global line_thickness
    if line_thickness > 1:
        line_thickness -= 1
        print(f"Current line thickness: {line_thickness}")  # 현재 선 굵기를 출력
    else:
        print("Line thickness cannot be less than 1.")
