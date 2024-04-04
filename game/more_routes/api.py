#!/usr/bin/python3
from flask import Blueprint, redirect, request, jsonify, render_template
from models.user import User
from models import storage
import re
import requests
import random
from models.helper import *
from models.legal_moves import *
from models.game import Game



api_route = Blueprint('other_routes1', __name__)



game = None
board =  [None] * 64
board[:16] = ["black"] * 16
board[-16:] = ["white"] * 16

@api_route.route("/api/possible", methods=["POST"])
def possible():
    global game
    data = request.json
    if game:
        board = game.board
    else:
        board = board
    start = data.get("start")
    color = data.get("color")
    piece_type = data.get("pieceType")
    
    enemy = "white" if color == "black" else "black"


    if piece_type == '♕':
        game.queen_move = queen(board, start, color, enemy, None)
        return jsonify({"moves":game.queen_move})
    elif piece_type == '♔':
        game.king = king(board, start, color, enemy, None)
        return jsonify({"moves":game.king})
    elif piece_type == '♗':
        game.bishop_move = bishop(board, start, color)
        return jsonify({"moves": game.bishop_move})
    elif piece_type == '♖':
        game.rook = rook(board, start, color, enemy)
        return jsonify({"moves": game.rook})
    elif piece_type == '♘' :
        game.knight = faras(board, start, color, enemy)
        return jsonify({"moves": game.knight})
    else:
        if color == "black":
            game.pawn = black_pawn(board, start, game)
            return jsonify({"moves": game.pawn})
        else:
            game.pawn = white_pawn(board, start, game)
            return jsonify({"moves": game.pawn})
        


@api_route.route("/api/is_valid_move", methods=["POST"])
def is_valid_move():
    data = request.json
    board = game.board
    color_board = data.get('boardColor')
    color = data.get("color")
    start = data.get("start")
    enemy = data.get("enemy")
    end = data.get("end")
    idx = end[0] * 8 + end[1]
    piece_type = data.get("pieceType")

    if piece_type == '♙' and hasattr(game, 'pawn') and idx in game.pawn:
            return jsonify({"valid_move": True, "killed": not is_end(board, end)})
    elif piece_type == '♗' and hasattr(game, 'bishop_move') and idx in game.bishop_move:
            return jsonify({"valid_move": True, "killed": not is_end(board, end)})
    elif piece_type == '♖' and hasattr(game, 'rook') and idx in game.rook:
        return jsonify({"valid_move": True, "killed": not is_end(board, end)})
    elif piece_type == '♘' and hasattr(game, 'knight') and idx in game.knight:
        return jsonify({"valid_move": True, "killed": not is_end(board, end)})
    elif piece_type == '♔' and hasattr(game, 'king') and idx in game.king:
        return jsonify({"valid_move": True, "killed": not is_end(board, end)})
    elif piece_type == '♕' and hasattr(game, 'queen_move') and idx in game.queen_move:
        return jsonify({"valid_move": True, "killed": not is_end(board, end)})
    return jsonify({"valid_move": False, "killed": False})






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


@api_route.route('/game', methods=['POST'])
def leter_name():
    board = request.json['board']
    return jsonify({'baord': board})
    
    
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


@api_route.route('/api/board', methods=['POST'])
def update_board():
    global game
    data = request.json
    color_board = data.get('ColorBoard')
    game_id = data.get('gameId')
    print(game_id)
    user_id = data.get('userId')
    game = storage.get(Game, game_id)
    if (game):
        game.board = color_board
    elif game_id:
        game = Game()
        game.id = game_id
        game.board = color_board
        storage.new(game)
    else:
        return "not game"
    

    
    return 'Board updated successfully', 200


@api_route.route('/api/invite', methods=['POST'])
def invite():
    data = request.json
    player_id = data['player_id']
    return 'ok', 200
