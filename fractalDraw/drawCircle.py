# tkinter在windows下实现有锯齿,改为用js实现
import tkinter

OFFSET = 5


class DrawCircle(tkinter.Tk):

    def __init__(self, class_name, width, height, step):
        x2 = width + OFFSET
        y2 = height + OFFSET
        super().__init__(class_name)
        self.geometry('%dx%d' % (x2 + OFFSET, y2 + OFFSET))
        c = tkinter.Canvas(self, width=width, height=height)
        c.pack()
        y = int(height / 2)
        self.draw(c, OFFSET, OFFSET, width, height, step)
        self.mainloop()

    def draw(self, canvas, start_x, start_y, end_x, end_y, step, level=0):
        if start_x > end_x or start_y > end_y:
            self.mainloop()
            return
        if level % 2 == 0:
            canvas.create_oval(start_x, start_y, end_x, end_y, fill='lightblue')
        else:
            canvas.create_oval(start_x, start_y, end_x, end_y, fill='Violet')
        self.draw(canvas, start_x + step, start_y + step, end_x - step, end_y - step, step, level + 1)


if __name__ == '__main__':
    DrawCircle('画圆', 700, 700, 3)
