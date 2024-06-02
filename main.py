from tkinter import *
import time
import brush_settings
from brush_settings import change_brush_size, change_bg_color, change_brush_color, set_brush_mode, set_paint_mode_normal, set_paint_mode_pressure, paint_start, paint, dotted_paint
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import simpledialog
import math
import random
from fun_timer import Timer
from picture import ImageEditor
from spray import SprayBrush
import os
from TransformationHandler import TransformationHandler

# 초기 설정 값들
global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1, canvas
brush_size = 1
selected_shape = "oval"
brush_color = "black"
brush_mode = "solid"
current_color = "black"
eraser_mode = False
spacing = 10
last_x, last_y = None, None
x1, y1 = None, None

dynamic_brush = False
previous_time = None
previous_x, previous_y = None, None

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
    canvas.config(bg="white")
    button_frame.config(bg="sky blue")
    for widget in button_frame.winfo_children():
        widget.config(bg="light grey", fg="black")
    timer_label.config(bg="sky blue", fg="black")

def apply_dark_mode():
    window.config(bg="grey20")
    canvas.config(bg="grey30")
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
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.image = image

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

def paint_airbrush(event, canvas):
    for _ in range(dot_count.get()):
        radius = random.randint(1, brush_size)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, dot_distance.get())
        x = event.x + distance * math.cos(angle)
        y = event.y + distance * math.sin(angle)
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=brush_color, outline=brush_color)

def increase_dot_count():
    dot_count.set(dot_count.get() + 1)

def decrease_dot_count():
    dot_count.set(max(dot_count.get() - 1, 1))

def increase_dot_distance():
    dot_distance.set(dot_distance.get() + 1)

def decrease_dot_distance():
    dot_distance.set(max(dot_distance.get() - 1, 0))

def bind_shortcuts():
    window.bind("<c>", lambda event: clear_paint(canvas))
    window.bind("<Control-s>", save_canvas)
    window.bind("<Control-z>", erase_last_stroke)

def set_paint_mode_airbrush(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint_airbrush(event, canvas))

def set_paint_mode_normal(canvas, set_origin_mode=False):
    canvas.bind("<Button-1>", lambda event: paint_start(event))
    canvas.bind("<B1-Motion>", paint_stroke)
    if set_origin_mode:
        pass

def set_paint_mode_pressure(canvas):
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event, canvas))
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

def start_paint_pressure(event, canvas):
    global start_time
    start_time = time.time()

def paint_pressure(event, canvas):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def dotted_paint(event, canvas):
    global last_x, last_y
    spacing = 10 + brush_size
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x - brush_size / 2, event.y - brush_size / 2, event.x + brush_size / 2, event.y + brush_size / 2, fill=brush_color, outline=brush_color)
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y
        canvas.create_oval(last_x - 1, last_y - 1, last_x + 1, last_y + 1, fill=brush_color, outline=brush_color)

def set_brush_mode(canvas, mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", lambda event: set_paint_mode_normal(canvas))
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))
    elif brush_mode == "double_line":
        canvas.bind("<B1-Motion>", lambda event: double_line_paint(event, canvas))
        canvas.bind("<Button-1>", start_new_line)

def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)
    spray_brush.set_brush_size(brush_size)

def zoom(event):
    scale = 1.0
    if event.delta > 0:
        scale = 1.1
    elif event.delta < 0:
        scale = 0.9
    canvas.scale("all", event.x, event.y, scale, scale)

def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

def add_text(event, canvas, text_box):
    text = text_box.get()
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))

def bind_shortcuts_window(window):
    window.bind("<Alt-Return>", toggle_fullscreen)
    window.bind("<Command-Return>", toggle_fullscreen)

def toggle_fullscreen(event=None):
    global window
    window.attributes("-fullscreen", not window.attributes("-fullscreen"))

def erase(event, canvas):
    bg_color = canvas.cget("bg")
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color(canvas):
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color(event=None):
    global brush_color
    selected_color = askcolor()[1]
    if selected_color:
        brush_color = selected_color
        set_brush_color(brush_color)

