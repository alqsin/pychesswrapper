import re

class PGNError(Exception):
    """Errors related to reading PGN format."""
    def __init__(self, message):
        self.message = message

def parse_pgn(pgn):
    """Take pgn, a string representing a chess game in PGN format, and
    return a dict of tags as well as a list of moves played.
    """
    if not isinstance(pgn, str):
        raise PGNError("PGN input must be a string!")

    tags = {}
    moves = []

    # look for tags
    tag_rx = re.compile(r'\s*\[\s*(\w+)\s*\"([^"]+)\"\s*\]\s*')
    i = 0
    while True:
        tag_match = tag_rx.search(pgn, i)
        if tag_match is None:
            break
        tags[tag_match.group(1)] = tag_match.group(2)
        i = tag_match.end()  # gets the next char after end of match

    # check that remainder of PGN is algebraic notation
    pgn = pgn[i:].lstrip()
    if not pgn.startswith('1.'):
        raise PGNError("Error parsing PGN: could not find algebraic notation"
                        " section!")

    # remove comments from algebraic notation
    comment_rx = [
        re.compile(r'\{[^}]*\}'),  # comments in brackets
        re.compile(r';.*'),  # comments after ;
    ]

    for rx in comment_rx:
        pgn = rx.sub('', pgn)

    # find moves
    move_rx_list = [
        r'\bO\-O\b',
        r'\bO\-O\-O\b',
        r'\b[KQRBN]?[a-h|1-8]?[xX]?[a-h][1-8][+#]?\b',
    ]
    move_rx = re.compile('|'.join(move_rx_list))

    curr_move = 1
    while True:
        curr_move_pos = pgn.find(str(curr_move) + '.')
        if curr_move_pos == -1:
            break
        next_move_pos = pgn.find(str(curr_move + 1) + '.')
        for _ in range(2):
            move = move_rx.search(
                pgn,
                curr_move_pos,
                next_move_pos if next_move_pos != -1 else len(pgn)
            )
            if move is None:
                if next_move_pos == -1:
                    break
                raise PGNError("Error parsing PGN: could not find notation"
                               " at move {}!".format(curr_move))
            moves.append(move.group(0))
            curr_move_pos = move.end() + 1
        curr_move += 1

    return (tags, moves)
