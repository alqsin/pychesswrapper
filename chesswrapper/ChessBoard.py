import chessfuns
from PieceHolder import PieceHolder

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
        # initialize emtpy PieceHolder
        self.pieces = PieceHolder()

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
        for rank in reversed(self.pieces.get_board_layout()):
            for piece in rank:
                if piece is None:
                    result += '  '
                else:
                    result += piece + ' '
            result += '\n'
        return result

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
                    raise ChessBoardError("Too many squares specified in FEN"
                                     " at rank {}!".format(8 - r))
                if chessfuns.is_chess_int(ch):
                    f += int(ch)
                else:
                    self.pieces.add_piece(ch, r = 8 - r, f = f)
                    f += 1

        # interpret active colour
        if fen_fields[1] == 'w':
            self.white_to_move = True
        elif fen_fields[1] == 'b':
            self.white_to_move = False
        else:
            raise ChessBoardError("Active colour is invalid!")
        
        # interpret castling
        self.can_castle = {
            'K': False,
            'Q': False,
            'k': False,
            'q': False,
        }
        if fen_fields[2] != '-':
            for castling in fen_fields[2]:
                if not castling.lower() in valid_castling:
                    raise ChessBoardError("Castling is invalid!")
                self.can_castle[castling] = True

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

    def play_move(self, piece, square, is_capture):
        """Plays piece to square. Uses turn status to determine which
        color to move.
        """
        # record numeric coordinates
        (r, f) = chessfuns.square_to_coords(square)

        if self.white_to_move:
            piece = piece.upper()
        else:
            piece = piece.lower()

        # move piece and record square moved from
        from_square = self.pieces.move_piece(piece, square)

        # adjust castling privileges
        if piece == 'k':
            self.can_castle['k'] = self.can_castle['q'] = False
        elif piece == 'K':
            self.can_castle['K'] = self.can_castle['Q'] = False
        elif piece == 'r':
            if from_square == 'a8':
                self.can_castle['q'] = False
            elif from_square == 'h8':
                self.can_castle['k'] = False
        elif piece == 'R':
            if from_square == 'a1':
                self.can_castle['Q'] = False
            elif from_square == 'h1':
                self.can_castle['K'] = False

        # adjust en passant square
        if piece == 'P':
            if r == 4 and from_square.r == 2:
                self.en_passant = chessfuns.coords_to_square(3, f)
        elif piece == 'p':
            if r == 5 and from_square.r == 7:
                self.en_passant = chessfuns.coords_to_square(6, f)
        else:
            self.en_passant = '-'

        # adjust halfmove clock
        if is_capture or piece.lower() == 'p':
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # adjust move number
        if not self.white_to_move:
            self.move_number += 1

        # adjust turn
        self.white_to_move = not self.white_to_move


    def export_fen(self):
        """Returns current board (and metadata) as FEN string."""
        fen = ''
        for rank in reversed(self.pieces.get_board_layout()):
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
