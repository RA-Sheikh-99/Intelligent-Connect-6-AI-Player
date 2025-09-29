import pygame
import sys
from boardsize import get_user_number

BOARD_SIZE = int(get_user_number())   
CELL_SIZE = 30         
MARGIN = 40             
WIN_CONDITION = 6       
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE + 2 * MARGIN + 40 
FPS = 60               
PLAYER1 = 1             
PLAYER2 = 2           

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)        
GRAY = (200, 200, 200)   
RED = (255, 100, 100)    
BLUE = (100, 100, 255)   

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Intelligent Connect 6 player")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

board = []
for y in range(BOARD_SIZE):
    board.append([0] * BOARD_SIZE)  # Initialize empty board

current_player = PLAYER1
move_buffer = []     # Store stones placed during a turn
game_over = False
first_turn = True    # flag for first turn

def draw_board(): # Draw the entire board and stones
    screen.fill(WHITE)

    # Show current player or winner
    if game_over:
        text = font.render("Player " + str(current_player) + " Wins!", True, BLACK)
    else:
        text = font.render("Player " + str(current_player) + "'s Turn", True, BLACK)
    screen.blit(text, (10, 5))

    offset = 40  # Extra top space for text

    # Draw board grid
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (MARGIN, MARGIN + i * CELL_SIZE + offset), (WINDOW_SIZE - MARGIN, MARGIN + i * CELL_SIZE + offset))
        pygame.draw.line(screen, BLACK, (MARGIN + i * CELL_SIZE, MARGIN + offset), (MARGIN + i * CELL_SIZE, WINDOW_SIZE - MARGIN))

    # Draw stones
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == PLAYER1:
                pygame.draw.circle(screen, RED, to_pixel(x, y), CELL_SIZE // 2 - 2)
            elif board[y][x] == PLAYER2:
                pygame.draw.circle(screen, BLUE, to_pixel(x, y), CELL_SIZE // 2 - 2)

    pygame.display.flip()

def to_pixel(x, y): # Convert grid coordinates to pixel coordinates
    return (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE + 40)


def to_grid(pos): # Convert pixel coordinates to grid position
    x, y = pos
    y = y - 40 
    gx = (x - MARGIN + CELL_SIZE // 2) // CELL_SIZE
    gy = (y - MARGIN + CELL_SIZE // 2) // CELL_SIZE

    if gx >= 0 and gx < BOARD_SIZE and gy >= 0 and gy < BOARD_SIZE:
        return (gx, gy)
    else:
        return None


def is_valid(x, y): # Check if move is valid
    if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE:
        if board[y][x] == 0:
            return True
    return False

def check_win(player): # Check if a player has won
    def count(x, y, dx, dy):
        total = 0
        for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
            nx = x + i * dx
            ny = y + i * dy
            if nx >= 0 and nx < BOARD_SIZE and ny >= 0 and ny < BOARD_SIZE:
                if board[ny][nx] == player:
                    total += 1
                    if total >= WIN_CONDITION:
                        return True
                else:
                    total = 0
        return False

    for y in range(BOARD_SIZE): # Check all cells for possible win directions
        for x in range(BOARD_SIZE):
            if board[y][x] == player:
                if count(x, y, 1, 0) or count(x, y, 0, 1) or count(x, y, 1, 1) or count(x, y, 1, -1):
                    return True
    return False

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate_board2(board)

    moves = get_possible_moves(board)[:10] # Limit moves for performance

    if maximizing:
        max_eval = -999999
        for move in moves:
            make_move(board, move, PLAYER2)
            eval = minimax(board, depth-1, alpha, beta, False)
            undo_move(board, move)
            if eval > max_eval:
                max_eval = eval
            if eval > alpha:
                alpha = eval
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 999999
        for move in moves:
            make_move(board, move, PLAYER1)
            eval = minimax(board, depth-1, alpha, beta, True)
            undo_move(board, move)
            if eval < min_eval:
                min_eval = eval
            if eval < beta:
                beta = eval
            if beta <= alpha:
                break
        return min_eval

def evaluate_board2(board): # Evalution function 2
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == PLAYER2:
                score += evaluate_position2(board, x, y, PLAYER2)
            elif board[y][x] == PLAYER1:
                score -= evaluate_position2(board, x, y, PLAYER1)
    return score

def evaluate_position2(board, x, y, player): # Evaluate score from a specific position
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        score += advanced_count_line(board, x, y, dx, dy, player)
    return score

def advanced_count_line(board, x, y, dx, dy, player): # Count consecutive stones and reward long sequence
    max_streak = 0
    streak = 0

    for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
        nx = x + i * dx
        ny = y + i * dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[ny][nx] == player:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
    return max_streak ** 2

def get_possible_moves(board):
    moves = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                moves.append((x, y))
    return moves

# Place a stone
def make_move(board, move, player):
    x, y = move
    board[y][x] = player

def undo_move(board, move):
    x, y = move
    board[y][x] = 0

while True:
    clock.tick(FPS)
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            continue

        if event.type == pygame.MOUSEBUTTONDOWN and current_player == PLAYER1: # Human player turn
            pos = pygame.mouse.get_pos()
            grid = to_grid(pos)
            if grid != None:
                x, y = grid
                if is_valid(x, y):
                    board[y][x] = PLAYER1
                    move_buffer.append((x, y))

                    if first_turn:
                        stones_needed = 1
                    else:
                        stones_needed = 2

                    if len(move_buffer) == stones_needed:
                        if check_win(current_player):
                            print("Player " + str(current_player) + " wins!")
                            game_over = True
                            continue

                        move_buffer = []
                        if current_player == PLAYER1:
                            current_player = PLAYER2
                        else:
                            current_player = PLAYER1

                        if first_turn:
                            first_turn = False

    
        if current_player == PLAYER2 and not game_over: # ai player turn
            best_move = None
            best_value = -999999

            for move in get_possible_moves(board):    # Evaluate all possible moves
                make_move(board, move, PLAYER2)
                value = minimax(board, 1, -999999, 999999, False)
                undo_move(board, move)

                if value > best_value:
                    best_value = value
                    best_move = move

            if best_move:  # Make the best move found
                make_move(board, best_move, PLAYER2)
                move_buffer.append(best_move)

                if first_turn:
                    stones_needed = 1
                else:
                    stones_needed = 2

                if len(move_buffer) == stones_needed:
                    if check_win(current_player):
                        print("Player " + str(current_player) + " wins!")
                        game_over = True
                        continue

                    move_buffer = []
                    if current_player == PLAYER1:
                        current_player = PLAYER2
                    else:
                        current_player = PLAYER1

                    if first_turn:
                        first_turn = False
