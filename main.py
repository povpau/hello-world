import pygame
import tkinter as tk
from tkinter import filedialog

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (128, 128, 128)

# File selection dialog
root = tk.Tk()
root.withdraw()
param_file = filedialog.askopenfilename(title="Select parameter file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
if not param_file:
    print("No file selected. Exiting.")
    exit(1)

# Read parameters from file
with open(param_file, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# Parse parameters
# 1st line: grid_rows
# 2nd line: grid_cols
# 3rd line: num_vertical_headers
# 4th line: num_horizontal_headers
# Next num_vertical_headers lines: vertical header cells (comma separated)
# Next num_horizontal_headers lines: horizontal header cells (comma separated)
grid_rows = int(lines[0])
grid_cols = int(lines[1])
num_vertical_headers = int(lines[2])
num_horizontal_headers = int(lines[3])

vertical_header_cells = []
for i in range(num_vertical_headers):
    vals = lines[4 + i].split(',')
    if len(vals) != grid_rows:
        raise ValueError(f"Vertical header col {i+1} must have {grid_rows} values, got {len(vals)}")
    vertical_header_cells.append([v.strip() for v in vals])

horizontal_header_cells = []
for i in range(num_horizontal_headers):
    vals = lines[4 + num_vertical_headers + i].split(',')
    if len(vals) != grid_cols:
        raise ValueError(f"Horizontal header row {i+1} must have {grid_cols} values, got {len(vals)}")
    horizontal_header_cells.append([v.strip() for v in vals])

cell_size = 60
width = (grid_cols + num_vertical_headers) * cell_size
height = (grid_rows + num_horizontal_headers) * cell_size

# Check header cell sizes
assert all(len(col) == grid_rows for col in vertical_header_cells), "Each vertical header column must have grid_rows elements"
assert all(len(row) == grid_cols for row in horizontal_header_cells), "Each horizontal header row must have grid_cols elements"

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Grid with Multiple Headers')
font = pygame.font.SysFont(None, 32)

# Grid state: 0 for white, 1 for black (excluding headers)
grid = [[0 for _ in range(grid_cols)] for _ in range(grid_rows)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - num_vertical_headers * cell_size) // cell_size
            row = (y - num_horizontal_headers * cell_size) // cell_size
            # Only allow toggling non-header cells
            if 0 <= row < grid_rows and 0 <= col < grid_cols and x >= num_vertical_headers * cell_size and y >= num_horizontal_headers * cell_size:
                grid[row][col] = 1 - grid[row][col]  # Toggle cell

    # Draw background
    screen.fill(WHITE)

    # Draw vertical headers (columns)
    for vh in range(num_vertical_headers):
        for r in range(grid_rows):
            rect = pygame.Rect(vh * cell_size, (r + num_horizontal_headers) * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARKGRAY, rect)
            num_text = font.render(str(vertical_header_cells[vh][r]), True, BLACK)
            text_rect = num_text.get_rect(center=(rect.x + cell_size // 2, rect.y + cell_size // 2))
            screen.blit(num_text, text_rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw horizontal headers (rows)
    for hh in range(num_horizontal_headers):
        for c in range(grid_cols):
            rect = pygame.Rect((c + num_vertical_headers) * cell_size, hh * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARKGRAY, rect)
            num_text = font.render(str(horizontal_header_cells[hh][c]), True, BLACK)
            text_rect = num_text.get_rect(center=(rect.x + cell_size // 2, rect.y + cell_size // 2))
            screen.blit(num_text, text_rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw grid cells
    for r in range(grid_rows):
        for c in range(grid_cols):
            color = BLACK if grid[r][c] else WHITE
            rect = pygame.Rect((c + num_vertical_headers) * cell_size, (r + num_horizontal_headers) * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)
    pygame.display.flip()

pygame.quit()