def set_brush_color(color):
    global brush_color
    brush_color = color
    spray_brush.set_brush_color(brush_color)

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
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'white', 'pink', 'brown', 'grey']
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

def save_canvas(canvas):
    file_path = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path)

def reset_brush(canvas):
    global brush_size, brush_color
    brush_size = 1
    brush_color = "black"
    change_brush_size(brush_size)
    canvas.bind("<B1-Motion>", lambda event: set_paint_mode_normal(canvas))

def setup_reset_brush_button(window, canvas):
    button_reset = Button(window, text="Reset Brush", command=lambda: reset_brush(canvas))
    button_reset.pack(side=LEFT)
    button_reset.bind("<Enter>", on_enter)
    button_reset.bind("<Leave>", on_leave)

def flood_fill(event):
    fill_color = askcolor()[1]
    x, y = event.x, event.y
    target = canvas.find_closest(x, y)
    if target:
        canvas.itemconfig(target, fill=fill_color)

def draw_actor(event, actor_name):
    x, y = event.x, event.y
    canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="white", outline="black")
    canvas.create_line(x, y + 15, x, y + 40)
    canvas.create_line(x, y + 20, x - 10, y + 30)
    canvas.create_line(x, y + 20, x + 10, y + 30)
    canvas.create_line(x, y + 40, x - 10, y + 50)
    canvas.create_line(x, y + 40, x + 10, y + 50)
    canvas.create_text(x, y + 60, text=actor_name, anchor="center")
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def draw_use_case(event, use_case_name):
    x, y = event.x, event.y
    canvas.create_oval(x - 50, y - 25, x + 50, y + 25, fill="white", outline="black")
    canvas.create_text(x, y, text=use_case_name, anchor="center")
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def draw_relationship_start(event):
    global x1, y1, preview_line
    x1, y1 = event.x, event.y
    preview_line = None
    canvas.bind("<B1-Motion>", draw_relationship_preview)

def draw_relationship_preview(event):
    global x1, y1, preview_line
    x2, y2 = event.x, event.y
    if preview_line:
        canvas.delete(preview_line)
    preview_line = canvas.create_line(x1, y1, x2, y2, dash=(4, 2))

def draw_relationship_end(event, relationship_type):
    global x1, y1, preview_line
    x2, y2 = event.x, event.y
    if preview_line:
        canvas.delete(preview_line)
    if relationship_type in ["include", "extend"]:
        canvas.create_line(x1, y1, x2, y2, arrow=LAST, dash=(4, 2))
    else:
        canvas.create_line(x1, y1, x2, y2)
    if relationship_type == "include":
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="<<include>>", anchor="center")
    elif relationship_type == "extend":
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="<<extend>>", anchor="center")
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def add_actor():
    actor_name = simpledialog.askstring("Input", "액터의 이름을 입력하세요:")
    if actor_name:
        canvas.bind("<Button-1>", lambda event: draw_actor(event, actor_name))

def add_use_case():
    use_case_name = simpledialog.askstring("Input", "유스케이스의 이름을 입력하세요:")
    if use_case_name:
        canvas.bind("<Button-1>", lambda event: draw_use_case(event, use_case_name))

def add_relationship():
    relationship_type = simpledialog.askstring("Input", "관계의 유형을 입력하세요 (include/extend/line):")
    if relationship_type in ["include", "extend", "line"]:
        canvas.bind("<Button-1>", draw_relationship_start)
        canvas.bind("<ButtonRelease-1>", lambda event: draw_relationship_end(event, relationship_type))
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

def create_transformation_menu(event):
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Flip Horizontal", command=transformation_handler.flip_horizontal)
    popup.add_command(label="Flip Vertical", command=transformation_handler.flip_vertical)
    popup.add_command(label="Rotate 90 Degrees", command=transformation_handler.rotate_90)
    popup.post(event.x_root, event.y_root)

