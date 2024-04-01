def longest_backward_move(board, row, col):
    last_black_backward = None
    last_black_left = None
    last_black_right = None
    longest = None


    for i in range(row - 1, -1, -1):
        if board[i * 8 + col] == 'white':
            if i < 7 and board[(i + 1) * 8 + col] is None:
                longest = (i + 1, col)
            break
        if board[i * 8 + col] == 'black':
            last_black_backward = (i, col)
            break
    for j in range(col - 1, -1, -1):
        if board[row * 8 + j] == 'white':
            if j < 7 and board[row * 8 + j + 1] is None and longest is None:
                longest = (row, j + 1)
            break
        if board[row * 8 + j] == "black":
            last_black_left = (row, j)
            return last_black_left
    for k in range(col + 1, 8):
        if board[row * 8 + k] == 'white':
            if k > 0 and board[row * 8 + k - 1] is None and longest is None:
                longest = (row, k - 1)
            break
        if board[row * 8 + k] == 'black':
            last_black_right = (row, k)
            break
    for i in range(row + 1, 8):
        if board[i * 8 + col] == 'white':
            if i > 0 and board[(i - 1) * 8 + col] is None:
                longest = (i - 1, col)
            break
        if board[i * 8 + col] == 'black':
            return (i, col)

    if last_black_backward:
        return last_black_backward
    if last_black_left:
        return last_black_left
    if last_black_right:
        return last_black_right
    return longest

def bacward_diagonal(board, row, col, end):
    ran = col + 2
    if col > 0:
        col = col - 1
    for i in range(col, ran):
        start = row, i
        idx = row * 8 + i
        if idx < 64 and board[idx] and is_diagonal(start, end):
            return start
    return False



def is_infont(board, start, end):
    x, y = start
    x = x+1
    loc = x*8+y
    if loc < 64 and board[x*8+y] is not None:
        return False
    x, y = end
    return True

def sides(board, start, end):
    """ check if the move is to forward, left or right and back"""
    x0, y0 = start
    x1, y1 = end
    if x0 != x1:
        return False
    direction = 1 if y1 > y0 else -1
    squares = [(x0, y) for y in range(y0 + direction, y1, direction)]

    for sq in squares:
        x, y = sq
        if board[x * 8 + y]:
            return False
    return True


def count_sq(start, end):
    """ count how many squares between the clicked and destination"""
    x0, y0 = start
    x1, y1 = end
    if x0 != x1 and y0 != y1:
        """note same line"""
        return 3
    if x0 == x1:
        return abs(y1 - y0) - 1
    else:
        return abs(x1 - x0) - 1

def knight_mv(start, end):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
        return True
    else:
        return False

def is_end(board, end):
    """ check the end poition before moving to"""
    loc = end[0] * 8 + end[1]
    if loc < 64 and board[loc] is not None:
        return False
    elif loc < 64:
        return True
    return False

def is_diagonal(start, end):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    if dx == dy:
        squares_between = dx - 1
        if squares_between == 0:
            return True
        else:
            return 0
    else:
        return False

def is_forward(start, end):
    start_row, end_row = start[0], end[0]
    if start_row == end_row:
        return False
    return end_row > start_row


def is_all_none(board, start, end):
    start_x, start_y = start
    end_x, end_y = end
    if start_x == end_x:
        if start_y < end_y:
            for i in range(start_y + 1, end_y):
                if board[start_x * 8 + i] is not None:
                    return False
        else:
            for i in range(end_y + 1, start_y):
                if board[start_x * 8 + i] is not None:
                    return False
    elif start_y == end_y:
        if start_x < end_x:
            for i in range(start_x + 1, end_x):
                if board[i * 8 + start_y] is not None:
                    return False
        else:
            for i in range(end_x + 1, start_x):
                if board[i * 8 + start_y] is not None:
                    return False
    else:
        return False

    return True



def get_one_move(board, loc):
    p_row = loc[0] + 1
    p_column = loc[1]
    next_row = loc[0] - 1
    next_column = loc[1]
    left_x, left_y = loc[0], loc[1] - 1
    right_x, right_y = loc[0], loc[1] + 1

    idx_left = left_x * 8 + left_y
    idx_right = right_x * 8 + right_y
    
    idx_f = next_row * 8 + next_column
    idx_b = p_row * 8 + p_column

    if idx_f >= 0 and idx_f < 64 and board[idx_f] == "black":
        return (next_row, next_column)
    elif idx_left < 64 and board[idx_left] == "black":
        return (loc[0], loc[1] - 1)
    elif idx_right < 64 and board[idx_right] == "black":
        return (loc[0], loc[1] + 1)
    elif idx_f - 1 >= 0 and idx_f - 1 < 64 and board[idx_f - 1] == "black":
        return (next_row, next_column - 1)
    elif idx_f + 1 >= 0 and idx_f + 1 < 64 and board[idx_f + 1] == "black":
        return (next_row, next_column + 1)
    elif idx_b >= 0 and idx_b < 64 and board[idx_b] == "black":
        return (p_row, p_column)
    elif idx_b - 1 >= 0 and idx_b - 1 < 64 and board[idx_b - 1] == "black":
        return (p_row , p_column - 1)
    elif idx_b + 1 >= 0 and idx_b + 1 < 64 and board[idx_b + 1] == "black":
        return (p_row , p_column + 1)
    elif idx_f < 64 and board[idx_f] is None:
        return (next_row, next_column)
    elif idx_b < 64 and board[idx_b] is None:
        return (p_row, p_column)
    elif idx_left < 64 and board[idx_left] is None:
        return (loc[0], loc[1] - 1)
    elif idx_right < 64 and board[idx_right] is None:
        return (loc[0], loc[1] + 1)
    else:
        return False
