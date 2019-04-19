# 雪花分形
import tkinter

import math

OFFSET = 5
# 正三角形角度
ANGLE = 60


class Snowflake(tkinter.Tk):
    def __init__(self, class_name, length, depth):
        self.length = length
        super().__init__(className=class_name)
        # 计算停止递归的边长
        x2 = y2 = length + OFFSET
        min_length = self.get_min(depth)
        self.geometry('%dx%d' % (x2 + OFFSET, y2 + OFFSET))
        self.canvas = tkinter.Canvas(self, width=length, height=length)
        self.bind('<Key>', self.redraw)
        self.canvas.pack()
        self.draw(self.canvas, OFFSET, length, length, 0, min_length)
        self.mainloop()

    def get_min(self, depth):
        math_pow = math.pow(3, depth)
        min_length = max(self.length / math_pow, 2)
        print('min_length:%d' % min_length)
        return min_length

    def redraw(self, event):
        # 判断是否数字
        char = event.char
        if char.isdigit():
            click_num = int(char)
            if 0 <= click_num < 10:
                min_length = self.get_min(click_num)
                self.canvas.destroy()
                self.canvas = tkinter.Canvas(self, width=self.length, height=self.length)
                self.canvas.pack()
                self.draw(self.canvas, OFFSET, self.length, self.length, 0, min_length)
                self.mainloop()

    # line:线长,angle:角度
    def draw(self, canvas, start_x, start_y, line, angle, min_length):
        #
        if line <= min_length:
            # 计算终点坐标 连线
            canvas.create_line(start_x, start_y, start_x + line * math.cos(math.radians(angle)),
                               start_y - line * math.sin(math.radians(angle)))
        else:
            # 每条线段的长度
            line = line / 3
            # 计算abc结点的坐标
            a_x, a_y = start_x + line * math.cos(math.radians(angle)), start_y - line * math.sin(math.radians(angle))
            b_x, b_y = a_x + line * math.cos(math.radians(angle + ANGLE)), a_y - line * math.sin(
                math.radians(angle + ANGLE))
            c_x, c_y = b_x + line * math.cos(math.radians(angle - ANGLE)), b_y - line * math.sin(
                math.radians(angle - ANGLE))
            self.draw(canvas, start_x, start_y, line, angle, min_length)
            self.draw(canvas, a_x, a_y, line, angle + ANGLE, min_length)
            self.draw(canvas, b_x, b_y, line, angle - ANGLE, min_length)
            self.draw(canvas, c_x, c_y, line, angle, min_length)


def main():
    Snowflake('snowflake', 900, 2)


if __name__ == '__main__':
    main()
