import sys, pygame

pygame.init()
clock = pygame.time.Clock()

# Window variables
WINDOW_SIZE = 500, 500
CELL_SIZE = 5
BG_COLOUR = 0,0,150
DEAD_COLOUR = 0,0,0
ALIVE_COLOUR = 255,255,255


def main():
  # Create pygame window
  window = pygame.display.set_mode(WINDOW_SIZE)
  window.fill(BG_COLOUR)
  pygame.display.set_caption("Drawing box")

  # Create cell matrix
  matrix = []
  for row in range(0, WINDOW_SIZE[1], CELL_SIZE):
    line = []
    for col in range(0, WINDOW_SIZE[0], CELL_SIZE):
      line.append([pygame.Rect(col, row, CELL_SIZE-1, CELL_SIZE-1),0])
    matrix.append(line)

  # Pause game before ready
  play = False
  
  while True:
    # Quit when quit event is triggered
    for event in pygame.event.get():
      # Quit game
      if event.type == pygame.QUIT: sys.exit()
      # Pause/Play game
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          if play:
            play = False
          else:
            play = True

    # Draw background
    window.fill(BG_COLOUR)

    # Draw cell matrix on screen
    for row in matrix:
      for cell in row:
        # Draw alive cell in white
        if cell[1] == 1:
          pygame.draw.rect(window, ALIVE_COLOUR, cell[0])
        # Draw dead cell in black
        else:
          pygame.draw.rect(window, DEAD_COLOUR, cell[0])

    # Use mouse to draw alive cells into matrix
    for row in range(len(matrix)):
      for col in range(len(matrix[0])):
        # If left mouse, turn cell alive
        if pygame.mouse.get_pressed() == (1, 0, 0) and pygame.Rect.collidepoint(matrix[row][col][0], pygame.mouse.get_pos()):
          matrix[row][col][1] = 1
        # If right mouse, turn cell dead
        if pygame.mouse.get_pressed() == (0, 0, 1) and pygame.Rect.collidepoint(matrix[row][col][0], pygame.mouse.get_pos()):
          matrix[row][col][1] = 0

    # Press 'c' to clear game
    if pygame.key.get_pressed()[pygame.K_c]:
      matrix = []
      for row in range(0, WINDOW_SIZE[1], CELL_SIZE):
        line = []
        for col in range(0, WINDOW_SIZE[0], CELL_SIZE):
          line.append([pygame.Rect(col, row, CELL_SIZE-1, CELL_SIZE-1),0])
        matrix.append(line)

    # Play game of life
    if play:
      # Create new matrix for next generation
      new_matrix = []

      # Loop through rows
      for row in range(len(matrix)):

        # Initiate an empty row to fill with the next generation
        new_cell_row = []

        # Loop through columns
        for col in range(len(matrix[0])):

          # Create empty list of neighbouring live matrix
          neighbours = []

          # Loop through neighbouring matrix
          for i in range(-1,2,1):
              for j in range(-1,2,1):
                # Skip centre cell (that's the cell we are currently calculating)
                if i == 0 and j == 0:
                  continue
                # Create new cell indexes
                new_row = row - i
                new_col = col - j

                # Check if new cell indexes are within the matrix, if not then skip to next cell
                if new_row < 0 or new_row > len(matrix)-1 or new_col < 0 or new_col > len(matrix[0])-1:
                  continue

                # Check if new cell index is alive, append to neighbour list
                if matrix[new_row][new_col][1] == 1:
                  neighbours.append(1)

          # Any live cell with fewer than two or more than three live neighbours dies
          if len(neighbours) < 2 or len(neighbours) > 3 :
            new_cell_row.append([pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1),0])

          # Any live cell with two or three live neighbours lives on to the next generation.
          elif len(neighbours) == 2:
            if matrix[row][col][1] == 1:
              new_cell_row.append([pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1),1])
            else:
              new_cell_row.append([pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1),0])

          # Any dead cell with exactly three live neighbours becomes a live cell.
          elif len(neighbours) == 3:
            new_cell_row.append([pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1),1])

        # Add the new row to the new matrix
        new_matrix.append(new_cell_row)

      matrix = new_matrix

    # Refresh window
    pygame.display.flip()


if __name__ == '__main__':
  main()
