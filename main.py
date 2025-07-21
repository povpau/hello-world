import pygame

# Grid settings
rows, cols = 9, 9
cell_size = 60
width, height = cols * cell_size, rows * cell_size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (128, 128, 128)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Selectable Grid')

# Grid state: 0 for white, 1 for black
grid = [[0 for _ in range(cols)] for _ in range(rows)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // cell_size
            row = y // cell_size
            if 1 <= row < rows and 1 <= col < cols:
                grid[row][col] = 1 - grid[row][col]  # Toggle cell

    # Draw grid
    screen.fill(WHITE)
    for r in range(rows):
        for c in range(cols):
            color = BLACK if grid[r][c] else WHITE
            rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)  # Grid lines
    pygame.display.flip()

pygame.quit()