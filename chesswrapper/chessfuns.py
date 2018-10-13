import re

coordinate_rx = re.compile(r'\A[a-h][1-8]\Z')

class ChessFnError(Exception):
    """Errors raised by chess functions."""
    def __init__(self, message):
        self.message = message

def is_int(x):
    """Returns True is x is a representation of an integer, False otherwise."""
    if isinstance(x, int):
        return True
    if not isinstance(x, str):
        return False
    try:
        int(x)
    except Exception:
        return False
    return True

def is_chess_int(x):
    """Returns True if x is a representation of an integer between
    1 and 8, False otherwise.
    """
    if not is_int(x):
        return False
    if int(x) >= 1 and int(x) <= 8:
        return True
    return False

def is_coordinate(square):
    """Returns True if square is a valid square coordinate."""
    if coordinate_rx.match(square):
        return True
    return False

def square_to_coords(square):
    """Returns the coordinates (1-indexed) corresponding to square, a string
    representing a square on a chess board.
    For example, h5 returns (5, 8)
    """
    if not isinstance(square, str) or not len(square) == 2:
        try:
            err_msg = str(square) + " is not a valid square!"
        except Exception:
            err_msg = "Not a valid square (no string definition)!"
        raise ChessFnError(err_msg)
    if not coordinate_rx.match(square):
        raise ChessFnError("{} is not a proper square!".format(square))
    return (
        int(square[1]),
        ord(square[0]) - ord('a') + 1
    )

def coords_to_square(r, f):
    """Returns the square corresponding to coordinates (r, f)"""
    if not is_chess_int(r) or not is_chess_int(f):
        raise ChessFnError("Invalid coordinates specified!")
    return chr(ord('a') + f - 1) + str(r)

def piece_can_move(piece, r1, f1, r2, f2, is_capture):
    """Checks if a piece can move from (r1, f1) to (r2, f2). Only considers
    piece type, does not consider whether or not square is reachable.
    """
    fdiff = abs(f1 - f2)
    if piece.lower() == 'p':
        dir = -1 if piece == 'p' else 1
        if is_capture:
            if r2 - r1 == dir and fdiff == 1:
                return True
        elif fdiff == 0:
            if r2 - r1 == dir:
                return True
            if dir == 1:
                if r1 == 2 and r2 == 4:
                    return True
            else:
                if r1 == 7 and r2 == 5:
                    return True
        return False
    rdiff = abs(r1 - r2)
    if piece.lower() == 'k':
        if rdiff <= 1 and fdiff <= 1:
            return True
        return False
    if piece.lower() == 'q':
        if rdiff == 0 or fdiff == 0:
            return True
        if rdiff == fdiff:
            return True
        return False
    if piece.lower() == 'b':
        if rdiff == fdiff:
            return True
    if piece.lower() == 'n':
        if rdiff == 2 and fdiff == 1:
            return True
        if rdiff == 1 and fdiff == 2:
            return True
        return False
    if piece.lower() == 'r':
        if rdiff == 0 or fdiff == 0:
            return True
    return False
