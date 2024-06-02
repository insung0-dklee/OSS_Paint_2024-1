from tkinter import *
import time
from tkinter.colorchooser import askcolor
from tkinter import filedialog, PhotoImage, messagebox, simpledialog
import math
import random
import os

# 초기 설정 값들
global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1, canvas
brush_size = 1  # 초기 브러시 크기
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
brush_color = "black"  # 기본 색상은 검은색으로 설정
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
x1, y1 = None, None

# 멀티 레이어 기능 추가
layers = {}
current_layer = None

def add_layer():
    global current_layer
    layer_name = simpledialog.askstring("Input", "레이어 이름을 입력하세요:")
    if layer_name:
        new_canvas = Canvas(window, bg="white")
        new_canvas.pack(fill="both", expand=True)
        new_canvas.lower()  # 새 캔버스를 배경 레이어로 만들기 위해 낮춤
        layers[layer_name] = new_canvas
        current_layer = new_canvas
        switch_to_layer(layer_name)

def remove_layer():
    global current_layer
    layer_name = simpledialog.askstring("Input", "제거할 레이어 이름을 입력하세요:")
    if layer_name in layers:
        layers[layer_name].destroy()
        del layers[layer_name]
        current_layer = None if not layers else list(layers.values())[-1]
        if current_layer:
            current_layer.lift()

def switch_to_layer(layer_name):
    global current_layer
    if layer_name in layers:
        current_layer = layers[layer_name]
        for layer in layers.values():
            layer.lower()
        current_layer.lift()

def setup_layer_buttons():
    button_add_layer = Button(button_frame, text="레이어 추가", command=add_layer)
    button_add_layer.pack(side=LEFT)
    button_add_layer.bind("<Enter>", on_enter)
    button_add_layer.bind("<Leave>", on_leave)

    button_remove_layer = Button(button_frame, text="레이어 제거", command=remove_layer)
    button_remove_layer.pack(side=LEFT)
    button_remove_layer.bind("<Enter>", on_enter)
    button_remove_layer.bind("<Leave>", on_leave)

    button_switch_layer = Button(button_frame, text="레이어 전환", command=switch_layer)
    button_switch_layer.pack(side=LEFT)
    button_switch_layer.bind("<Enter>", on_enter)
    button_switch_layer.bind("<Leave>", on_leave)

def switch_layer():
    layer_name = simpledialog.askstring("Input", "전환할 레이어 이름을 입력하세요:")
    if layer_name in layers:
        switch_to_layer(layer_name)

# 페인팅 함수들을 현재 레이어에 맞게 업데이트
def paint_start(event): 
    global x1, y1, current_stroke
    if current_layer:
        x1, y1 = event.x, event.y
        current_stroke = []

def paint_stroke(event): 
    global x1, y1, current_stroke
    if current_layer:
        x2, y2 = event.x, event.y
        current_layer.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
        current_stroke.append((x1, y1, x2, y2))
        x1, y1 = x2, y2

def paint_end(event): 
    global current_stroke
    if current_layer:
        strokes.append(list(current_stroke))
        current_stroke.clear()

def close_program():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

def show_info_window():
    messagebox.showinfo("Info", "OSS_Paint_2024\n 그림판 v1.0.0")

is_dark_mode = False

def toggle_dark_mode():
    global is_dark_mode
    if is_dark_mode:
        apply_light_mode()
    else:
        apply_dark_mode()
    is_dark_mode = not is_dark_mode

def apply_light_mode():
    window.config(bg="sky blue")
    if current_layer:
        current_layer.config(bg="white")
    button_frame.config(bg="sky blue")
    for widget in button_frame.winfo_children():
        widget.config(bg="light grey", fg="black")
    timer_label.config(bg="sky blue", fg="black")

def apply_dark_mode():
    window.config(bg="grey20")
    if current_layer:
        current_layer.config(bg="grey30")
    button_frame.config(bg="grey20")
    for widget in button_frame.winfo_children():
        widget.config(bg="grey40", fg="white")
    timer_label.config(bg="grey20", fg="white")

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        editor.open_image(file_path)

def on_enter(event):
    event.widget.config(bg="light blue")

def on_leave(event):
    event.widget.config(bg="SystemButtonFace")

def upload_image():
    path = filedialog.askopenfilename()
    if path:
        if not path.lower().endswith('.png'):
            messagebox.showerror("Invalid File", "PNG 파일만 업로드할 수 있습니다.")
            return
        image = PhotoImage(file=path)
        current_layer.create_image(0, 0, anchor=NW, image=image)
        current_layer.image = image

