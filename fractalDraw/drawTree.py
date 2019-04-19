# 递归画树
import random
import tkinter

import math

OFFSET = 5
# 分叉角度
ANGLE = 45
# 取多少为树干
TRUNK_LENGTH = 2 / 5


class DrawTree(tkinter.Tk):
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
        self.draw(self.canvas, OFFSET + length / 2, length, length, 90, min_length)
        self.mainloop()

    def get_min(self, depth):
        math_pow = math.pow(2, depth)
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
                self.draw(self.canvas, OFFSET + self.length / 2, self.length, self.length, 90, min_length)
                self.mainloop()

    # line:线长,angle:角度
    def draw(self, canvas, start_x, start_y, line, angle, min_length):
        # 计算终点坐标
        end_x = start_x + line * math.cos(math.radians(angle))
        end_y = start_y - line * math.sin(math.radians(angle))
        if line <= min_length:
            # 连线
            canvas.create_line(start_x, start_y, end_x, end_y, width=2, fill='snow')
        else:
            # a结点坐标
            a_x, a_y = start_x + (end_x - start_x) * TRUNK_LENGTH, start_y + (end_y - start_y) * TRUNK_LENGTH
            # b_x, b_y = a_x + line * math.cos(math.radians(angle + ANGLE)), a_y - line * math.sin(
            #     math.radians(angle + ANGLE))
            # c_x, c_y = a_x - line * math.cos(math.radians(angle + ANGLE)), a_y - line * math.sin(
            #     math.radians(angle + ANGLE))
            canvas.create_line(start_x, start_y, a_x, a_y, width=2, fill='snow')
            # 添加随机角度 random.randint(-25, 15)
            self.draw(canvas, a_x, a_y, line * (1 - TRUNK_LENGTH), angle + ANGLE + random.randint(-25, 25), min_length)
            self.draw(canvas, a_x, a_y, line * (1 - TRUNK_LENGTH), angle - ANGLE + random.randint(-25, 25), min_length)


def main():
    DrawTree('tree', 900, 2)


if __name__ == '__main__':
    main()
