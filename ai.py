BOARD_SIZE = 8

def is_in_check(pieces, locations, color, opponent_pieces, opponent_locations):
    try:
        king_location = locations[pieces.index('king')]
    except ValueError:
        return False  # King is not in the list, so it can't be in check
    opponent_moves = check_options(opponent_pieces, opponent_locations, 'white' if color == 'black' else 'black', pieces, locations, [False, False], [[False, False], [False, False]])
    return any(move[1] == king_location for move in opponent_moves)

def is_checkmate(pieces, locations, color, opponent_pieces, opponent_locations):
    if not is_in_check(pieces, locations, color, opponent_pieces, opponent_locations):
        return False
    for piece, location in zip(pieces, locations):
        moves = check_options([piece], [location], color, opponent_pieces, opponent_locations, [False, False], [[False, False], [False, False]])
        if moves:
            return False
    return True

def check_options(pieces, locations, color, opponent_pieces, opponent_locations, king_moved, rook_moved):
    valid_moves = []

    for piece, location in zip(pieces, locations):
        if piece == 'pawn':
            direction = -1 if color == 'white' else 1
            start_row = 6 if color == 'white' else 1
            # Move forward one square
            new_location = (location[0], location[1] + direction)
            if 0 <= new_location[1] < BOARD_SIZE and new_location not in opponent_locations and new_location not in locations:
                valid_moves.append((piece, new_location))
            # Initial move: move forward two squares
            if location[1] == start_row:
                new_location = (location[0], location[1] + 2 * direction)
                if 0 <= new_location[1] < BOARD_SIZE and (location[0], location[1] + direction) not in opponent_locations and (location[0], location[1] + direction) not in locations and new_location not in opponent_locations and new_location not in locations:
                    valid_moves.append((piece, new_location))
            # Capture moves
            for dx in [-1, 1]:
                capture_location = (location[0] + dx, location[1] + direction)
                if capture_location in opponent_locations:
                    valid_moves.append((piece, capture_location))
        elif piece == 'rook':
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                for i in range(1, BOARD_SIZE):
                    new_location = (location[0] + dx * i, location[1] + dy * i)
                    if 0 <= new_location[0] < BOARD_SIZE and 0 <= new_location[1] < BOARD_SIZE:
                        if new_location in opponent_locations or new_location in locations:
                            if new_location in opponent_locations:
                                valid_moves.append((piece, new_location))
                            break
                        valid_moves.append((piece, new_location))
                    else:
                        break
        elif piece == 'knight':
            for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                new_location = (location[0] + dx, location[1] + dy)
                if 0 <= new_location[0] < BOARD_SIZE and 0 <= new_location[1] < BOARD_SIZE:
                    if new_location not in locations:
                        valid_moves.append((piece, new_location))
                    elif new_location in opponent_locations:
                        valid_moves.append((piece, new_location))
        elif piece == 'bishop':
            for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, BOARD_SIZE):
                    new_location = (location[0] + dx * i, location[1] + dy * i)
                    if 0 <= new_location[0] < BOARD_SIZE and 0 <= new_location[1] < BOARD_SIZE:
                        if new_location in opponent_locations or new_location in locations:
                            if new_location in opponent_locations:
                                valid_moves.append((piece, new_location))
                            break
                        valid_moves.append((piece, new_location))
                    else:
                        break
        elif piece == 'queen':
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, BOARD_SIZE):
                    new_location = (location[0] + dx * i, location[1] + dy * i)
                    if 0 <= new_location[0] < BOARD_SIZE and 0 <= new_location[1] < BOARD_SIZE:
                        if new_location in opponent_locations or new_location in locations:
                            if new_location in opponent_locations:
                                valid_moves.append((piece, new_location))
                            break
                        valid_moves.append((piece, new_location))
                    else:
                        break
        elif piece == 'king':
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                new_location = (location[0] + dx, location[1] + dy)
                if 0 <= new_location[0] < BOARD_SIZE and 0 <= new_location[1] < BOARD_SIZE:
                    if new_location not in locations:
                        valid_moves.append((piece, new_location))
                    elif new_location in opponent_locations:
                        valid_moves.append((piece, new_location))
            # Castling
            if color == 'white' and not king_moved[0]:
                if not rook_moved[0][0] and all((i, 7) not in locations for i in range(1, 4)):
                    valid_moves.append((piece, (2, 7)))
                if not rook_moved[0][1] and all((i, 7) not in locations for i in range(5, 7)):
                    valid_moves.append((piece, (6, 7)))
            elif color == 'black' and not king_moved[1]:
                if not rook_moved[1][0] and all((i, 0) not in locations for i in range(1, 4)):
                    valid_moves.append((piece, (2, 0)))
                if not rook_moved[1][1] and all((i, 0) not in locations for i in range(5, 7)):
                    valid_moves.append((piece, (6, 0)))
    return valid_moves