timer = Timer()

def update_timer():
    elapsed_time = timer.get_elapsed_time()
    timer_label.config(text=f"Time: {int(elapsed_time)} s")
    window.after(1000, update_timer)

def stop_timer():
    timer.stop()

def reset_timer():
    timer.reset()
    if not timer.running:
        timer.start()

def start_stop():
    if not timer.running:
        timer.start()

def paint_airbrush(event):
    for _ in range(dot_count.get()):
        radius = random.randint(1, brush_size)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, dot_distance.get())
        x = event.x + distance * math.cos(angle)
        y = event.y + distance * math.sin(angle)
        current_layer.create_oval(x - radius, y - radius, x + radius, y + radius, fill=brush_color, outline=brush_color)

def increase_dot_count():
    dot_count.set(dot_count.get() + 1)

def decrease_dot_count():
    dot_count.set(max(dot_count.get() - 1, 1))

def increase_dot_distance():
    dot_distance.set(dot_distance.get() + 1)

def decrease_dot_distance():
    dot_distance.set(max(dot_distance.get() - 1, 0))

def bind_shortcuts():
    window.bind("<c>", lambda event: clear_paint(current_layer))
    window.bind("<Control-s>", save_canvas)
    window.bind("<Control-z>", erase_last_stroke)

def set_paint_mode_airbrush():
    current_layer.bind("<B1-Motion>", paint_airbrush)

def set_paint_mode_normal():
    current_layer.bind("<Button-1>", paint_start)
    current_layer.bind("<B1-Motion>", paint_stroke)
    current_layer.bind("<ButtonRelease-1>", paint_end)

def set_paint_mode_pressure():
    current_layer.bind("<Button-1>", start_paint_pressure)
    current_layer.bind("<B1-Motion>", paint_pressure)

def start_paint_pressure(event):
    global start_time
    start_time = time.time()

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = ( event.x - radius ), ( event.y - radius )
    x2, y2 = ( event.x + radius ), ( event.y + radius )
    current_layer.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def dotted_paint(event):
    global last_x, last_y
    spacing = 10 + brush_size
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            current_layer.create_oval(event.x-brush_size / 2, event.y-brush_size / 2, event.x+brush_size / 2, event.y+brush_size / 2, fill=brush_color, outline=brush_color)
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y
        current_layer.create_oval(last_x - 1, last_y - 1, last_x + 1, last_y + 1, fill=brush_color, outline=brush_color)

def set_brush_mode(mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        current_layer.bind("<B1-Motion>", paint_stroke)
    elif brush_mode == "dotted":
        current_layer.bind("<B1-Motion>", dotted_paint)
    elif brush_mode == "double_line":
        current_layer.bind("<B1-Motion>", double_line_paint)
        current_layer.bind("<Button-1>", start_new_line)

def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

def zoom(event):
    scale = 1.0
    if event.delta > 0:
        scale = 1.1
    elif event.delta < 0:
        scale = 0.9
    current_layer.scale("all", event.x, event.y, scale, scale)

def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

def add_text(event, text_box):
    text = text_box.get()
    current_layer.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))

def bind_shortcuts_window(window):
    window.bind("<Alt-Return>", toggle_fullscreen)
    window.bind("<Command-Return>", toggle_fullscreen)

def toggle_fullscreen(event=None):
    global window
    window.attributes("-fullscreen", not window.attributes("-fullscreen"))

def flip_horizontal():
    objects = current_layer.find_all()
    current_layer.update()
    canvas_width = current_layer.winfo_width()
    for obj in objects:
        coords = current_layer.coords(obj)
        for i in range(len(coords)):
            if i % 2 == 0:
                coords[i] = canvas_width - coords[i]
        current_layer.coords(obj, *coords)

def erase(event):
    bg_color = current_layer.cget("bg")
    x1, y1 = ( event.x-3 ), ( event.y-3 )
    x2, y2 = ( event.x+3 ), ( event.y+3 )
    current_layer.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color():
    bg_color = askcolor()
    current_layer.config(bg=bg_color[1])

def change_brush_color(event=None):
    global brush_color
    selected_color = askcolor()[1]
    if selected_color:
        brush_color = selected_color

def set_brush_color(color):
    global brush_color
    brush_color = color

