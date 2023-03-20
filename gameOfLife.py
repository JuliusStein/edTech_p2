import pygame
import sys

WIDTH = 400
ROWS = 10
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Game of Life")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))


def make_grid(rows, width):
    grid = []

    gap = WIDTH // rows

    print(gap)

    for i in range(rows):
        #make a new row
        grid.append([])
        for j in range(rows):
            #iterate accros collumns, creating a Node instance at each
            node = Node(j, i, gap)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS

    for i in range(rows):
        #make a new row (a black line accross the screen)
        pygame.draw.line(win, BLACK, (0, i*gap), (width, i*gap))

        for j in range(rows):
            #iterate accros collumns, creating a black line at each
            pygame.draw.line(win, BLACK, (j*gap, 0), (j*gap, width))

    """
    The nodes are all white so this we need to draw the 
    grey lines that separate all the chess tiles
    from each other and that is what this function does
    """


def update_display(win, grid, rows, width):
    #iterate over all the nodes in the grid and draw them
    #draw functions both to update the display and to draw the grid
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def Find_Node(pos, WIDTH):
    interval = WIDTH / ROWS
    y, x = pos

    rows = y // interval
    columns = x // interval

    return int(rows), int(columns)

def neighbour(tile):
    col, row = tile.row, tile.col

    # creates a new list of all the neighbouring locations of the given tile
    neighbours = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1],
                  [row, col - 1], [row, col + 1],
                  [row + 1, col - 1], [row + 1, col], [row + 1, col + 1], ]

    #iterates through locations, retrieving the neighboring cells and returning them as a list
    actual = []
    for i in neighbours:
        row, col = i
        if 0 <= row <= (ROWS - 1) and 0 <= col <= (ROWS - 1):
            actual.append(i)
    # print(row, col, actual)
    return actual

# it is important that the grid be updated in the array before the changes are enacted because
# if the changes are enacted before the grid is updated, the changes will affect the following
# cell's calcaulations
def update_grid(grid):
    newgrid = []
    #iterate in row major order over the grid
    for row in grid:
        for tile in row:
            # get the neighboring cells for the given tile
            neighbours = neighbour(tile)
            count = 0
            # iterate over the neighbouring cells and count the number of occupied cells
            for i in neighbours:
                row, col = i
                if grid[row][col].colour == BLACK:
                    count += 1
            """
             Apply the rules of the game of life to the given tile: 
             1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
             2. Any live cell with two or three live neighbours lives on to the next generation.
             3. Any live cell with more than three live neighbours dies, as if by overpopulation.
             4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            """

            if tile.colour == BLACK:
                if count == 2 or count == 3:
                    newgrid.append(BLACK)
                else:
                    newgrid.append(WHITE)
            else:
                if count == 3:
                    newgrid.append(BLACK)
                else:
                    newgrid.append(WHITE)

    # return the new updated grid
    return newgrid


def main(WIN, WIDTH):
    run = None
    grid = make_grid(ROWS, WIDTH)

    while True:
        pygame.time.delay(50)  #stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True

            #if the mouse is clicked, change the colour of the tile
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = Find_Node(pos, WIDTH)
                if grid[col][row].colour == WHITE:
                    grid[col][row].colour = BLACK
                elif grid[col][row].colour == BLACK:
                    grid[col][row].colour = WHITE

            
            while run:
                #continuously check if there is a mouseclick
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False

                #pygame.time.delay(50)

                # creates a new updated frame
                newcolours = update_grid(grid)
                count=0
                for i in range(0,len(grid[0])):
                    for j in range(0, len(grid[0])):
                        grid[i][j].colour=newcolours[count]
                        count+=1
                update_display(WIN, grid, ROWS, WIDTH)
                #run= False

            update_display(WIN, grid, ROWS, WIDTH)


main(WIN, WIDTH)