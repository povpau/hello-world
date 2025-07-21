import pygame

# User input for grid size (excluding headers)
grid_rows = int(input("Enter number of grid rows: "))
grid_cols = int(input("Enter number of grid columns: "))
num_vertical_headers = int(input("Enter number of vertical header columns: "))
num_horizontal_headers = int(input("Enter number of horizontal header rows: "))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (128, 128, 128)

# Prompt user for vertical header cell values (one line per header, comma separated, empty allowed)
vertical_header_cells = []
for vh in range(num_vertical_headers):
    while True:
        vals = input(f"Enter {grid_rows} comma separated values for vertical header col {vh+1} (empty allowed): ").split(',')
        if len(vals) == grid_rows:
            vertical_header_cells.append([v.strip() for v in vals])
            break
        else:
            print(f"Incorrect number of values. Expected {grid_rows}, got {len(vals)}. Please try again.")

# Prompt user for horizontal header cell values (one line per header, comma separated, empty allowed)
horizontal_header_cells = []
for hh in range(num_horizontal_headers):
    while True:
        vals = input(f"Enter {grid_cols} comma separated values for horizontal header row {hh+1} (empty allowed): ").split(',')
        if len(vals) == grid_cols:
            horizontal_header_cells.append([v.strip() for v in vals])
            break
        else:
            print(f"Incorrect number of values. Expected {grid_cols}, got {len(vals)}. Please try again.")

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