def set_custom_color(r_entry, g_entry, b_entry, palette_frame):
    try:
        r = int(r_entry.get())
        g = int(g_entry.get())
        b = int(b_entry.get())
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            color = f'#{r:02x}{g:02x}{b:02x}'
            set_brush_color(color)
            button = Button(palette_frame, bg=color, width=2, height=1, command=lambda c=color: set_brush_color(c))
            button.pack(side=LEFT, padx=2, pady=2)
        else:
            print("RGB 값은 0에서 255 사이여야 합니다.")
    except ValueError:
        print("유효한 RGB 값을 입력하세요.")

def setup_palette(window):
    palette_window = Toplevel(window)
    palette_window.title("팔레트 설정")
    palette_frame = Frame(palette_window)
    palette_frame.pack(pady=10)
    colors = [
        'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'white', 'pink', 'brown', 'grey'
    ]
    for color in colors:
        button = Button(palette_frame, bg=color, width=2, height=1, command=lambda c=color: set_brush_color(c))
        button.pack(side=LEFT, padx=2, pady=2)
    custom_color_frame = Frame(palette_window)
    custom_color_frame.pack(pady=10)
    Label(custom_color_frame, text="R:").grid(row=0, column=0)
    r_entry = Entry(custom_color_frame, width=3)
    r_entry.grid(row=0, column=1)
    Label(custom_color_frame, text="G:").grid(row=0, column=2)
    g_entry = Entry(custom_color_frame, width=3)
    g_entry.grid(row=0, column=3)
    Label(custom_color_frame, text="B:").grid(row=0, column=4)
    b_entry = Entry(custom_color_frame, width=3)
    b_entry.grid(row=0, column=5)
    Button(custom_color_frame, text="Set Color", command=lambda: set_custom_color(r_entry, g_entry, b_entry, palette_frame)).grid(row=1, columnspan=6, pady=10)

def save_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        current_layer.postscript(file=file_path)

def reset_brush():
    global brush_size, brush_color
    brush_size = 1
    brush_color = "black"
    change_brush_size(brush_size)
    current_layer.bind("<B1-Motion>", paint_stroke)

def setup_reset_brush_button(window):
    button_reset = Button(window, text="Reset Brush", command=reset_brush)
    button_reset.pack(side=LEFT)
    button_reset.bind("<Enter>", on_enter)
    button_reset.bind("<Leave>", on_leave)

def flood_fill(event):
    fill_color = askcolor()[1]
    x, y = event.x, event.y
    target = current_layer.find_closest(x, y)
    if target:
        current_layer.itemconfig(target, fill=fill_color)

def draw_actor(event, actor_name):
    x, y = event.x, event.y
    current_layer.create_oval(x - 15, y - 15, x + 15, y + 15, fill="white", outline="black")
    current_layer.create_line(x, y + 15, x, y + 40)
    current_layer.create_line(x, y + 20, x - 10, y + 30)
    current_layer.create_line(x, y + 20, x + 10, y + 30)
    current_layer.create_line(x, y + 40, x - 10, y + 50)
    current_layer.create_line(x, y + 40, x + 10, y + 50)
    current_layer.create_text(x, y + 60, text=actor_name, anchor="center")
    current_layer.unbind("<Button-1>")
    current_layer.unbind("<B1-Motion>")
    current_layer.unbind("<ButtonRelease-1>")

def draw_use_case(event, use_case_name):
    x, y = event.x, event.y
    current_layer.create_oval(x - 50, y - 25, x + 50, y + 25, fill="white", outline="black")
    current_layer.create_text(x, y, text=use_case_name, anchor="center")
    current_layer.unbind("<Button-1>")
    current_layer.unbind("<B1-Motion>")
    current_layer.unbind("<ButtonRelease-1>")

def draw_relationship_start(event):
    global x1, y1, preview_line
    x1, y1 = event.x, event.y
    preview_line = None
    current_layer.bind("<B1-Motion>", draw_relationship_preview)

def draw_relationship_preview(event):
    global x1, y1, preview_line
    x2, y2 = event.x, event.y
    if preview_line:
        current_layer.delete(preview_line)
    preview_line = current_layer.create_line(x1, y1, x2, y2, dash=(4, 2))

def draw_relationship_end(event, relationship_type):
    global x1, y1, preview_line
    x2, y2 = event.x, event.y
    if preview_line:
        current_layer.delete(preview_line)
    if relationship_type in ["include", "extend"]:
        current_layer.create_line(x1, y1, x2, y2, arrow=LAST, dash=(4, 2))
    else:
        current_layer.create_line(x1, y1, x2, y2)
    if relationship_type == "include":
        current_layer.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="<<include>>", anchor="center")
    elif relationship_type == "extend":
        current_layer.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="<<extend>>", anchor="center")
    current_layer.unbind("<Button-1>")
    current_layer.unbind("<B1-Motion>")
    current_layer.unbind("<ButtonRelease-1>")

