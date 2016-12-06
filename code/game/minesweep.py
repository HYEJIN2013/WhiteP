# -*- coding=utf-8 -*-

SIZE = (10, 10)
BOMBNUM = 5

import random


class Map(list):

    def __init__(self, size):
        super(list, self).__init__()
        self.size_x, self.size_y = size
        self.total_num = self.size_x * self.size_y
        self += [0] * self.total_num
        self.unknow = [True] * self.total_num

    def index2xy(self, index):
        x = int(index / self.size_y)
        y = int(index % self.size_y)
        return x, y

    def xy2index(self, x, y):
        return int(x * self.size_y + y)

    def get_side_list(self, index):
        side_list = []
        dirs = (
            (0, 0), (0, 1), (0, -1),
            (1, 0), (1, 1), (1, -1),
            (-1, 0), (-1, 1), (-1, -1))
        x, y = self.index2xy(index)
        for dir_x, dir_y in dirs:
            fix_x = x + dir_x
            fix_y = y + dir_y
            if 0 <= fix_x and fix_x < self.size_x and \
                    0 <= fix_y and fix_y < self.size_y:
                side_list.append(self.xy2index(fix_x, fix_y))
        return side_list

    def _update_bomb_side(self, index):
        for fix_index in self.get_side_list(index):
            if self[fix_index] < 9:
                self[fix_index] += 1

    def put_bomb(self, num):
        bomb_list = random.sample(range(self.total_num), num)
        for index in bomb_list:
            self[index] = 9
            self._update_bomb_side(index)

    def click(self, x, y):
        index = self.xy2index(x, y)
        if self[index] == 9:
            self.unknow = [False] * self.total_num
            return False
        elif self[index] == 0:
            self.unknow[index] = False
            for fix_index in self.get_side_list(index):
                if self.unknow[fix_index]:
                    fix_x, fix_y = self.index2xy(fix_index)
                    self.click(fix_x, fix_y)
        else:
            self.unknow[index] = False
        return True

    def output(self):
        str_list = [str(i) for i in range(self.size_y)]
        print(' ' * 6 + ' '.join(str_list))
        print(' ' * 6 + '-' * (self.size_y * 2 - 1))
        for x in range(self.size_x):
            begin = x * self.size_y
            end = (x+1) * self.size_y
            f = lambda i: '+' if self.unknow[i] else str(self[i])
            str_list = map(f, range(begin, end))
            print('%3s | ' % x + ' '.join(str_list).replace('9', '*'))


if __name__ == '__main__':
    m = Map(SIZE)
    m.put_bomb(BOMBNUM)
    print("SIZE:%s   BOMBNUM:%s" % (SIZE, BOMBNUM))
    while True:
        m.output()
        try:
            x, y = raw_input().split(' ')
        except:
            x, y = input().split(' ')
        x, y = int(x), int(y)
        if not m.click(x, y):
            m.output()
            print('!!! GAME OVER !!!')
            break
        elif len([i for i in m.unknow if i]) == BOMBNUM:
            m.output()
            print('!!! GAME SUCCESSED !!!')
            break
