import chessfuns

valid_pieces = ['p', 'n', 'b', 'r', 'q', 'k']
valid_castling = ['k', 'q']

class ChessBoardError(Exception):
    """Errors raised by ChessGame."""
    def __init__(self, message):
        self.message = message

class ChessBoard:
    def __init__(self, fen = None):
        """Initialize an 8x8 chess board from a FEN string, or as the default
        starting position if no FEN is provided.
        """
        # initialize board to 8x8 array of None
        self.board = []
        for _ in range(8):
            self.board.append([None] * 8)

        if fen is not None:
            self.initialize_from_fen(fen)
        else:
            # use default starting position
            self.initialize_from_fen(
                'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            )

    def __str__(self):
        """Return an ascii representation of current position."""
        result = ('White to move\n' if self.white_to_move 
                  else 'Black to move\n')
        for rank in reversed(self.board):
            for piece in rank:
                if piece is None:
                    result += '  '
                else:
                    result += piece + ' '
            result += '\n'
        return result

    def add_piece(self, piece, r = None, f = None, square = None):
        """Adds piece (either by coordinates f and r, or by square) to self."""
        if square is not None:
            (r, f) = chessfuns.square_to_coords(square)
        elif f is None or r is None:
            raise ChessBoardError("Coordinates for piece not defined!")
        self.board[r-1][f-1] = piece

    def initialize_from_fen(self, fen):
        """Takes a FEN string and initializes self to match it."""
        fen_fields = fen.split(' ')
        if not len(fen_fields) == 6:
            raise ChessBoardError("FEN has wrong number of fields!")

        # interpret board position
        ranks = fen_fields[0].split('/')
        if not len(ranks) == 8:
            raise ChessBoardError("FEN is improperly formatted!")
        for (r, rank) in enumerate(ranks):
            f = 1
            for ch in rank:
                if f > 8:
                    raise ChessBoardError("Too many squares specified in FEN at"
                                     " rank {}!".format(8 - r))
                if ch.lower() in valid_pieces:
                    self.add_piece(ch, r = 8 - r, f = f)
                    f += 1
                elif chessfuns.is_chess_int(ch):
                    f += int(ch)
                else:
                    raise ChessBoardError("Invalid FEN character found!")

        # interpret active colour
        if fen_fields[1] == 'w':
            self.white_to_move = True
        elif fen_fields[1] == 'b':
            self.white_to_move = False
        else:
            raise ChessBoardError("Active colour is invalid!")
        
        # interpret castling
        self.can_castle = []
        if fen_fields[2] != '-':
            for castling in fen_fields[2]:
                if not castling.lower() in valid_castling:
                    raise ChessBoardError("Castling is invalid!")
                self.can_castle.append(castling)

        # interpret en passant
        if not fen_fields[3] == '-' and \
           not chessfuns.is_coordinate(fen_fields[3]):
            raise ChessBoardError("En passant square value is not valid!")
        self.en_passant = fen_fields[3]

        # interpret halfmove clock
        if not chessfuns.is_int(fen_fields[4]):
            raise ChessBoardError("Halfmove clock is not valid!")
        self.halfmove_clock = int(fen_fields[4])

        # interpret move number
        if not chessfuns.is_int(fen_fields[5]):
            raise ChessBoardError("Move number is not valid!")
        self.move_number = int(fen_fields[5])

    def play_move(self, move):
        return

    def export_fen(self):
        """Returns current board (and metadata) as FEN string."""
        fen = ''
        for rank in reversed(self.board):
            if len(fen) > 0:
                fen += '/'
            empty_squares = 0
            for piece in rank:
                if piece is None:
                    empty_squares += 1
                    continue
                if empty_squares > 0:
                    fen += str(empty_squares)
                    empty_squares = 0
                fen += piece
            if empty_squares > 0:
                fen += str(empty_squares)
        fen += (' w' if self.white_to_move else ' b')
        fen += ' ' + ''.join(self.can_castle)
        fen += ' ' + self.en_passant
        fen += ' ' + str(self.halfmove_clock)
        fen += ' ' + str(self.move_number)
        return fen
