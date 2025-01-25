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

def check_options(pieces, locations, color):
    valid_moves = []
    opponent_locations = white_locations if color == 'black' else black_locations

    for piece, location in zip(pieces, locations):
        if piece == 'pawn':
            direction = -1 if color == 'white' else 1
            new_location = (location[0], location[1] + direction)
            if 0 <= new_location[1] < BOARD_SIZE and new_location not in white_locations and new_location not in black_locations:
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
    return valid_moves

def pick_random_move(valid_moves):
    if valid_moves:
        return random.choice(valid_moves)
    return None

def get_click_coords(event):
    x, y = event.pos
    # Convert the x, y coordinates to the grid coordinates
    grid_x = x // TILE_SIZE
    grid_y = y // TILE_SIZE
    return (grid_x, grid_y)

def execute_move(pieces, locations, move):
    piece, new_location = move
    current_location = locations[pieces.index(piece)]
    index = locations.index(current_location)
    locations[index] = new_location
    return pieces, locations

def draw_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
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
        draw_game_over()
        running = False
        continue

    if turn_step % 2 == 1:  # AI's turn (assuming AI is black)
        ai_move = pick_random_move(black_options)
        if ai_move:
            black_pieces, black_locations = execute_move(black_pieces, black_locations, ai_move)
            black_options = check_options(black_pieces, black_locations, 'black')
            white_options = check_options(white_pieces, white_locations, 'white')
            turn_step += 1

    # Draw the board and pieces
    draw_board()
    draw_pieces()
    pygame.display.flip()

pygame.quit()