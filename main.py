import random
import pygame

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 8
TILE_SIZE = 75
SCREEN_SIZE = BOARD_SIZE * TILE_SIZE
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Chess Game")

# Load and resize chess piece images
piece_images = {
    'black_pawn': pygame.transform.scale(pygame.image.load('images/b_pawn.png'), (TILE_SIZE, TILE_SIZE)),
    'black_rook': pygame.transform.scale(pygame.image.load('images/b_rook.png'), (TILE_SIZE, TILE_SIZE)),
    'black_knight': pygame.transform.scale(pygame.image.load('images/b_knight.png'), (TILE_SIZE, TILE_SIZE)),
    'black_bishop': pygame.transform.scale(pygame.image.load('images/b_bishop.png'), (TILE_SIZE, TILE_SIZE)),
    'black_queen': pygame.transform.scale(pygame.image.load('images/b_queen.png'), (TILE_SIZE, TILE_SIZE)),
    'black_king': pygame.transform.scale(pygame.image.load('images/b_king.png'), (TILE_SIZE, TILE_SIZE)),
    'white_pawn': pygame.transform.scale(pygame.image.load('images/w_pawn.png'), (TILE_SIZE, TILE_SIZE)),
    'white_rook': pygame.transform.scale(pygame.image.load('images/w_rook.png'), (TILE_SIZE, TILE_SIZE)),
    'white_knight': pygame.transform.scale(pygame.image.load('images/w_knight.png'), (TILE_SIZE, TILE_SIZE)),
    'white_bishop': pygame.transform.scale(pygame.image.load('images/w_bishop.png'), (TILE_SIZE, TILE_SIZE)),
    'white_queen': pygame.transform.scale(pygame.image.load('images/w_queen.png'), (TILE_SIZE, TILE_SIZE)),
    'white_king': pygame.transform.scale(pygame.image.load('images/w_king.png'), (TILE_SIZE, TILE_SIZE)),
}

# Initialize piece locations
black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
white_locations = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                   (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]

# Initialize piece types
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'] + ['pawn'] * 8
white_pieces = ['pawn'] * 8 + ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

# Initialize captured pieces lists
captured_pieces_white = []
captured_pieces_black = []

# Initialize game state variables
turn_step = 0
selection = 100
valid_moves = []
winner = ''  # Initialize the winner variable
game_over = False

# Track if kings and rooks have moved for castling
white_king_moved = False
black_king_moved = False
white_rook_moved = [False, False]  # [left rook, right rook]
black_rook_moved = [False, False]  # [left rook, right rook]

def is_in_check(pieces, locations, color):
    try:
        king_location = locations[pieces.index('king')]
    except ValueError:
        return False  # King is not in the list, so it can't be in check
    opponent_pieces = white_pieces if color == 'black' else black_pieces
    opponent_locations = white_locations if color == 'black' else black_locations
    opponent_moves = check_options(opponent_pieces, opponent_locations, 'white' if color == 'black' else 'black', check_check=False)
    return any(move[1] == king_location for move in opponent_moves)

def check_options(pieces, locations, color, check_check=True):
    valid_moves = []
    opponent_locations = white_locations if color == 'black' else black_locations

    for piece, location in zip(pieces, locations):
        if piece == 'pawn':
            direction = -1 if color == 'white' else 1
            start_row = 6 if color == 'white' else 1
            # Move forward one square
            new_location = (location[0], location[1] + direction)
            if 0 <= new_location[1] < BOARD_SIZE and new_location not in white_locations and new_location not in black_locations:
                valid_moves.append((piece, new_location))
            # Initial move: move forward two squares
            if location[1] == start_row:
                new_location = (location[0], location[1] + 2 * direction)
                if 0 <= new_location[1] < BOARD_SIZE and (location[0], location[1] + direction) not in white_locations and (location[0], location[1] + direction) not in black_locations and new_location not in white_locations and new_location not in black_locations:
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
                        if new_location in white_locations or new_location in black_locations:
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
                    if new_location not in white_locations and new_location not in black_locations:
                        valid_moves.append((piece, new_location))
                    elif new_location in opponent_locations:
                        valid_moves.append((piece, new_location))
        elif piece == 'bishop':
            for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, BOARD_SIZE):
                    new_location = (location[0] + dx * i, location[1] + dy * i)
                    if 0 <= new_location[0] < BOARD_SIZE and 0 <= new_location[1] < BOARD_SIZE:
                        if new_location in white_locations or new_location in black_locations:
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
                        if new_location in white_locations or new_location in black_locations:
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
                    if new_location not in white_locations and new_location not in black_locations:
                        valid_moves.append((piece, new_location))
                    elif new_location in opponent_locations:
                        valid_moves.append((piece, new_location))
            # Castling
            if color == 'white' and not white_king_moved:
                if not white_rook_moved[0] and all((i, 7) not in white_locations and (i, 7) not in black_locations for i in range(1, 4)):
                    valid_moves.append((piece, (2, 7)))  # Castling queen side
                if not white_rook_moved[1] and all((i, 7) not in white_locations and (i, 7) not in black_locations for i in range(5, 7)):
                    valid_moves.append((piece, (6, 7)))  # Castling king side
            if color == 'black' and not black_king_moved:
                if not black_rook_moved[0] and all((i, 0) not in white_locations and (i, 0) not in black_locations for i in range(1, 4)):
                    valid_moves.append((piece, (2, 0)))  # Castling queen side
                if not black_rook_moved[1] and all((i, 0) not in white_locations and (i, 0) not in black_locations for i in range(5, 7)):
                    valid_moves.append((piece, (6, 0)))  # Castling king side

    if check_check:
        valid_moves = [move for move in valid_moves if not is_in_check(pieces, [new_location if loc == location else loc for loc in locations], color)]
    return valid_moves

