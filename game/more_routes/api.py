#!/usr/bin/python3
from flask import Blueprint, redirect, request, jsonify, render_template
from models.user import User
from models import storage
import re
import requests
import random
from models.helper import *

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
    elif piece_type == '♖' and is_all_none(board, start, end) and not is_diagonal(start, end):
        if is_end(board, end):
            return jsonify({"valid_move": True, "killed": False})
        elif enemy:
            return jsonify({"valid_move": True, "killed": True})
        return jsonify({"valid_move": False})
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
    elif piece_type == '♕' and ((sides(board, start, end) or is_infont(board, start, end)) or not is_diagonal(start, end)):
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
    pieceBoard = request.json['pieceBoard']
    num_columns = 8
    sq = []
    for (idx, color), piece in zip(enumerate(board), pieceBoard):
        row_idx = idx // num_columns
        col_idx = idx % num_columns
        loc = (row_idx, col_idx)
        start = {'row': row_idx, 'col': col_idx}
        if color == 'white':
            print(piece)
            if piece == "♙":
                end = bacward_diagonal(board, row_idx - 1, col_idx, loc)
                target = end[0] * 8 + end[1] if end else False
                if end and board[target] == "black":
                    end = {'row': end[0], 'col': end[1]}
                    return jsonify({'start_position': start, 'end_position': end, "killed": True})
                elif end and board[target] is None:
                    end = {'row': end[0], 'col': end[1]}
                    sq.append((start, end))
            if piece == "♖":
                ends = longest_backward_move(board, row_idx, col_idx)
                if ends and board[ends[0] * 8 + ends[1]] != "white":
                    end = {'row': ends[0], 'col': ends[1]}
                    if is_end(board, ends):
                        sq.append((start, end))
                    else:
                        return jsonify({'start_position': start, 'end_position': end, "killed": True})
            if piece == '♘':
                pos = random_knight_mv(board, loc)
                if pos:
                    x, y = pos
                    end = {'row': x, 'col': y}
                    flag = True if board[x * 8 + y] else False
                    if flag:return jsonify({'start_position': start, 'end_position': end, "killed": flag})
                    else:sq.append((start, end))
            if piece == '♗':
                end = bacward_diagonal(board, row_idx - 1, col_idx, loc)
                target = end[0] * 8 + end[1] if end else False
                print("biship end: ", end, board[target])
                if end and board[target] == "black":
                    end = {'row': end[0], 'col': end[1]}
                    return jsonify({'start_position': start, 'end_position': end, "killed": True})
                elif end:
                    print(end)
                    if is_end(board, end):
                        end = {'row': end[0], 'col': end[1]}
                        sq.append((start, end))
            if piece == "♕":
                ends = longest_backward_move(board, row_idx, col_idx)
                if ends and board[ends[0] * 8 + ends[1]] != "white":
                    end = {'row': ends[0], 'col': ends[1]}
                    if is_end(board, ends):
                        sq.append((start, end))
                    else:
                        return jsonify({'start_position': start, 'end_position': end, "killed": True})
            elif piece == '♔':
               end = get_one_move(board, loc)
               if end:
                   idx = end[0] * 8 + end[1]
                   end = {'row': end[0], 'col': end[1]}
                   if idx < 64 and board[idx]:
                       return jsonify({'start_position': start, 'end_position': end, "killed": True})
                   else:sq.append((start, end))
            if is_end(board, (row_idx-1, col_idx)) and piece != '♗':
                start = {'row': row_idx, 'col': col_idx}
                end = {'row': row_idx - 1, 'col': col_idx}
                sq.append((start, end))
    if sq:
        start_position, end_position = random.choice(sq)
    return jsonify({'start_position': start_position, 'end_position': end_position})


    
    
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


def random_knight_mv(board, start):
    target = {"black":[], None: []}
    for n, loc in enumerate(board):
        x = n // 8
        y = n % 8
        
        if board[n] != 'white' and knight_mv((x, y), start):
            target[loc].append((x, y))
    if target['black']:
        return random.choice(target['black'])
    elif target[None]:
        return random.choice(target[None])
    return False