def setup_paint_app(window):
    global brush_size, brush_color, button_frame


    brush_size = 1
    brush_color = "black"

    global canvas
    canvas = Canvas(window, bg="white")
    canvas.pack(fill="both", expand=True)

    global transformation_handler
    transformation_handler = TransformationHandler(canvas)


    last_x, last_y = None, None
    brush_mode = "solid"

    button_frame = Frame(window, bg="sky blue")
    button_frame.pack(fill=X)

    button_toggle_mode = Button(window, text="Toggle Dark Mode", command=toggle_dark_mode)
    button_toggle_mode.pack(side=LEFT)

    button_flip_horizontal = Button(window, text="Flip Horizontal", command=transformation_handler.flip_horizontal)
    button_flip_horizontal.pack(side=LEFT)
    button_flip_horizontal.bind("<Enter>", on_enter)
    button_flip_horizontal.bind("<Leave>", on_leave)

    button_flip_vertical = Button(window, text="Flip Vertical", command=transformation_handler.flip_vertical)
    button_flip_vertical.pack(side=LEFT)
    button_flip_vertical.bind("<Enter>", on_enter)
    button_flip_vertical.bind("<Leave>", on_leave)

    button_rotate_90 = Button(window, text="Rotate 90 Degrees", command=transformation_handler.rotate_90)
    button_rotate_90.pack(side=LEFT)
    button_rotate_90.bind("<Enter>", on_enter)
    button_rotate_90.bind("<Leave>", on_leave)


    button_marker = Button(button_frame, text="Marker Mode", command=lambda: set_paint_mode_marker(canvas))
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
    start_button.pack(side=RIGHT)

    global spray_brush
    spray_brush = SprayBrush(canvas, brush_color)

    button_spray = Button(window, text="spray", command=lambda: canvas.bind("<B1-Motion>", spray_brush.spray_paint))
    button_spray.pack(side=LEFT)

    button_erase_last_stroke = Button(button_frame, text="Erase Last Stroke", command=erase_last_stroke)
    button_erase_last_stroke.pack(side=LEFT)

    button_redo_last_stroke = Button(button_frame, text="Rewrite Last Stroke", command=rewrite_last_stroke)
    button_redo_last_stroke.pack(side=LEFT)

    button_clear = Button(button_frame, text="All Clear", command=lambda: clear_paint(canvas))
    button_clear.pack(side=LEFT)
    button_clear.bind("<Enter>", on_enter)
    button_clear.bind("<Leave>", on_leave)

    brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack(side=LEFT)

    button_solid = Button(button_frame, text="Solid Brush", command=lambda: set_brush_mode(canvas, "solid"))
    button_solid.pack()
    button_solid.bind("<Enter>", on_enter)
    button_solid.bind("<Leave>", on_leave)

    button_dotted = Button(button_frame, text="Dotted Brush", command=lambda: set_brush_mode(canvas, "dotted"))
    button_dotted.pack()
    button_dotted.bind("<Enter>", on_enter)
    button_dotted.bind("<Leave>", on_leave)

    button_double_line = Button(button_frame, text="Double line Brush", command=lambda: set_brush_mode(canvas, "double_line"))
    button_double_line.pack()
    button_double_line.bind("<Enter>", on_enter)
    button_double_line.bind("<Leave>", on_leave)

    setup_reset_brush_button(window, canvas)

    button_paint = Button(window, text="normal", command=lambda: set_paint_mode_normal(canvas))
    button_paint.pack(side=RIGHT)
    button_paint.bind("<Enter>", on_enter)
    button_paint.bind("<Leave>", on_leave)



    text_box = Entry(window)
    text_box.pack(side=LEFT)
    canvas.bind("<Button-3>", lambda event: add_text(event, canvas, text_box))
    window.bind("<F11>", toggle_fullscreen)

    button_flip = Button(window, text="Flip Horizontal", command=lambda: transformation_handler.flip_horizontal())
    button_flip.pack(side=LEFT)
    button_flip.bind("<Enter>", on_enter)
    button_flip.bind("<Leave>", on_leave)

    canvas.bind("<B3-Motion>", lambda event: erase(event, canvas))

    button_choose_shape = Button(window, text="shape", command=choose_shape)
    button_choose_shape.bind("<Button-1>", choose_shape)
    button_choose_shape.pack(side=LEFT)

    canvas.bind("<Enter>", change_cursor)
    canvas.bind("<Leave>", default_cursor)

    canvas.bind("<Button-3>", show_coordinates)
    canvas.bind("<ButtonRelease-3>", hide_coordinates)

    canvas.bind("<MouseWheel>", zoom)

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

    button_paint = Button(window, text="airbrush", command=lambda: set_paint_mode_airbrush(canvas))
    button_paint.pack(side=RIGHT)

    canvas.bind("<Button-1>", paint_start)
    canvas.bind("<B1-Motion>", paint_stroke)
    canvas.bind("<ButtonRelease-1>", paint_end)

    set_paint_mode_normal(canvas)

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
    file_menu.add_command(label="Save", command=lambda: save_canvas(canvas))
    file_menu.add_command(label="Exit", command=close_program)

    color_menu.add_command(label="Set Palette", command=lambda: setup_palette(window))
    color_menu.add_command(label="Change Background Color", command=lambda: change_bg_color(canvas))
    color_menu.add_command(label="Change Brush Color", command=lambda: change_brush_color())

    tool_menu.add_command(label="Toggle FullScreen", command=toggle_fullscreen)
    tool_menu.add_command(label="Toggle Ruler", command=toggle_ruler)
    tool_menu.add_command(label="Toggle Grid", command=lambda: toggle_grid(canvas))
    tool_menu.add_command(label="Grid Setting", command=open_grid_dialog)

    tool_menu.add_command(label="Flip Horizontal", command=transformation_handler.flip_horizontal)
    tool_menu.add_command(label="Flip Vertical", command=transformation_handler.flip_vertical)
    tool_menu.add_command(label="Rotate 90 Degrees", command=transformation_handler.rotate_90)

    help_menu.add_command(label="Info", command=show_info_window)




