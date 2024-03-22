#!/usr/bin/python3
from flask import Blueprint, redirect, request, jsonify, render_template
from models.user import User
from models import storage
import re
import requests

api_route = Blueprint('other_routes1', __name__)
emails = storage.get_user_email();



@api_route.route("/api/is_valid_move", methods=["POST"])
def is_valid_move():
    data = request.json
    board = data.get("board")
    start = data.get("start")
    print(start)
    end = data.get("end")
    piece_type = data.get("pieceType")
    if piece_type == '♙' and pawn_start_positions.get((start[0], start[1])) == 0:
        pawn_start_positions[(start[0], start[1])] = 1
        return jsonify({"valid_move": is_valid_pawn_move(start, end, True)})

    print(piece_type)
    return jsonify({"valid_move": is_valid_pawn_move(start, end, False)})




pawn_start_positions = {
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


def is_valid_pawn_move(current_position, new_position, is_first_move):
    current_row, current_col = current_position
    new_row, new_col = new_position
    if new_col == current_col and new_row == current_row + 1:
        return True
    if is_first_move and new_col == current_col and new_row == current_row + 2:
        return True
    return False
