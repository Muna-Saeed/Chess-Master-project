from models.helper import *


def queen(board, start, color, enemy, piece_tye):
    target = get_diagonal_squares(board, start, color, enemy)
    row, col = start[0], start[1]
    return target + rook(board, start, color, enemy)

def king(board, start, color, enemy, piece_type):
    target = []
    row = start[0]
    col = start[1]
    idx = row * 8 + col +1    
    idx = row * 8 + col  -1
    if idx < 64 and idx > 0 and (board[idx] is None or board[idx] == enemy):
        target.append(idx)
    idx = row * 8 + col   + 1
    if idx < 64 and  idx > 0 and (board[idx] is None or board[idx] == enemy):
        target.append(idx)
    idx = (row - 1) * 8 + col
    if idx < 64 and idx > 0 and (board[idx] is None or board[idx] == enemy):
        target.append(idx)
    print(target)
    target += black_pawn(board, start, piece_type) + bishop(board, start,  color)
    
    return target

def black_pawn(board, start, piece_type):
    possible_moves = []
    row, col = start
    if row + 1 < 8 and board[(row + 1) * 8 + col] is None:
        possible_moves.append((row + 1) * 8 + col)

    for i in range(row + 1, row + 2):
        for j in [col - 1, col + 1]:
            idx = i * 8 + j
            if i < 8 and j < 8 and i >= 0 and j >= 0:
                if board[idx] == "white":
                    possible_moves.append(idx)
    return possible_moves

def bishop(board, start,  color):
    possible_moves = []
    row, col = start

    for i in range(row + 1, row + 2):
        for j in [col - 1, col + 1]:
            idx = i * 8 + j
            if i < 8 and j < 8 and i >= 0 and j >= 0:
                if board[idx] != color:
                    possible_moves.append(idx)

    for i in range(row - 1, row):
        for j in [col - 1, col + 1]:
            idx = i * 8 + j
            if i < 8 and j < 8 and i >= 0 and j >= 0:
                if board[idx] != color:
                    possible_moves.append(idx)
    return possible_moves

def rook(board, start, color, enemy):
    row, col = start
    possible = []
    for i in range(row - 1, -1, -1):
        if board[i * 8 + col] == color:
            break
        if board[i * 8 + col] == enemy:
            possible.append(i * 8 + col)
            break
        possible.append(i * 8 + col)

    for j in range(col - 1, -1, -1):
        if board[row * 8 + j] == enemy:
            possible.append(row * 8 + j)
            break
        elif board[row * 8 + j] == color:
            break
        possible.append(row * 8 + j)

    for k in range(col + 1, 8):
        if board[row * 8 + k] == color:
            break
        elif board[row * 8 + k] == enemy:
            possible.append(row * 8 +  k)
            break
        possible.append(row * 8 +  k)
    for i in range(row + 1, 8):
        if board[i * 8 + col] == color:
            break
        if board[i * 8 + col] == enemy:
            possible.append(i * 8 + col)
            break
        possible.append(i * 8 + col)
    return possible


def faras(board, start, color, enemy):
    target = []
    for n, loc in enumerate(board):
        x = n // 8
        y = n % 8
        
        if board[n] != color and knight_mv((x, y), start):
            target.append(x * 8 + y)

    return target


def get_diagonal_squares(board, start, color, enemy):
    row, col = start  
    diagonal_squares = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r * 8 + c] == color:
                break
            if board[r * 8 + c] == enemy:
                diagonal_squares.append(r * 8 + c)
                break
            diagonal_squares.append(r * 8 + c)
            r += dr
            c += dc
    return diagonal_squares
