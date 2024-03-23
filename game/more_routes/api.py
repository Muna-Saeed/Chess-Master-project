#!/usr/bin/python3
from flask import Blueprint, redirect, request, jsonify, render_template
from models.user import User
from models import storage
import re
import requests
import random


api_route = Blueprint('other_routes1', __name__)



@api_route.route("/api/is_valid_move", methods=["POST"])
def is_valid_move():
    data = request.json
    board = data.get("board")
    start = data.get("start")
    end = data.get("end")
    piece_type = data.get("pieceType")
    if piece_type == '♙' and pawn_start.get((start[0], start[1])) == 0 and is_infont(board, start, end) and count_sq(start, end) < 2:
        pawn_start[(start[0], start[1])] = 1
        return jsonify({"valid_move": True})
    elif piece_type == '♖' and (is_infont(board, start, end) or sides(board, start, end)):
        return jsonify({"valid_move": True})
    elif piece_type == '♘' and knight_mv(start, end) and is_end(board, end):
        return jsonify({"valid_move": True})
    elif piece_type == '♗' and is_diagonal(start, end) and is_end(board, end):
        return jsonify({"valid_move": True})
    elif piece_type == '♕' and is_end(board, end) and count_sq(start, end) == 0:
        return jsonify({"valid_move": True})
    elif piece_type == '♔' and '♕' and is_end(board, end):
        return jsonify({"valid_move": True})
    return jsonify({"valid_move": False})


pawn_start = {
    (1, 0): 0,
    (1, 1): 0,
    (1, 2): 0,
    (1, 3): 0,
    (1, 4): 0,
    (1, 5): 0,
    (1, 6): 0,
    (1, 7): 0,
    (6, 0): 0,
    (6, 1): 0,
    (6, 2): 0,
    (6, 3): 0,
    (6, 4): 0,
    (6, 5): 0,
    (6, 6): 0,
    (6, 7): 0
}


def get_piece_moves(board, row, col):
    moves = []
    if board[row] is not None:
        
        piece = board[row][col]
        piece_color = piece[0]
        print(piece_color)
        piece_type = piece

        if piece_color == 'W':
            if row - 1 >= 0 and board[row - 1][col] == '':
                moves.append((row, col, row - 1, col))
        else:
            if row + 1 < len(board) and board[row + 1] is not None and board[row + 1][col] == '':
                moves.append((row, col, row + 1, col))
    return moves



@api_route.route('/api/generate_random_move', methods=['POST'])
def select_white_piece():
    board = request.json['board']
    start_position = None
    end_position = None
    num_columns = 8
    sq = []
    for idx, color in enumerate(board):
        row_idx = idx // num_columns
        col_idx = idx % num_columns
        if color == 'white':
            if row_idx > 0 and not board[idx - num_columns]:
                start = {'row': row_idx, 'col': col_idx}
                end = {'row': row_idx - 1, 'col': col_idx}
                sq.append((start, end))
    if sq:
        start_position, end_position = random.choice(sq)
    return jsonify({'start_position': start_position, 'end_position': end_position})



def is_infont(board, start, end):    
    x, y = start
    x = x+1
    if board[x*8+y] is not None:
        return False
    x, y = end
    if board[x*8+y] is not None:
        return False
    return True

def sides(board, start, end):
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
    if board[end[0] * 8 + end[1]]:
        return False
    return True


def count_sq(start, end):
    x0, y0 = start
    x1, y1 = end
    if x0 != x1 and y0 != y1:
        return None
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
    if board[end[0] * 8 + end[1]]:
        return False
    return True

def is_diagonal(start, end):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    if dx == dy:
        squares_between = dx - 1
        if squares_between == 0:
            print("true")
            return True
        else:
            print("more steps")
            return False
    else:
        print("NOT dig")
        return False