def add_actor():
    actor_name = simpledialog.askstring("Input", "액터의 이름을 입력하세요:")
    if actor_name:
        current_layer.bind("<Button-1>", lambda event: draw_actor(event, actor_name))

def add_use_case():
    use_case_name = simpledialog.askstring("Input", "유스케이스의 이름을 입력하세요:")
    if use_case_name:
        current_layer.bind("<Button-1>", lambda event: draw_use_case(event, use_case_name))

def add_relationship():
    relationship_type = simpledialog.askstring("Input", "관계의 유형을 입력하세요 (include/extend/line):")
    if relationship_type in ["include", "extend", "line"]:
        current_layer.bind("<Button-1>", draw_relationship_start)
        current_layer.bind("<ButtonRelease-1>", lambda event: draw_relationship_end(event, relationship_type))
    else:
        messagebox.showerror("Error", "잘못된 입력입니다. include, extend, line 중에 입력하세요.")

def choose_use_case_element(event=None):
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Actor", command=add_actor)
    popup.add_command(label="Use Case", command=add_use_case)
    popup.add_command(label="Relationship", command=add_relationship)
    if event:
        popup.post(event.x_root, event.y_root)
    else:
        popup.post(window.winfo_pointerx(), window.winfo_pointery())

def setup_paint_app(window):
    global brush_size, brush_color, button_frame

    brush_size = 1
    brush_color = "black"

    global canvas
    canvas = Canvas(window, bg="white")
    canvas.pack(fill="both", expand=True)

    last_x, last_y = None, None
    brush_mode = "solid"

    button_frame = Frame(window,bg="sky blue")
    button_frame.pack(fill=X)

    button_toggle_mode = Button(window, text="Toggle Dark Mode", command=toggle_dark_mode)
    button_toggle_mode.pack(side=LEFT)

    button_marker = Button(button_frame, text="Marker Mode", command=set_paint_mode_marker)
    button_marker.pack(side=LEFT)
    button_marker.bind("<Enter>", on_enter)
    button_marker.bind("<Leave>", on_leave)

    button_use_case = Button(window, text="Use Case Diagram", command=choose_use_case_element)
    button_use_case.pack(side=LEFT)

    button_stop_timer = Button(button_frame, text="Stop Timer", command=stop_timer)
    button_stop_timer.pack(side=RIGHT)

    button_reset_timer = Button(button_frame, text="Reset Timer", command=reset_timer)
    button_reset_timer.pack(side=RIGHT)

    start_button = Button(button_frame, text="Start", command=start_stop)
    start_button.pack(side = RIGHT)

    global spray_brush
    spray_brush = SprayBrush(current_layer, brush_color)
    button_spray = Button(window, text="spray", command=lambda: current_layer.bind("<B1-Motion>", spray_brush.spray_paint))
    button_spray.pack(side=LEFT)

    button_erase_last_stroke = Button(button_frame, text="Erase Last Stroke", command=erase_last_stroke)
    button_erase_last_stroke.pack(side=LEFT)

    button_redo_last_stroke = Button(button_frame, text="Rewrite Last Stroke", command=rewrite_last_stroke)
    button_redo_last_stroke.pack(side=LEFT)

    button_clear = Button(button_frame, text="All Clear", command=lambda: clear_paint(current_layer))
    button_clear.pack(side=LEFT)
    button_clear.bind("<Enter>", on_enter)
    button_clear.bind("<Leave>", on_leave)

    brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack(side=LEFT)

    button_solid = Button(button_frame, text="Solid Brush", command=lambda: set_brush_mode("solid"))
    button_solid.pack()
    button_solid.bind("<Enter>", on_enter)
    button_solid.bind("<Leave>", on_leave)

    button_dotted = Button(button_frame, text="Dotted Brush", command=lambda: set_brush_mode("dotted"))
    button_dotted.pack()
    button_dotted.bind("<Enter>", on_enter)
    button_dotted.bind("<Leave>", on_leave)

    button_double_line = Button(button_frame, text="Double line Brush", command=lambda: set_brush_mode("double_line"))
    button_double_line.pack()
    button_double_line.bind("<Enter>", on_enter)
    button_double_line.bind("<Leave>", on_leave)

    setup_reset_brush_button(window)

    button_paint = Button(window, text="normal", command=set_paint_mode_normal)
    button_paint.pack(side=RIGHT)
    button_paint.bind("<Enter>", on_enter)
    button_paint.bind("<Leave>", on_leave)

    button_paint = Button(window, text="pressure", command=set_paint_mode_pressure)
    button_paint.pack(side=RIGHT)
    button_paint.bind("<Enter>", on_enter)
    button_paint.bind("<Leave>", on_leave)

    text_box = Entry(window)
    text_box.pack(side=LEFT)
    current_layer.bind("<Button-3>", lambda event: add_text(event, text_box))
    window.bind("<F11>", toggle_fullscreen)

    button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)
    button_flip.pack(side=LEFT)
    button_flip.bind("<Enter>", on_enter)
    button_flip.bind("<Leave>", on_leave)

    current_layer.bind("<B3-Motion>", erase)

    button_choose_shape = Button(window, text="shape", command=choose_shape)
    button_choose_shape.bind("<Button-1>", choose_shape)
    button_choose_shape.pack(side=LEFT)

    current_layer.bind("<Enter>", change_cursor)
    current_layer.bind("<Leave>", default_cursor)

    current_layer.bind("<Button-3>", show_coordinates)
    current_layer.bind("<ButtonRelease-3>", hide_coordinates)

    current_layer.bind("<MouseWheel>", zoom)

    bind_shortcuts()

    dot_count = IntVar()
    dot_count.set(10)

    dot_distance = IntVar()
    dot_distance.set(10)

    frame_distance = Frame(window)
    frame_distance.pack(side=RIGHT)

    frame_count = Frame(window)
    frame_count.pack(side=RIGHT)

    Button(frame_distance, text="+", command=increase_dot_distance).pack(side=RIGHT)
    Label(frame_distance, text="Distance").pack(side=RIGHT)
    Label(frame_distance, textvariable=dot_distance).pack(side=RIGHT)
    Button(frame_distance, text="-", command=decrease_dot_distance).pack(side=RIGHT)

    Button(frame_count, text="+", command=increase_dot_count).pack(side=RIGHT)
    Label(frame_count, text="Count").pack(side=RIGHT)
    Label(frame_count, textvariable=dot_count).pack(side=RIGHT)
    Button(frame_count, text="-", command=decrease_dot_count).pack(side=RIGHT)

    button_paint = Button(window, text="airbrush", command=set_paint_mode_airbrush)
    button_paint.pack(side=RIGHT)

    set_paint_mode_normal()

    menu_bar = Menu(window)
    window.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    color_menu = Menu(menu_bar, tearoff=0)
    tool_menu = Menu(menu_bar, tearoff=0)
    help_menu = Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label="File", menu=file_menu)
    menu_bar.add_cascade(label="Color", menu=color_menu)
    menu_bar.add_cascade(label="Tools", menu=tool_menu)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    file_menu.add_command(label="Open New Window", command=create_new_window)
    file_menu.add_command(label="Add Image", command=upload_image)
    file_menu.add_command(label="Save", command=save_canvas)
    file_menu.add_command(label="Exit", command=close_program)

    color_menu.add_command(label="Set Palette", command=lambda: setup_palette(window))
    color_menu.add_command(label="Change Background Color", command=change_bg_color)
    color_menu.add_command(label="Change Brush Color", command=change_brush_color)

    tool_menu.add_command(label="Toggle FullScreen", command=toggle_fullscreen)
    tool_menu.add_command(label="Toggle Ruler", command=toggle_ruler)
    tool_menu.add_command(label="Toggle Grid", command=lambda: toggle_grid(current_layer))
    tool_menu.add_command(label="Grid Setting", command=open_grid_dialog)

    help_menu.add_command(label="Info", command=show_info_window)

