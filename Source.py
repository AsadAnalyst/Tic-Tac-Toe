import numpy as np
import pygame
import time

pygame.init()
WIDTH, HEIGHT = 600, 650
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 4, 4
CELL_SIZE = WIDTH // BOARD_COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class TicTacToe:
    def __init__(self, use_alpha_beta, ai_first):
        self.board = np.full((4, 4), '-')
        self.current_player = 'O' if ai_first else 'X'
        self.ai_player = 'O'
        self.human_player = 'X'
        self.use_alpha_beta = use_alpha_beta
        self.game_over = False
        self.nodes_expanded = 0

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe 4x4")
        self.window.fill(WHITE)
        self.draw_grid()
        pygame.display.update()

        if ai_first:
            self.ai_move()

    def draw_grid(self):
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(self.window, BLACK, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), LINE_WIDTH)
        for col in range(1, BOARD_COLS):
            pygame.draw.line(self.window, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT - 50), LINE_WIDTH)
        pygame.display.update()

    def draw_move(self, row, col):
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        if self.board[row, col] == 'X':
            pygame.draw.line(self.window, RED, (center_x - 30, center_y - 30), (center_x + 30, center_y + 30),
                             LINE_WIDTH)
            pygame.draw.line(self.window, RED, (center_x + 30, center_y - 30), (center_x - 30, center_y + 30),
                             LINE_WIDTH)
        else:
            pygame.draw.circle(self.window, BLUE, (center_x, center_y), 30, LINE_WIDTH)
        pygame.display.update()

    def make_move(self, row, col):
        if self.board[row, col] == '-' and not self.game_over:
            self.board[row, col] = self.current_player
            self.draw_move(row, col)
            if self.is_winner(self.current_player):
                print(f"{self.current_player} wins!")
                self.game_over = True
            elif self.is_board_full():
                print("Game Draw!")
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == self.ai_player:
                    self.ai_move()

    def is_winner(self, player):
        for row in range(4):
            if all(self.board[row, col] == player for col in range(4)):
                return True
        for col in range(4):
            if all(self.board[row, col] == player for row in range(4)):
                return True
        if all(self.board[i, i] == player for i in range(4)) or all(self.board[i, 3 - i] == player for i in range(4)):
            return True
        return False

    def is_board_full(self):
        return '-' not in self.board

    def ai_move(self):
        if self.game_over:
            return

        print(f"AI ({self.ai_player}) is thinking...")
        start_time = time.time()

        if self.use_alpha_beta:
            _, move = self.minimax_alpha_beta(self.board, 4, float('-inf'), float('inf'), True)
        else:
            _, move = self.minimax(self.board, 4, True)

        end_time = time.time()
        print(f"AI thinking time: {round(end_time - start_time, 3)} seconds")

        if move:
            row, col = move
            self.make_move(row, col)
        else:
            print("AI could not find a move! Board state:")
            print(self.board)

    def minimax(self, board, depth, is_maximizing):
        if self.is_winner('O'):
            return 10, None
        if self.is_winner('X'):
            return -10, None
        if self.is_board_full() or depth == 0:
            return 0, None

        best_score = float('-inf') if is_maximizing else float('inf')
        best_move = None
        for row in range(4):
            for col in range(4):
                if board[row, col] == '-':
                    board[row, col] = 'O' if is_maximizing else 'X'
                    score, _ = self.minimax(board, depth - 1, not is_maximizing)
                    board[row, col] = '-'
                    if (is_maximizing and score > best_score) or (not is_maximizing and score < best_score):
                        best_score = score
                        best_move = (row, col)
        return best_score, best_move

    def minimax_alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        if self.is_winner('O'):
            return 10, None
        if self.is_winner('X'):
            return -10, None
        if self.is_board_full() or depth == 0:
            return 0, None

        best_move = None
        for row in range(4):
            for col in range(4):
                if board[row, col] == '-':
                    board[row, col] = 'O' if is_maximizing else 'X'
                    score, _ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, not is_maximizing)
                    board[row, col] = '-'
                    if is_maximizing:
                        if score > alpha:
                            alpha = score
                            best_move = (row, col)
                        if alpha >= beta:
                            break
                    else:
                        if score < beta:
                            beta = score
                            best_move = (row, col)
                        if alpha >= beta:
                            break
        return alpha if is_maximizing else beta, best_move


if __name__ == "__main__":
    use_alpha_beta = input("Use Alpha-Beta Pruning? (yes/no): ").strip().lower() == 'yes'
    ai_first = input("Should AI play first? (yes/no): ").strip().lower() == 'yes'
    game = TicTacToe(use_alpha_beta, ai_first)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if game.current_player == game.human_player:
                    game.make_move(row, col)
    pygame.quit()
