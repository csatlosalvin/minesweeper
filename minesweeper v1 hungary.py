import pygame
import random
import sys

# Pygame inicializálása
pygame.init()

# Színek
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (105, 105, 105)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Ablak mérete
WIDTH, HEIGHT = 300, 350  # Csökkentett ablakméret az újraindítási gombhoz
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Aknák száma
MINES_COUNT = 10

# Ablak létrehozása
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aknakereső")

# Betűtípus inicializálása
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)

# Táblázat létrehozása és aknák elhelyezése
def create_board():
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    mines = set()
    while len(mines) < MINES_COUNT:
        mine = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        mines.add(mine)
    
    for (i, j) in mines:
        board[i][j] = 'M'
        for x in range(max(0, i-1), min(ROWS, i+2)):
            for y in range(max(0, j-1), min(COLS, j+2)):
                if board[x][y] != 'M':
                    board[x][y] += 1
    return board

# Tábla rajzolása
def draw_board(board, revealed, flagged):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            if revealed[row][col]:
                pygame.draw.rect(screen, WHITE, rect)
                if board[row][col] == 'M':
                    pygame.draw.circle(screen, BLACK, rect.center, SQUARE_SIZE // 4)
                elif board[row][col] > 0:
                    text = FONT.render(str(board[row][col]), True, BLACK)
                    screen.blit(text, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 5))
            else:
                pygame.draw.rect(screen, GRAY, rect)
                if flagged[row][col]:
                    pygame.draw.circle(screen, RED, rect.center, SQUARE_SIZE // 4)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Szomszédos mezők felfedése
def reveal(board, revealed, row, col):
    if revealed[row][col]:
        return
    revealed[row][col] = True
    if board[row][col] == 0:
        for x in range(max(0, row-1), min(ROWS, row+2)):
            for y in range(max(0, col-1), min(COLS, col+2)):
                if not revealed[x][y]:
                    reveal(board, revealed, x, y)

# Újraindítási gomb rajzolása
def draw_restart_button():
    rect = pygame.Rect(100, 310, 100, 30)
    pygame.draw.rect(screen, GREEN, rect)
    text = FONT.render("Újraindítás", True, BLACK)
    screen.blit(text, (110, 315))

# Fő függvény
def main():
    board = create_board()
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // SQUARE_SIZE
                col = mouse_pos[0] // SQUARE_SIZE

                if 100 <= mouse_pos[0] <= 200 and 310 <= mouse_pos[1] <= 340:
                    # Újraindítási gomb kezelése
                    board = create_board()
                    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
                    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
                    game_over = False
                elif not game_over:
                    if event.button == 1:  # Bal egérgomb
                        if not flagged[row][col]:
                            if board[row][col] == 'M':
                                game_over = True
                                for r in range(ROWS):
                                    for c in range(COLS):
                                        revealed[r][c] = True
                            else:
                                reveal(board, revealed, row, col)
                    elif event.button == 3:  # Jobb egérgomb
                        flagged[row][col] = not flagged[row][col]

        screen.fill(DARK_GRAY)
        draw_board(board, revealed, flagged)
        draw_restart_button()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