def create_new_window():
    new_window = Toplevel(window)
    new_window.title("새 그림판")
    new_window.geometry("800x600+200+200")
    new_window.configure(bg="sky blue")
    setup_paint_app(new_window)

def change_cursor(event):
    canvas.config(cursor="pencil")

def default_cursor(event):
    canvas.config(cursor="")

def show_coordinates(event):
    canvas.delete("coord_text")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x_percent = (event.x / width) * 100
    y_percent = (event.y / height) * 100
    coord_text = f"<{x_percent:.1f}% / {100 - y_percent:.1f}%>"
    canvas.create_text(10, 10, text=coord_text, anchor="nw", tags="coord_text")

def hide_coordinates(event):
    canvas.delete("coord_text")

def select_shape_color():
    global shape_outline_color, shape_fill_color
    shape_outline_color = askcolor()[1]
    shape_fill_color = askcolor()[1]

def create_rectangle(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_rectangle)

def create_triangle(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_triangle)

def create_circle(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_circle)

def start_rectangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_rectangle(event))
    canvas.bind("<ButtonRelease-1>", finish_rectangle)

def draw_rectangle(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    current_shape = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")
    paint_start(event)

def finish_rectangle(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

def start_triangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", draw_triangle)
    canvas.bind("<ButtonRelease-1>", finish_triangle)

def draw_triangle(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    x2, y2 = event.x, event.y
    side_length = math.sqrt((x2 - start_x) ** 2 + (y2 - start_y) ** 2)
    angle = math.radians(60)
    x3 = start_x + side_length * math.cos(angle)
    y3 = start_y + side_length * math.sin(angle)
    angle += math.radians(60)
    x4 = start_x + side_length * math.cos(angle)
    y4 = start_y + side_length * math.sin(angle)
    current_shape = canvas.create_polygon(start_x, start_y, x2, y2, x3, y3, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_triangle(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

def start_circle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_circle(event))
    canvas.bind("<ButtonRelease-1>", finish_circle)

def draw_circle(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    r = ((start_x - event.x) ** 2 + (start_y - event.y) ** 2) ** 0.5
    current_shape = canvas.create_oval(start_x - r, start_y - r, start_x + r, start_y + r, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_circle(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

def create_star(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_star)

def start_star(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_star(event))
    canvas.bind("<ButtonRelease-1>", finish_star)

def draw_star(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    outer_radius = ((start_x - event.x) ** 2 + (start_y - event.y) ** 2) ** 0.5
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
    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_star(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

def choose_shape(event):
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Rectangle", command=lambda: create_rectangle(event))
    popup.add_command(label="Triangle", command=lambda: create_triangle(event))
    popup.add_command(label="Circle", command=lambda: create_circle(event))
    popup.add_command(label="Star", command=lambda: create_star(event))
    popup.post(event.x_root, event.y_root)

def paint_marker(event, canvas):
    radius = brush_size
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def set_paint_mode_marker(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint_marker(event, canvas))
    canvas.bind("<Button-1>", lambda event: paint_marker(event, canvas))

strokes = []
current_stroke = []
redo_strokes = []

def paint_start(event):
    global x1, y1, current_stroke
    x1, y1 = event.x, event.y
    current_stroke = []

def paint_stroke(event):
    global x1, y1, current_stroke
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    current_stroke.append((x1, y1, x2, y2))
    x1, y1 = x2, y2

def paint_end(event):
    global current_stroke
    strokes.append(list(current_stroke))
    current_stroke.clear()

def erase_last_stroke(event=None):
    if strokes:
        last_stroke = strokes.pop()
        redo_strokes.append(last_stroke)
        for line in last_stroke:
            canvas.create_line(*line, fill="white", width=brush_size)

def rewrite_last_stroke():
    if redo_strokes:
        last_redo_stroke = redo_strokes.pop()
        strokes.append(last_redo_stroke)
        for line in last_redo_stroke:
            canvas.create_line(*line, fill=brush_color, width=brush_size)

def start_new_line(event):
    global last_x, last_y
    last_x, last_y = None, None

def double_line_paint(event, canvas):
    global last_x, last_y
    spacing = brush_size
    if last_x is not None and last_y is not None:
        angle = math.atan2(event.y - last_y, event.x - last_x)
        dx = math.cos(angle + math.pi / 2) * spacing
        dy = math.sin(angle + math.pi / 2) * spacing
        canvas.create_line(last_x - dx, last_y - dy, event.x - dx, event.y - dy, width=brush_size, fill=brush_color)
        canvas.create_line(last_x + dx, last_y + dy, event.x + dx, event.y + dy, width=brush_size, fill=brush_color)
        last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

def draw_tile_pattern(canvas, tile_size=50):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for x in range(0, canvas_width, tile_size):
        for y in range(0, canvas_height, tile_size):
            canvas.create_rectangle(x, y, x + tile_size, y + tile_size, outline="black")

def draw_wave_pattern(canvas, wave_length=50, amplitude=20):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for y in range(0, canvas_height, wave_length):
        for x in range(0, canvas_width, wave_length):
            canvas.create_arc(x, y, x + wave_length, y + wave_length, start=0, extent=180, style=ARC)
            canvas.create_arc(x, y + amplitude, x + wave_length, y + wave_length + amplitude, start=180, extent=180, style=ARC)

def draw_diagonal_pattern(canvas, line_spacing=50):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for x in range(0, canvas_width, line_spacing):
        canvas.create_line(x, 0, 0, x, fill="black")
        canvas.create_line(canvas_width - x, canvas_height, canvas_width, canvas_height - x, fill="black")
    for y in range(0, canvas_height, line_spacing):
        canvas.create_line(0, y, y, 0, fill="black")
        canvas.create_line(canvas_width, canvas_height - y, canvas_width - y, canvas_height, fill="black")

def draw_grid(canvas, step):
    canvas.delete("grid_line")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for x in range(0, width, step):
        canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid_line")
    for y in range(0, height, step):
        canvas.create_line(0, y, width, y, fill="lightgray", tags="grid_line")

def toggle_grid(canvas):
    if canvas.find_withtag("grid_line"):
        canvas.delete("grid_line")
    else:
        draw_grid(canvas, 50)

def change_grid_spacing(value):
    draw_grid(canvas, value)

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
    draw_grid(canvas, grid_spacing_global)

def draw_ruler():
    global ruler_lines, ruler_texts
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    try:
        interval = int(interval_entry.get())
    except ValueError:
        interval = 10
    for x in range(0, canvas_width, interval):
        if x % (interval * 5) == 0:
            line = canvas.create_line(x, 0, x, 15, fill="black")
            text = canvas.create_text(x, 25, text=str(x), anchor=N)
            ruler_lines.append(line)
            ruler_texts.append(text)
        else:
            line = canvas.create_line(x, 0, x, 10, fill="black")
            ruler_lines.append(line)
    for y in range(0, canvas_height, interval):
        if y % (interval * 5) == 0:
            line = canvas.create_line(0, y, 15, y, fill="black")
            text = canvas.create_text(25, y, text=str(y), anchor=W)
            ruler_lines.append(line)
            ruler_texts.append(text)
        else:
            line = canvas.create_line(0, y, 10, y, fill="black")
            ruler_lines.append(line)

def clear_ruler():
    global ruler_lines, ruler_texts
    for item in ruler_lines + ruler_texts:
        canvas.delete(item)
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
        save_canvas(canvas)
    window.destroy()

def get_image_size(file_path):
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        return size
    else:
        print("File not found.")
        return 0

def get_canvas_size(canvas):
    temp_file = "temp_canvas.ps"
    canvas.postscript(file=temp_file)
    size = get_image_size(temp_file)
    os.remove(temp_file)
    return size

def print_image_size(file_path):
    size = get_image_size(file_path)
    print("Image size:", size, "bytes")

def print_canvas_size(canvas):
    size = get_canvas_size(canvas)
    print("Canvas size:", size, "bytes")

window = Tk()
version = "1.0.0"
window.title(f"그림판 v{version}")
window.geometry("800x600+200+200")
window.resizable(True, True)
window.configure(bg="sky blue")
setup_paint_app(window)
editor = ImageEditor(canvas)
transformation_handler = TransformationHandler(canvas)

timer_label = Label(window, text="Time: 0 s")
timer_label.pack(side=RIGHT)

drag_data = {"item": None, "x": 0, "y": 0}

def open_text_input_window():
    text_input_window = Toplevel(window)
    text_input_window.title("Text Input")
    text_input = Text(text_input_window, width=30, height=5)
    text_input.pack()
    confirm_button = Button(text_input_window, text="확인", command=lambda: add_text_to_canvas(text_input.get("1.0", "end-1c")))
    confirm_button.pack()

def add_text_to_canvas(text):
    if text.strip():
        text_item = canvas.create_text(100, 100, text=text, fill="black", font=('Arial', 12))
        canvas.tag_bind(text_item, "<ButtonPress-1>", start_drag)
        canvas.tag_bind(text_item, "<B1-Motion>", drag)
        canvas.tag_bind(text_item, "<ButtonRelease-1>", end_drag)

def start_drag(event):
    drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def drag(event):
    if drag_data["item"]:
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        canvas.move(drag_data["item"], dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

def end_drag(event):
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0

text_box_button = Button(window, text="TEXTBOX", command=open_text_input_window)
text_box_button.pack()

dot_count = IntVar()
dot_count.set(10)

dot_distance = IntVar()
dot_distance.set(10)

frame_distance = Frame(window)
frame_distance.pack(side=RIGHT)

frame_count = Frame(window)
frame_count.pack(side=RIGHT)

ruler_on = False
ruler_lines = []
ruler_texts = []

interval_label = Label(window, text="Ruler Interval:")
interval_label.pack()

interval_entry = Entry(window)
interval_entry.pack()
interval_entry.insert(0, "10")

canvas.bind("<Configure>", on_resize)

bind_shortcuts_window(window)

window.protocol("WM_DELETE_WINDOW", on_closing)

timer.start()
update_timer()

window.mainloop()
