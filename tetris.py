import pygame
import random

# Init pygame
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_SIZE = 25
COLUMNS = 10
ROWS = 20
PLAY_WIDTH = COLUMNS * GRID_SIZE
PLAY_HEIGHT = ROWS * GRID_SIZE

# Renkler (Neon)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

SHAPE_COLORS = [CYAN, MAGENTA, YELLOW, GREEN, ORANGE, BLUE, RED]

# Şekıller
S = [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '...O.',
      '.....']]

Z = [['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '.O...',
      '.....']]

I = [['..O..',
      '..O..',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      'OOOO.',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.OO..',
      '.OO..',
      '.....']]

J = [['.....',
      '.O...',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..OO.',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '...O.',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....']]

L = [['.....',
      '...O.',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '..OO.',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '.O...',
      '.....'],
     ['.....',
      '.OO..',
      '..O..',
      '..O..',
      '.....']]

T = [['.....',
      '..O..',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLUMNS):
            if (x, y) in locked_pos:
                grid[y][x] = locked_pos[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(COLUMNS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

def clear_rows(grid, locked):
    full_rows = []
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            full_rows.append(i)
            for j in range(len(row)):
                if (j, i) in locked:
                    del locked[(j, i)]

    if full_rows:
        # Sort keys by y descending to avoid overwriting during pop/set
        new_locked = {}
        for (x, y), color in locked.items():
            # Count how many full rows are below this block
            shift = len([r for r in full_rows if r > y])
            new_locked[(x, y + shift)] = color

        locked.clear()
        locked.update(new_locked)

    return len(full_rows)

def draw_grid(surface, grid):
    sx = 0
    sy = 0

    for i in range(len(grid)):
        pygame.draw.line(surface, GRAY, (sx, sy + i*GRID_SIZE), (sx + PLAY_WIDTH, sy + i*GRID_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GRAY, (sx + j*GRID_SIZE, sy), (sx + j*GRID_SIZE, sy + PLAY_HEIGHT))

def draw_block(surface, color, x, y):
    if color == BLACK:
        return
    pygame.draw.rect(surface, color, (x, y, GRID_SIZE, GRID_SIZE), 0)
    # Koyu kenarlık
    pygame.draw.rect(surface, (max(0, color[0]-100), max(0, color[1]-100), max(0, color[2]-100)), (x, y, GRID_SIZE, GRID_SIZE), 1)
    # Açık iç kenarlık (Parlama efekti için)
    pygame.draw.rect(surface, (min(255, color[0]+100), min(255, color[1]+100), min(255, color[2]+100)), (x+2, y+2, GRID_SIZE-4, GRID_SIZE-4), 1)

def draw_window(surface, grid, score=0, last_score=0):
    surface.fill(BLACK)

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 60, bold=True)
    label = font.render('TETRıS', 1, WHITE)

    surface.blit(label, (PLAY_WIDTH / 2 - (label.get_width() / 2), 10))

    # Current score
    font = pygame.font.SysFont('Arial', 30)
    label = font.render('SKOR: ' + str(score), 1, WHITE)

    sx = PLAY_WIDTH + 50
    sy = PLAY_HEIGHT // 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != BLACK:
                draw_block(surface, grid[i][j], j*GRID_SIZE, i*GRID_SIZE)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, MAGENTA, (0, 0, PLAY_WIDTH, PLAY_HEIGHT), 3)

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Arial', 30)
    label = font.render('SIRADAKı', 1, WHITE)

    sx = PLAY_WIDTH + 50
    sy = PLAY_HEIGHT // 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                draw_block(surface, shape.color, sx + j*GRID_SIZE, sy + i*GRID_SIZE)

    surface.blit(label, (sx + 10, sy - 30))

def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    # Yavaş hız için fall_speed değerini yüksek tutuyoruz (0.45 saniye)
    fall_speed = 0.45
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # Her 10 saniyede bir hızı biraz artır (ama yine de yavaş kalsın)
        if level_time/1000 > 10:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "OYUN BıTTı", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            return

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('Arial', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (PLAY_WIDTH / 2 - (label.get_width() / 2), PLAY_HEIGHT / 2 - (label.get_height() / 2)))

def main_menu(win):
    run = True
    while run:
        if not pygame.display.get_init():
            break
        win.fill(BLACK)
        draw_text_middle(win, 'BAŞLAMAK ıÇıN BıR TUŞA BASIN', 30, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
                if not pygame.display.get_init():
                    run = False

    if pygame.display.get_init():
        pygame.display.quit()

if __name__ == '__main__':
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetrıs')
    main_menu(win)
