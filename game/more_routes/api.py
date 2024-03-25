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
    color_board = data.get('boardColor')
    start = data.get("start")
    enemy = data.get("enemy")
    end = data.get("end")
    piece_type = data.get("pieceType")

    if piece_type == '♙' and is_infont(board, start, end) and count_sq(start, end) < 2 and is_forward(start, end):
        if pawn_start.get((start[0], start[1])) == 0:
            pawn_start[(start[0], start[1])] = 1
            return jsonify({"valid_move": True, "killed": False})
        elif count_sq(start, end) == 0:
            return jsonify({"valid_move": True, "killed": False})
    elif piece_type == '♙' and enemy and is_diagonal(start, end) and not is_end(board, end):
            return jsonify({"valid_move": True, "killed": True})
    elif piece_type == '♖' and (is_forward(start, end) or sides(board, start, end)) and not is_diagonal(start, end):
        print("in")
        if is_end(board, end):
            return jsonify({"valid_move": True, "killed": False})
        elif enemy:
            return jsonify({"valid_move": True, "killed": True})
        return jsonify({"valid_move": True})
    elif piece_type == '♘' and knight_mv(start, end):
        if is_end(board, end):
            return jsonify({"valid_move": True, "killed": False})
        elif enemy:
            return jsonify({"valid_move": True, "killed": True})
    elif piece_type == '♗' and is_diagonal(start, end):
        if is_end(board, end):
            return jsonify({"valid_move": True, "killed": False})
        elif enemy:
            return jsonify({"valid_move": True, "killed": True})
    elif piece_type == '♔' and count_sq(start, end) == 0:
        if is_end(board, end):
            return jsonify({"valid_move": True, "killed": False})
        elif enemy:
            return jsonify({"valid_move": True, "killed": True})
    elif piece_type == '♕':
        if is_end(board, end):
            return jsonify({"valid_move": True, "killed": False})
        elif enemy:
            return jsonify({"valid_move": True, "killed": True})

    return jsonify({"valid_move": False, "killed": False})


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
            print("No sqauare between them")
            return True
        else:
            print("more steps")
            return False
    else:
        return False

def is_forward(start, end):
    start_row, end_row = start[0], end[0]
    if start_row == end_row:
        return False
    return end_row > start_row
