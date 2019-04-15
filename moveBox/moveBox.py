# 配置
# 空位
EMPTY = '.'
# 3个方向移位时x,y坐标变更值
NEXT = [(-1, 0), (1, 0), (0, 1)]
# 使用栈遍历
STACK = []


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
            board.run()


def is_win(self, board):
    for y in range(self.rows):
        for char in board.data[y]:
            if EMPTY != char:
                return False
    return True


# 每一步的盘面
class Board:
    # 初始化盘面
    def __init__(self, lines: []) -> None:
        # 记录步数
        self.turn = 0
        # 行数 lines长度
        self.rows = len(lines)
        # 列数 line字符数
        self.columns = 0
        self.data = []
        for y in range(self.rows):
            line = []
            self.data.append(line)
            if self.columns == 0:
                self.columns = len(lines[y])
            for x in range(len(lines[y])):
                if '\n' != lines[y][x]:
                    line.append(lines[y][x])

    def in_area(self, x, y):
        return 0 <= x < self.columns and 0 <= y < self.rows

    def swap(self, x, y, x_t, y_t):
        if self.in_area(x, y) and self.in_area(x_t, y_t):
            self.data[y][x], self.data[y_t][x_t] = self.data[y_t][x_t], self.data[y][x]

    def run(self):
        # 遍历每个箱子
        for y in range(self.rows):
            for x, char in enumerate(self.data[y]):
                if EMPTY != char:
                    # 移动,仅处理箱子
                    for i, move_x, move_y in range(len(NEXT)):
                        x_t, y_t = x + move_x, y + move_y
                        # 与左右下交换,如果左方为箱子时不处理,
                        if i == 0 and EMPTY == self.data[y_t][x_t]:
                            continue
                        self.swap(x, y, x_t, y_t)
                        while True:
                            # 掉落
                            self.drop()
                            # 标记+消除
                            if not self.mark_clean():
                                self.turn += 1
                                STACK.append(self)
                                break

    def drop(self):
        y = self.rows
        for x in range(self.columns):
            # 对最底一行逐列遍历,处理每列的箱子掉落
            i, curr = y, y
            while i > 0:
                pass

    def mark_clean(self):
        pass

    def print(self):
        for y in range(self.rows):
            print(str(self.data[y]))


if __name__ == '__main__':
    game_data = GameData('boston_09.txt')
    game_data.start_board.print()
