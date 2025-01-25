# Importing Modules
import pygame
import requests
import rembg
from io import BytesIO

# Initialising pygame module
pygame.init()

# Setting Width and height of the Chess Game screen
WIDTH = 1000
HEIGHT = 900

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess Game')

font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

timer = pygame.time.Clock()
fps = 60

# ChessBoard class
class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.king_positions = {'K': (7, 4), 'k': (0, 4)}

    def is_check(self, color):
        king_pos = self.king_positions['K'] if color == 'white' else self.king_positions['k']
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and (piece.islower() if color == 'white' else piece.isupper()):
                    if self.is_threat(king_pos, (row, col), piece):
                        return True
        return False

    def is_threat(self, king_pos, attacker_pos, piece):
        directions = {
            'r': [(1, 0), (-1, 0), (0, 1), (0, -1)],
            'b': [(1, 1), (-1, -1), (1, -1), (-1, 1)],
            'q': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)],
            'n': [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)],
            'p': [(-1, -1), (-1, 1)] if piece.isupper() else [(1, -1), (1, 1)]
        }
        # For a knight (n), check if the king is one move away
        if piece.lower() == 'n':
            row_diff = abs(king_pos[0] - attacker_pos[0])
            col_diff = abs(king_pos[1] - attacker_pos[1])
            return row_diff == 2 and col_diff == 1 or row_diff == 1 and col_diff == 2

        for direction in directions.get(piece.lower(), []):
            r, c = attacker_pos
            while 0 <= r < 8 and 0 <= c < 8:
                r, c = r + direction[0], c + direction[1]
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] != '.':
                        if (r, c) == king_pos:
                            return True
                        break
        return False

    def is_checkmate(self, color):
        if not self.is_check(color):
            return False

        king_pos = self.king_positions['K'] if color == 'white' else self.king_positions['k']
        for row in range(8):
            for col in range(8):
                if (self.board[row][col] == 'K' if color == 'white' else self.board[row][col] == 'k'):
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            new_row, new_col = row + dx, col + dy
                            if 0 <= new_row < 8 and 0 <= new_col < 8:
                                if self.board[new_row][new_col] == '.':
                                    self.board[row][col] = '.'
                                    self.board[new_row][new_col] = 'K' if color == 'white' else 'k'
                                    if not self.is_check(color):
                                        return False
                                    self.board[new_row][new_col] = '.'
                                    self.board[row][col] = 'K' if color == 'white' else 'k'
        return True

# Initialize the chess board
chess_board = ChessBoard()

# url for chess pieces images
image_urls = ['https://media.geeksforgeeks.org/wp-content/uploads/20240302025946/black_queen.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025948/black_king.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025345/black_rook.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025951/black_bishop.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025947/black_knight.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025945/black_pawn.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025952/white_queen.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025943/white_king.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025949/white_rook.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025944/white_bishop.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025325/white_knight.png',
              'https://media.geeksforgeeks.org/wp-content/uploads/20240302025953/white_pawn.png']

# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[0]).content)))
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[1]).content)))
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[2]).content)))
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[3]).content)))
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[4]).content)))
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[5]).content)))
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[6]).content)))
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[7]).content)))
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[8]).content)))
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[9]).content)))
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[10]).content)))
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load(
    BytesIO(rembg.remove(requests.get(image_urls[11]).content)))
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king,
                white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king,
                black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small,
                      black_knight_small, black_rook_small, black_bishop_small]
piece_list = ['p', 'r', 'n', 'b', 'q', 'k']


# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
turn_step = 0  # Initialize turn_step

# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [
                             600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [
                             700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(
            status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))

# draw pieces onto board
def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = chess_board.board[row][col]
            if piece != '.':
                if piece.isupper():
                    index = piece_list.index(piece.lower())
                    screen.blit(white_images[index], (col * 100 + 10, row * 100 + 10))
                else:
                    index = piece_list.index(piece)
                    screen.blit(black_images[index], (col * 100 + 10, row * 100 + 10))

# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for move in moves:
        pygame.draw.circle(screen, color, (move[1] * 100 + 50, move[0] * 100 + 50), 5)

# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))

# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if chess_board.is_check('white'):
            king_pos = chess_board.king_positions['K']
            if counter < 15:
                pygame.draw.rect(screen, 'dark red', [king_pos[1] * 100 + 1, king_pos[0] * 100 + 1, 100, 100], 5)
    else:
        if chess_board.is_check('black'):
            king_pos = chess_board.king_positions['k']
            if counter < 15:
                pygame.draw.rect(screen, 'dark blue', [king_pos[1] * 100 + 1, king_pos[0] * 100 + 1, 100, 100], 5)

def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(
        f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!',
                            True, 'white'), (210, 240))

# main game loop
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (y_coord, x_coord)
            # Handle piece selection and movement logic here
            # Example: if a piece is selected, move it to the clicked position
            # You need to implement the logic for selecting and moving pieces

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                chess_board = ChessBoard()
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []

    if chess_board.is_checkmate('black'):
        winner = 'white'
        game_over = True
    elif chess_board.is_checkmate('white'):
        winner = 'black'
        game_over = True

    if winner != '':
        draw_game_over()

    pygame.display.flip()

pygame.quit()