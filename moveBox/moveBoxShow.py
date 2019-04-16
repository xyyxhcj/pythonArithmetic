import copy
import tkinter
# 配置
import tkinter.font

LABEL_WIDTH = 5
LABEL_HEIGHT = 2
# 空位
EMPTY = '.'
# 3个方向移位时x,y坐标变更值
NEXT = [(-1, 0), (1, 0), (0, 1)]
# 使用栈遍历
STACK = []
# 箱子颜色
COLORS = ['yellow', 'Pink', 'Plum', 'Navy', 'Cyan', 'Teal', 'Olive', 'Gold', 'Tan', 'Coral']
# 存储不同字符对应的颜色
COLOR_DICT = {}
# 选中箱子的前景色
SELECT_FG = 'snow'
# 默认前景色
DEFAULT_FG = 'black'
# 空区域颜色
EMPTY_COLOR = 'white'
# 全局盘面
GLOBAL_BOARD = None
# 延时
DELAY = 300
COLUMNS = 0
ROWS = 0


# 更新字典
def update(t_dict, y, x, value):
    if y not in t_dict:
        t_dict[y] = {}
    t_dict[y][x] = value


# 判断是否越界
def in_area(x, y):
    return 0 <= x < COLUMNS and 0 <= y < ROWS


# 每一局的数据
class GameData:
    # 读取文件初始化数据
    def __init__(self, file_name) -> None:
        f = open(file_name)
        # 最大步数
        self.max_turn = int(f.readline())
        # 原始状态
        board = Board(f.readlines())
        self.start_board = board
        f.close()

    def solve(self):
        STACK.append(self.start_board)
        solve = self.try_solve()
        if isinstance(solve, Board):
            solve.swap_log()

    def try_solve(self):
        while len(STACK) > 0:
            board = STACK.pop()
            if self.is_win(board):
                return board
            if board.turn == self.max_turn:
                continue
            else:
                board.run(self.max_turn)
        return False

    def is_win(self, board):
        for y in range(ROWS):
            for char in board.data[y]:
                if EMPTY != char:
                    return False
        return True


# 每一步的盘面
class Board:
    # 初始化盘面
    def __init__(self, lines: [], turn=0, pre_board=None, swap_info='') -> None:
        # 存储上一步
        self.pre_board = pre_board
        # 存储交换信息
        self.swap_info = swap_info
        # 记录步数
        self.turn = turn
        global ROWS, COLUMNS
        # 行数 lines长度
        ROWS = len(lines)
        # 列数 line字符数
        COLUMNS = 0
        self.data = []
        for y in range(ROWS):
            line = []
            self.data.append(line)
            for x in range(len(lines[y])):
                if '\n' != lines[y][x]:
                    line.append(lines[y][x])
            if COLUMNS == 0:
                COLUMNS = len(line)

    @staticmethod
    def swap(data, x, y, x_t, y_t):
        if in_area(x, y) and in_area(x_t, y_t):
            data[y][x], data[y_t][x_t] = data[y_t][x_t], data[y][x]

    def run(self, max_turn):
        # 遍历每个箱子
        for y in range(ROWS):
            for x, char in enumerate(self.data[y]):
                if EMPTY != char:
                    # 移动,仅处理箱子
                    for i, (move_x, move_y) in enumerate(NEXT):
                        x_t, y_t = x + move_x, y + move_y
                        # 与左右下交换,如果左方为箱子时不处理,
                        if i == 0 and EMPTY == self.data[y_t][x_t]:
                            continue
                        data = copy.deepcopy(self.data)
                        self.swap(data, x, y, x_t, y_t)
                        while True:
                            # 掉落
                            self.drop(data)
                            # 标记+消除
                            if not self.mark_clean(data):
                                break
                        swap_info = '(%d,%d) swap to (%d,%d)' % (x, y, x_t, y_t)
                        STACK.append(Board(data, self.turn + 1, self, swap_info))

    @staticmethod
    def drop(data):
        y = ROWS - 1
        for x in range(COLUMNS):
            # 对最底一行逐列遍历,处理每列的箱子掉落
            i, curr = y, y
            while i > 0:
                if EMPTY != data[i][x]:
                    if curr != i:
                        data[i][x], data[curr][x] = data[curr][x], data[i][x]
                    curr -= 1
                i -= 1

    @staticmethod
    def mark_clean(data):
        # 存储已标记坐标
        marks = {}
        clean = False
        # 遍历每个箱子,向右方和下方各扫描两个箱子,如果重复则标记
        for y in range(ROWS):
            for x, char in enumerate(data[y]):
                if EMPTY != char:
                    for i in range(1, len(NEXT)):
                        x2, y2 = x + NEXT[i][0], y + NEXT[i][1]
                        x3, y3 = x2 + NEXT[i][0], y2 + NEXT[i][1]
                        if in_area(x2, y2) and in_area(x3, y3) and data[y2][x2] == data[y3][x3] == data[y][x]:
                            # 标记
                            update(marks, y, x, True)
                            update(marks, y2, x2, True)
                            update(marks, y3, x3, True)
                            clean = True
        # 消除
        for y, mark_y in marks.items():
            for x in mark_y:
                data[y][x] = EMPTY
        return clean

    def print(self):
        # 可视化
        MoveTheBox(self.data, class_name='move box').mainloop()

    def swap_log(self):
        if self.pre_board is not None:
            self.pre_board.swap_log()
        print(self.swap_info)