def pick_ai_move(valid_moves):
    # Prioritize capture moves
    capture_moves = [move for move in valid_moves if move[1] in white_locations]
    if capture_moves:
        return random.choice(capture_moves)
    
    # Prioritize advancing pawns
    pawn_moves = [move for move in valid_moves if move[0] == 'pawn']
    if pawn_moves:
        return random.choice(pawn_moves)
    
    # Otherwise, pick any valid move
    if valid_moves:
        return random.choice(valid_moves)
    
    return None

def get_click_coords(event):
    x, y = event.pos
    # Convert the x, y coordinates to the grid coordinates
    grid_x = x // TILE_SIZE
    grid_y = y // TILE_SIZE
    return (grid_x, grid_y)

def execute_move(pieces, locations, move, color):
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
            global white_king_moved
            white_king_moved = True
        else:
            global black_king_moved
            black_king_moved = True
    if piece == 'rook':
        if color == 'white':
            if current_location == (0, 7):
                white_rook_moved[0] = True
            elif current_location == (7, 7):
                white_rook_moved[1] = True
        else:
            if current_location == (0, 0):
                black_rook_moved[0] = True
            elif current_location == (7, 0):
                black_rook_moved[1] = True
    return pieces, locations

def draw_game_over(winner):
    font = pygame.font.Font(None, 74)
    text = font.render(f"{winner.capitalize()} wins!", True, RED)
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else GREY
            pygame.draw.rect(screen, color, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_pieces():
    for piece, location in zip(black_pieces, black_locations):
        piece_image = piece_images['black_' + piece]
        screen.blit(piece_image, (location[0] * TILE_SIZE, location[1] * TILE_SIZE))
    for piece, location in zip(white_pieces, white_locations):
        piece_image = piece_images['white_' + piece]
        screen.blit(piece_image, (location[0] * TILE_SIZE, location[1] * TILE_SIZE))

def is_checkmate(pieces, locations, color):
    if not is_in_check(pieces, locations, color):
        return False
    for piece, location in zip(pieces, locations):
        moves = check_options([piece], [location], color)
        if moves:
            return False
    return True

# Check options for both players
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player's move
        if turn_step % 2 == 0:  # Player's turn (assuming player is white)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_coords = get_click_coords(event)
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    valid_moves = check_options([white_pieces[selection]], [click_coords], 'white')
                elif click_coords in [move[1] for move in valid_moves] and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step += 1
                    selection = 100
                    valid_moves = []

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                # Handle game over state
                pass

    if winner != '':
        game_over = True
        draw_game_over(winner)
        running = False
        continue

    if turn_step % 2 == 1:  # AI's turn (assuming AI is black)
        ai_move = pick_ai_move(black_options)
        if ai_move:
            black_pieces, black_locations = execute_move(black_pieces, black_locations, ai_move, 'black')
            black_options = check_options(black_pieces, black_locations, 'black')
            white_options = check_options(white_pieces, white_locations, 'white')
            turn_step += 1

    # Check for checkmate
    if is_checkmate(white_pieces, white_locations, 'white'):
        winner = 'black'
    elif is_checkmate(black_pieces, black_locations, 'black'):
        winner = 'white'

    # Draw the board and pieces
    draw_board()
    draw_pieces()
    pygame.display.flip()

pygame.quit()