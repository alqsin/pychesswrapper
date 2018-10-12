import chessfuns

valid_pieces = ['p', 'n', 'b', 'r', 'q', 'k']

class ChessPieceError(Exception):
    """Errors raised by PieceHolder."""
    def __init__(self, message):
        self.message = message

class Coordinate:
    def __init__(self, r, f):
        self.r = r
        self.f = f

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.r == other.r and self.f == other.f
        elif isinstance(other, str):
            return other == chessfuns.coords_to_square(self.r, self.f)
        else:
            raise ChessPieceError("Invalid coordinate comparison!")

    def copy(self):
        return Coordinate(self.r, self.f)

class PieceHolder:
    def __init__(self):
        all_pieces = valid_pieces + [piece.upper() for piece in valid_pieces]
        self.pieces = {piece : [] for piece in all_pieces}

        self.board = []
        for _ in range(8):
            self.board.append([None]  * 8)
    
    def add_piece(self, piece, r = None, f = None, square = None):
        """Adds piece (either by coordinates f and r, or by square) to self."""
        if square is not None:
            (r, f) = chessfuns.square_to_coords(square)
        elif f is None or r is None:
            raise ChessPieceError("Coordinates for piece not defined!")

        if not isinstance(piece, str) or not piece.lower() in valid_pieces:
            raise ChessPieceError("Invalid piece specified!")

        self.pieces[piece].append(Coordinate(r, f))
        self.board[r - 1][f - 1] = piece

    def move_piece(self, piece, square):
        """Moves piece to square, performing capture if necessary."""
        (r, f) = chessfuns.square_to_coords(square)
        capture = self.board[r - 1][f - 1]

        # try to find piece being moved
        from_square = None
        for coord in self[piece]:
            if chessfuns.piece_can_move(piece, coord.r, coord.f, r, f,
                                        False if capture is None else True):
                # record previous square and replace piece coordinates
                from_square = coord.copy()
                coord.r = r
                coord.f = f
                break
        if from_square is None:
            raise ChessPieceError("Could not find valid piece to move!")

        # move current piece
        self.board[from_square.r - 1][from_square.f - 1] = None
        self.board[r - 1][f - 1] = piece

        # remove captured piece
        if capture is not None:
            self[capture].pop(self[capture].index(Coordinate(r, f)))

        return from_square

    def __getitem__(self, piece):
        return self.pieces[piece]

    def get_board_layout(self):
        return self.board