def execute_move(pieces, locations, move, color, king_moved, rook_moved):
    piece, new_location = move
    current_location = locations[pieces.index(piece)]
    index = locations.index(current_location)
    locations[index] = new_location
    # Handle pawn promotion
    if piece == 'pawn' and (new_location[1] == 0 or new_location[1] == 7):
        pieces[index] = 'queen'  # Promote to queen for simplicity
    # Handle castling
    if piece == 'king':
        if abs(new_location[0] - current_location[0]) == 2:
            if new_location[0] == 2:  # Queen side castling
                rook_index = locations.index((0, new_location[1]))
                locations[rook_index] = (3, new_location[1])
            elif new_location[0] == 6:  # King side castling
                rook_index = locations.index((7, new_location[1]))
                locations[rook_index] = (5, new_location[1])
        if color == 'white':
            king_moved[0] = True
        else:
            king_moved[1] = True
    if piece == 'rook':
        if color == 'white':
            if current_location == (0, 7):
                rook_moved[0][0] = True
            elif current_location == (7, 7):
                rook_moved[0][1] = True
        else:
            if current_location == (0, 0):
                rook_moved[1][0] = True
            elif current_location == (7, 0):
                rook_moved[1][1] = True
    return pieces, locations

def minimax(pieces, locations, color, opponent_pieces, opponent_locations, king_moved, rook_moved, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_checkmate(pieces, locations, color, opponent_pieces, opponent_locations):
        return evaluate_board(pieces, locations, color)

    if maximizing_player:
        max_eval = -float('inf')
        for move in check_options(pieces, locations, color, opponent_pieces, opponent_locations, king_moved, rook_moved):
            new_pieces, new_locations = execute_move(pieces[:], locations[:], move, color, king_moved[:], rook_moved[:])
            eval = minimax(new_pieces, new_locations, color, opponent_pieces, opponent_locations, king_moved, rook_moved, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in check_options(opponent_pieces, opponent_locations, 'white' if color == 'black' else 'black', pieces, locations, king_moved, rook_moved):
            new_opponent_pieces, new_opponent_locations = execute_move(opponent_pieces[:], opponent_locations[:], move, 'white' if color == 'black' else 'black', king_moved[:], rook_moved[:])
            eval = minimax(pieces, locations, color, new_opponent_pieces, new_opponent_locations, king_moved, rook_moved, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def pick_best_move(pieces, locations, color, opponent_pieces, opponent_locations, king_moved, rook_moved):
    best_move = None
    best_value = -float('inf') if color == 'black' else float('inf')
    depth = 3  # Depth of the minimax algorithm

    for move in check_options(pieces, locations, color, opponent_pieces, opponent_locations, king_moved, rook_moved):
        new_pieces, new_locations = execute_move(pieces[:], locations[:], move, color, king_moved[:], rook_moved[:])
        board_value = minimax(new_pieces, new_locations, color, opponent_pieces, opponent_locations, king_moved, rook_moved, depth - 1, -float('inf'), float('inf'), False)
        if (color == 'black' and board_value > best_value) or (color == 'white' and board_value < best_value):
            best_value = board_value
            best_move = move

    return best_move
     


def evaluate_board(pieces, locations, color):
    piece_values = {
        'pawn': 1,
        'knight': 3,
        'bishop': 3,
        'rook': 5,
        'queen': 9,
        'king': 100
    }
    value = 0
    for piece, location in zip(pieces, locations):
        piece_value = piece_values.get(piece, 0)
        if color == 'black':
            value += piece_value
        else:
            value -= piece_value
    return value