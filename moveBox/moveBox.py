# 配置
# 空位
import copy

EMPTY = '.'
# 3个方向移位时x,y坐标变更值
NEXT = [(-1, 0), (1, 0), (0, 1)]
# 使用栈遍历
STACK = []


# 更新字典
def update(t_dict, y, x, value):
    if y not in t_dict:
        t_dict[y] = {}
    t_dict[y][x] = value


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
        # 行数 lines长度
        self.rows = board.rows
        # 列数 line字符数
        self.columns = board.columns

    def in_area(self, x, y):
        return 0 <= x < self.columns and 0 <= y < self.rows

    def solve(self):
        STACK.append(self.start_board)
        if self.try_solve():
            print('win')

    def try_solve(self):
        while len(STACK) > 0:
            board = STACK.pop()
            if self.is_win(board):
                return True
            if board.turn == self.max_turn:
                continue
            else:
                board.run(self.max_turn)
        return False

    def is_win(self, board):
        for y in range(self.rows):
            for char in board.data[y]:
                if EMPTY != char:
                    return False
        return True


# 每一步的盘面
class Board:
    # 初始化盘面
    def __init__(self, lines: [], turn=0) -> None:
        # 记录步数
        self.turn = turn
        # 行数 lines长度
        self.rows = len(lines)
        # 列数 line字符数
        self.columns = 0
        self.data = []
        for y in range(self.rows):
            line = []
            self.data.append(line)
            for x in range(len(lines[y])):
                if '\n' != lines[y][x]:
                    line.append(lines[y][x])
            if self.columns == 0:
                self.columns = len(line)

    def in_area(self, x, y):
        return 0 <= x < self.columns and 0 <= y < self.rows

    def swap(self, data, x, y, x_t, y_t):
        if self.in_area(x, y) and self.in_area(x_t, y_t):
            data[y][x], data[y_t][x_t] = data[y_t][x_t], data[y][x]

    def run(self, max_turn):
        # 遍历每个箱子
        for y in range(self.rows):
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
                        STACK.append(Board(data, self.turn + 1))

    def drop(self, data):
        y = self.rows - 1
        for x in range(self.columns):
            # 对最底一行逐列遍历,处理每列的箱子掉落
            i, curr = y, y
            while i > 0:
                if EMPTY != data[i][x]:
                    if curr != i:
                        data[i][x], data[curr][x] = data[curr][x], data[i][x]
                    curr -= 1
                i -= 1

    def mark_clean(self, data):
        # 存储已标记坐标
        marks = {}
        clean = False
        # 遍历每个箱子,向右方和下方各扫描两个箱子,如果重复则标记
        for y in range(self.rows):
            for x, char in enumerate(data[y]):
                if EMPTY != char:
                    for i in range(1, len(NEXT)):
                        x2, y2 = x + NEXT[i][0], y + NEXT[i][1]
                        x3, y3 = x2 + NEXT[i][0], y2 + NEXT[i][1]
                        if self.in_area(x2, y2) and self.in_area(x3, y3) and data[y2][x2] == data[y3][x3] == data[y][x]:
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
        for y in range(self.rows):
            print(str(self.data[y]))


if __name__ == '__main__':
    game_data = GameData('boston_09.txt')
    game_data.start_board.print()
    game_data.solve()
