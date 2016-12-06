import random

LINE = 3
BOARD = [random.choice([0,1]) for i in range(LINE * LINE)]

def switch(pos):
    for i in range(len(BOARD)):
        if (i + 1 is pos and (i + 1) % LINE is not 0) or \
           (i - 1 is pos and (i + 1) % LINE is not 1) or \
           i + LINE is pos or \
           i - LINE is pos:
            BOARD[i] = (BOARD[i] + 1) % 2
    BOARD[pos] = (BOARD[pos] + 1) % 2
    if 1 not in BOARD or 0 not in BOARD:
        return True
    return False

if __name__ == "__main__":
    end = False
    cnt = 0

    while not end:
        for i in range(0, len(BOARD), LINE):
            print(BOARD[i:i+LINE])
        pos = input(">")
        cnt += 1
        end = switch(int(pos))

    for i in range(0, len(BOARD), LINE):
        print(BOARD[i:i+LINE])

    print("ome")
    print("cnt:", cnt)