def create_new_window():
    new_window = Toplevel(window)
    new_window.title("새 그림판")
    new_window.geometry("800x600+200+200")
    new_window.configure(bg="sky blue")
    setup_paint_app(new_window)

def change_cursor(event):
    current_layer.config(cursor="pencil")

def default_cursor(event):
    current_layer.config(cursor="")

def show_coordinates(event):
    current_layer.delete("coord_text")
    width = current_layer.winfo_width()
    height = current_layer.winfo_height()
    x_percent = (event.x / width) * 100
    y_percent = (event.y / height) * 100
    coord_text = f"<{x_percent:.1f}% / {100-y_percent:.1f}%>"
    current_layer.create_text(10, 10, text=coord_text, anchor="nw", tags="coord_text")

def hide_coordinates(event):
    current_layer.delete("coord_text")

def select_shape_color():
    global shape_outline_color, shape_fill_color
    shape_outline_color = askcolor()[1]
    shape_fill_color = askcolor()[1]

def create_rectangle(event=None):
    select_shape_color()
    current_layer.bind("<Button-1>", start_rectangle)

def create_triangle(event=None):
    select_shape_color()
    current_layer.bind("<Button-1>", start_triangle)

def create_circle(event=None):
    select_shape_color()
    current_layer.bind("<Button-1>", start_circle)

