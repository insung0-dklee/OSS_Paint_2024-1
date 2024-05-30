
def zoom(canvas, scale_factor) :
    scale = 1.0
    if scale_factor > 0:
          scale *= 1.1
    elif scale_factor < 0 :
          scale /= 1.1
    canvas_scale_x = canvas.winfo_width() / 2
    canvas_scale_y = canvas.winfo_height() / 2

    canvas.scale("all", canvas_scale_x, canvas_scale_y, scale, scale)

    """
    확대 및 축소 함수
    @Zoom Param
    canvas : canvas를 가르킴
    scale_factor : 확대일 경우 1을 ,축소일 경우 - 1을 인수로 받음

    @fun
    enlargement event : 기존 scale * 1.1
    reduction evnet : 기존 scale / 1.1
    canvas_scale_x : Get the width of the canvas and divide by 2
    canvas_scale_y : Get the height of the canvas and divide by 2
    canvas.scale() : Change scale size using x and y coordinates
    
    @Return
    None
    """
