# erase.py
def erase(event, canvas):
    x1, y1 = (event.x - 5), (event.y - 5)
    x2, y2 = (event.x + 5), (event.y + 5)
    canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")