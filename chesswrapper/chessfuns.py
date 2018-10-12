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
