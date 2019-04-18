# tkinter在windows下实现有锯齿,改为用js实现
import tkinter

OFFSET = 5


class DrawCircle(tkinter.Tk):

    def __init__(self, class_name, width, height, step):
        self.width = width
        self.height = height
        x2 = width + OFFSET
        y2 = height + OFFSET
        super().__init__(class_name)
        self.geometry('%dx%d' % (x2 + OFFSET, y2 + OFFSET))
        self.canvas = tkinter.Canvas(self, width=width, height=height)
        self.bind('<Key>', self.redraw)
        self.canvas.pack()
        self.draw(self.canvas, OFFSET, OFFSET, width, height, step)

    def draw(self, canvas, start_x, start_y, end_x, end_y, step, depth=0):
        if step < 3:
            step = 3
        if start_x > end_x or start_y > end_y:
            self.mainloop()
            return
        if depth % 2 == 0:
            canvas.create_oval(start_x, start_y, end_x, end_y, fill='lightblue', width=2)
        else:
            canvas.create_oval(start_x, start_y, end_x, end_y, fill='Violet', width=2)
        self.draw(canvas, start_x + step, start_y + step, end_x - step, end_y - step, step, depth + 1)

    def redraw(self, event):
        click_num = int(event.char)
        print(click_num)
        if 0 < click_num < 10:
            self.draw(self.canvas, OFFSET, OFFSET, self.width, self.height, click_num)


if __name__ == '__main__':
    DrawCircle('画圆', 500, 500, 5)
