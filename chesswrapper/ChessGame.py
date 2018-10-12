import pgnlyzer
import re

class ChessError(Exception):
    """Errors raised by ChessGame."""
    def __init__(self, message):
        self.message = message

class ChessGame:
    def __init__(self, pgn = None):
        """Initialize a ChessGame either as an empty game (no moves played)
        or with pgn, a text string representing a game using pgn notation.
        """
        if pgn is None:
            self.tags = {}
            self.moves = []
            return
        try:
            (self.tags, self.moves) = pgnlyzer.parse_pgn(pgn)
        except pgnlyzer.PGNError as e:
            raise
        except Exception as e:
            raise ChessError("Some error occurred while trying to read PGN:\n"
                             + str(e))
