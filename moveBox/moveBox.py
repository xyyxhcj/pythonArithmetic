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


# 每一步的盘面
class Board:
    # 初始化盘面
    def __init__(self, lines: []) -> None:
        # 行数 lines长度
        self.rows = len(lines)
        # 列数 line字符数
        self.columns = 0
        self.data = []
        for y in range(self.rows):
            line = []
            self.data.append(line)
            if self.columns == 0:
                self.columns = len(lines[y]);
            for x in range(len(lines[y])):
                if '\n' != lines[y][x]:
                    line.append(lines[y][x])

    def print(self):
        for y in range(self.rows):
            print(str(self.data[y]))


if __name__ == '__main__':
    game_data = GameData('boston_09.txt')
    game_data.start_board.print()