def start_rectangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    current_layer.bind("<B1-Motion>", draw_rectangle)
    current_layer.bind("<ButtonRelease-1>", finish_rectangle)

def draw_rectangle(event):
    global start_x, start_y, current_shape
    current_layer.delete("temp_shape")
    current_shape = current_layer.create_rectangle(start_x, start_y, event.x, event.y, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_rectangle(event):
    global current_shape
    current_layer.unbind("<B1-Motion>")
    current_layer.unbind("<ButtonRelease-1>")
    if current_shape:
        current_layer.itemconfig(current_shape, tags="")

def start_triangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    current_layer.bind("<B1-Motion>", draw_triangle)
    current_layer.bind("<ButtonRelease-1>", finish_triangle)

def draw_triangle(event):
    global start_x, start_y, current_shape
    current_layer.delete("temp_shape")
    x2, y2 = event.x, event.y
    side_length = math.sqrt((x2 - start_x) ** 2 + (y2 - start_y) ** 2)
    angle = math.radians(60)
    x3 = start_x + side_length * math.cos(angle)
    y3 = start_y + side_length * math.sin(angle)
    angle += math.radians(60)
    x4 = start_x + side_length * math.cos(angle)
    y4 = start_y + side_length * math.sin(angle)
    current_shape = current_layer.create_polygon(start_x, start_y, x2, y2, x3, y3, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_triangle(event):
    global current_shape
    current_layer.unbind("<B1-Motion>")
    current_layer.unbind("<ButtonRelease-1>")
    if current_shape:
        current_layer.itemconfig(current_shape, tags="")

def start_circle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    current_layer.bind("<B1-Motion>", draw_circle)
    current_layer.bind("<ButtonRelease-1>", finish_circle)

def draw_circle(event):
    global start_x, start_y, current_shape
    current_layer.delete("temp_shape")
    r = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
    current_shape = current_layer.create_oval(start_x - r, start_y - r, start_x + r, start_y + r, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_circle(event):
    global current_shape
    current_layer.unbind("<B1-Motion>")
    current_layer.unbind("<ButtonRelease-1>")
    if current_shape:
        current_layer.itemconfig(current_shape, tags="")

def create_star(event=None):
    select_shape_color()
    current_layer.bind("<Button-1>", start_star)

def start_star(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    current_layer.bind("<B1-Motion>", draw_star)
    current_layer.bind("<ButtonRelease-1>", finish_star)

def draw_star(event):
    global start_x, start_y, current_shape
    current_layer.delete("temp_shape")
    outer_radius = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
    inner_radius = outer_radius / 2.5
    points = []
    for i in range(5):
        angle_outer = math.radians(i * 72 - 90)
        angle_inner = math.radians(i * 72 + 36 - 90)
        x_outer = start_x + outer_radius * math.cos(angle_outer)
        y_outer = start_y + outer_radius * math.sin(angle_outer)
        x_inner = start_x + inner_radius * math.cos(angle_inner)
        y_inner = start_y + inner_radius * math.sin(angle_inner)
        points.append(x_outer)
        points.append(y_outer)
        points.append(x_inner)
        points.append(y_inner)
    current_shape = current_layer.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_star(event):
    global current_shape
    current_layer.unbind("<B1-Motion>")
    current_layer.unbind("<ButtonRelease-1>")
    if current_shape:
        current_layer.itemconfig(current_shape, tags="")

def choose_shape(event):
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Rectangle", command=lambda: create_rectangle(event))
    popup.add_command(label="Triangle", command=lambda: create_triangle(event))
    popup.add_command(label="Circle", command=lambda: create_circle(event))
    popup.add_command(label="Star", command=lambda: create_star(event))
    popup.post(event.x_root, event.y_root)

def paint_marker(event):
    radius = brush_size
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    current_layer.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def set_paint_mode_marker():
    current_layer.bind("<B1-Motion>", paint_marker)
    current_layer.bind("<Button-1>", paint_marker)

strokes = []
current_stroke = []
redo_strokes = []

def paint_start(event):
    global x1, y1, current_stroke
    if current_layer:
        x1, y1 = event.x, event.y
        current_stroke = []

def paint_stroke(event):
    global x1, y1, current_stroke
    if current_layer:
        x2, y2 = event.x, event.y
        current_layer.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
        current_stroke.append((x1, y1, x2, y2))
        x1, y1 = x2, y2

def paint_end(event):
    global current_stroke
    if current_layer:
        strokes.append(list(current_stroke))
        current_stroke.clear()

def erase_last_stroke(event=None):
    if strokes:
        last_stroke = strokes.pop()
        redo_strokes.append(last_stroke)
        for line in last_stroke:
            current_layer.create_line(*line, fill="white", width=brush_size)

def rewrite_last_stroke():
    if redo_strokes:
        last_redo_stroke = redo_strokes.pop()
        strokes.append(last_redo_stroke)
        for line in last_redo_stroke:
            current_layer.create_line(*line, fill=brush_color, width=brush_size)

def start_new_line(event):
    global last_x, last_y
    last_x, last_y = None, None

def double_line_paint(event):
    global last_x, last_y
    spacing = brush_size
    if last_x is not None and last_y is not None:
        angle = math.atan2(event.y - last_y, event.x - last_x)
        dx = math.cos(angle + math.pi / 2) * spacing
        dy = math.sin(angle + math.pi / 2) * spacing
        current_layer.create_line(last_x - dx, last_y - dy, event.x - dx, event.y - dy, width=brush_size, fill=brush_color)
        current_layer.create_line(last_x + dx, last_y + dy, event.x + dx, event.y + dy, width=brush_size, fill=brush_color)
        last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

def draw_tile_pattern(tile_size=50):
    canvas_width = current_layer.winfo_width()
    canvas_height = current_layer.winfo_height()
    for x in range(0, canvas_width, tile_size):
        for y in range(0, canvas_height, tile_size):
            current_layer.create_rectangle(x, y, x + tile_size, y + tile_size, outline="black")

def draw_wave_pattern(wave_length=50, amplitude=20):
    canvas_width = current_layer.winfo_width()
    canvas_height = current_layer.winfo_height()
    for y in range(0, canvas_height, wave_length):
        for x in range(0, canvas_width, wave_length):
            current_layer.create_arc(x, y, x + wave_length, y + wave_length, start=0, extent=180, style=ARC)
            current_layer.create_arc(x, y + amplitude, x + wave_length, y + wave_length + amplitude, start=180, extent=180, style=ARC)

def draw_diagonal_pattern(line_spacing=50):
    canvas_width = current_layer.winfo_width()
    canvas_height = current_layer.winfo_height()
    for x in range(0, canvas_width, line_spacing):
        current_layer.create_line(x, 0, 0, x, fill="black")
        current_layer.create_line(canvas_width - x, canvas_height, canvas_width, canvas_height - x, fill="black")
    for y in range(0, canvas_height, line_spacing):
        current_layer.create_line(0, y, y, 0, fill="black")
        current_layer.create_line(canvas_width, canvas_height - y, canvas_width - y, canvas_height, fill="black")

def draw_grid(step):
    current_layer.delete("grid_line")
    width = current_layer.winfo_width()
    height = current_layer.winfo_height()
    for x in range(0, width, step):
        current_layer.create_line(x, 0, x, height, fill="lightgray", tags="grid_line")
    for y in range(0, height, step):
        current_layer.create_line(0, y, width, y, fill="lightgray", tags="grid_line")

def toggle_grid():
    if current_layer.find_withtag("grid_line"):
        current_layer.delete("grid_line")
    else:
        draw_grid(50)

def change_grid_spacing(value):
    draw_grid(value)

class GridDialog:
    def __init__(self, window):
        self.top = Toplevel(window)
        self.top.title("Grid scale")
        Label(self.top, text="그리드 간격:").pack()
        self.gridscale_slider = Scale(self.top, from_=50, to=100, resolution=5, orient=HORIZONTAL)
        self.gridscale_slider.set(50)
        self.gridscale_slider.pack()
        self.ok_button = Button(self.top, text="OK", command=self.ok)
        self.ok_button.pack()
        self.cancel_button = Button(self.top, text="Cancel", command=self.cancel)
        self.cancel_button.pack()
        self.result = None

    def ok(self):
        self.result = self.gridscale_slider.get()
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

def open_grid_dialog():
    dialog = GridDialog(window)
    window.wait_window(dialog.top)
    grid_spacing = dialog.result
    if grid_spacing is not None:
        global grid_spacing_global
        grid_spacing_global = grid_spacing
        window.bind("<Configure>", on_window_grid)

def on_window_grid(event):
    global grid_spacing_global
    draw_grid(grid_spacing_global)

def draw_ruler():
    global ruler_lines, ruler_texts
    canvas_width = current_layer.winfo_width()
    canvas_height = current_layer.winfo_height()
    try:
        interval = int(interval_entry.get())
    except ValueError:
        interval = 10
    for x in range(0, canvas_width, interval):
        if x % (interval * 5) == 0:
            line = current_layer.create_line(x, 0, x, 15, fill="black")
            text = current_layer.create_text(x, 25, text=str(x), anchor=N)
            ruler_lines.append(line)
            ruler_texts.append(text)
        else:
            line = current_layer.create_line(x, 0, x, 10, fill="black")
            ruler_lines.append(line)
    for y in range(0, canvas_height, interval):
        if y % (interval * 5) == 0:
            line = current_layer.create_line(0, y, 15, y, fill="black")
            text = current_layer.create_text(25, y, text=str(y), anchor=W)
            ruler_lines.append(line)
            ruler_texts.append(text)
        else:
            line = current_layer.create_line(0, y, 10, y, fill="black")
            ruler_lines.append(line)

def clear_ruler():
    global ruler_lines, ruler_texts
    for item in ruler_lines + ruler_texts:
        current_layer.delete(item)
    ruler_lines.clear()
    ruler_texts.clear()

def toggle_ruler():
    global ruler_on
    if ruler_on:
        clear_ruler()
    else:
        draw_ruler()
    ruler_on = not ruler_on

def on_resize(event):
    if ruler_on:
        clear_ruler()
        draw_ruler()

def on_closing():
    if messagebox.askokcancel("Quit", "그림을 저장하시겠습니까?"):
        save_canvas()
    window.destroy()

def get_image_size(file_path):
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        return size
    else:
        print("File not found.")
        return 0

def get_canvas_size():
    temp_file = "temp_canvas.ps"
    current_layer.postscript(file=temp_file)
    size = get_image_size(temp_file)
    os.remove(temp_file)
    return size

def print_image_size(file_path):
    size = get_image_size(file_path)
    print("Image size:", size, "bytes")

def print_canvas_size():
    size = get_canvas_size()
    print("Canvas size:", size, "bytes")

def open_text_input_window():
    text_input_window = Toplevel(window)
    text_input_window.title("Text Input")
    text_input = Text(text_input_window, width=30, height=5)
    text_input.pack()
    confirm_button = Button(text_input_window, text="확인", command=lambda: add_text_to_canvas(text_input.get("1.0", "end-1c")))
    confirm_button.pack()

def add_text_to_canvas(text):
    if text.strip():
        text_item = current_layer.create_text(100, 100, text=text, fill="black", font=('Arial', 12))
        current_layer.tag_bind(text_item, "<ButtonPress-1>", start_drag)
        current_layer.tag_bind(text_item, "<B1-Motion>", drag)
        current_layer.tag_bind(text_item, "<ButtonRelease-1>", end_drag)

def start_drag(event):
    drag_data["item"] = current_layer.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def drag(event):
    if drag_data["item"]:
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        current_layer.move(drag_data["item"], dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

def end_drag(event):
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0

text_box_button = Button(window, text="TEXTBOX", command=open_text_input_window)
text_box_button.pack()

ruler_on = False
ruler_lines = []
ruler_texts = []

interval_label = Label(window, text="Ruler Interval:")
interval_label.pack()

interval_entry = Entry(window)
interval_entry.pack()
interval_entry.insert(0, "10")

current_layer.bind("<Configure>", on_resize)

bind_shortcuts_window(window)

window.protocol("WM_DELETE_WINDOW", on_closing)

timer.start()
update_timer()

window = Tk()
version = "1.0.0"
window.title(f"그림판 v{version}")
window.geometry("800x600+200+200")
window.resizable(True, True)
window.configure(bg="sky blue")
setup_paint_app(window)
editor = ImageEditor(current_layer)
setup_layer_buttons()
add_layer()
timer_label = Label(window, text="Time: 0 s")
timer_label.pack(side=RIGHT)

window.mainloop()