class MoveTheBox(tkinter.Tk):

    def __init__(self, data, class_name):
        super().__init__(class_name)
        # 存储展示数据
        self.show_data = []
        # 存储选中区:坐标(x,y)
        self.selected = None
        # 标签字体
        self.font = tkinter.font.Font(family='Gill Sans', size=10, weight=tkinter.font.BOLD)
        # 初始化展示数据
        for y in range(len(data)):
            l_x = []
            self.show_data.append(l_x)
            for x in range(len(data[y])):
                text = ''
                val = data[y][x]
                if EMPTY != val:
                    if val not in COLOR_DICT:
                        COLOR_DICT[val] = COLORS.pop()
                    color = COLOR_DICT[val]
                    fg = DEFAULT_FG
                else:
                    color = EMPTY_COLOR
                    fg = EMPTY_COLOR
                text = '%d_%d' % (x, y)
                label = tkinter.Label(self, text=text, width=LABEL_WIDTH, height=LABEL_HEIGHT, bg=color, font=self.font,
                                      fg=fg)
                label.bind('<Button-1>', lambda event, x_t=x, y_t=y: self.click_label(x_t, y_t))
                label.grid(row=y, column=x)
                l_x.append({'val': val, 'label': label})

    def click_label(self, x, y):
        # 选中区前景色
        if self.selected is None:
            self.show_data[y][x]['label']['fg'] = 'snow'
            self.selected = (x, y)
        else:
            s_x, s_y = self.selected
            # 如果位置相邻则交换,去除selected及前景色
            if abs(s_x - x) + abs(s_y - y) == 1:
                self.swap_val_bg(x, y, s_x, s_y)
                self.selected = None
                # 循环掉落->消除
                while True:
                    self.drop()
                    if not self.mark_clean():
                        break

    # 掉落
    def drop(self):
        y = len(self.show_data) - 1
        for x, val in enumerate(self.show_data[y]):
            # 对最底一行逐列遍历,处理每列的箱子掉落
            i, curr = y, y
            while i > 0:
                if EMPTY != self.show_data[i][x]['val']:
                    if curr != i:
                        self.swap_val_bg(x, i, x, curr)
                    curr -= 1
                i -= 1

    # 标记清除
    def mark_clean(self):
        marks = {}
        clean = False
        for y in range(len(self.show_data)):
            for x, item in enumerate(self.show_data[y]):
                if EMPTY != item['val']:
                    for i in range(1, len(NEXT)):
                        x2, y2 = x + NEXT[i][0], y + NEXT[i][1]
                        x3, y3 = x2 + NEXT[i][0], y2 + NEXT[i][1]
                        if in_area(x2, y2) and in_area(x3, y3) and self.show_data[y2][x2]['val'] \
                                == self.show_data[y3][x3]['val'] == self.show_data[y][x]['val']:
                            # 标记
                            update(marks, y, x, True)
                            update(marks, y2, x2, True)
                            update(marks, y3, x3, True)
                            clean = True
        for y, mark_y in marks.items():
            for x in mark_y:
                self.show_data[y][x]['val'] = EMPTY
                self.reset_fg(x, y)
        return clean

    # 调整前景色
    def reset_fg(self, x, y):
        if EMPTY != self.show_data[y][x]['val']:
            self.show_data[y][x]['label']['fg'] = DEFAULT_FG
        else:
            self.show_data[y][x]['label']['fg'] = EMPTY_COLOR
            self.show_data[y][x]['label']['bg'] = EMPTY_COLOR

    # 移位
    def swap_val_bg(self, x, y, x_t, y_t):
        self.show_data[y_t][x_t]['val'], self.show_data[y][x]['val'] = self.show_data[y][x]['val'], \
                                                                       self.show_data[y_t][x_t]['val']
        self.show_data[y][x]['label']['bg'], self.show_data[y_t][x_t]['label']['bg'] = \
            self.show_data[y_t][x_t]['label']['bg'], self.show_data[y][x]['label']['bg']
        self.reset_fg(x, y)
        self.reset_fg(x_t, y_t)
        self.show_data[y][x]['label'].update()
        self.show_data[y_t][x_t]['label'].update()
        self.show_data[y][x]['label'].after(DELAY)
        self.show_data[y_t][x_t]['label'].after(DELAY)


if __name__ == '__main__':
    game_data = GameData('boston_09.txt')
    game_data.solve()
    game_data.start_board.print()
