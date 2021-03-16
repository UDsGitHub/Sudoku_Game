import random

# difficulties 35, 20, 8

difficulty = 8

grid = [[0 for j in range(9)] for i in range(9)]


def check_valid(board, pos, n):

    # check columns
    for i in range(9):
        if board[pos[0]][i] == n and pos[0] != i:
            return False

    # check rows
    for j in range(9):
        if board[j][pos[1]] == n and pos[1] != j:
            return False

    # check squares
    box_row = pos[0] // 3
    box_col = pos[1] // 3

    for k in range(3):
        for l in range(3):
            if board[box_row * 3 + k][box_col * 3 + l] == n and (k,l) != pos:
                return False

    return True


def make_grid(diffc):
    for i in range(diffc):
        row = random.randrange(9)
        col = random.randrange(9)
        num = random.randint(1,9)

        while not check_valid(grid, (row, col), num) or grid[row][col] != 0:
            row = random.randrange(9)
            col = random.randrange(9)
            num = random.randint(1, 9)

        grid[row][col] = num
    return grid

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(str(bo[i][j]))
            else:
                print(str(bo[i][j]) + " ", end="")
