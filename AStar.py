#epq project, A* pathfinding, good luck

import pygame
import math
from queue import PriorityQueue

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

Width = 800
win = pygame.display.set_mode((Width,Width))
pygame.display.set_caption("A* Pathfinding Visuliser")
pygame.init()

class Spot:
    def __init__(self,row,col,total_rows,width):#width is the width of the cube not the screen
        self.col = col
        self.row = row
        self.total_rows = total_rows
        self.width = width
        self.neighbors = []
        self.x = row * width
        self.y = col * width
        self.colour = WHITE

    def get_pos(self):
        return self.col,self.row
    def reset(self):
        self.colour = WHITE
    def is_barrier(self):
        return self.colour == BLACK

    def update_neighbors (self,grid):
        self.neighbors  = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors .append(grid[self.row + 1][self.col]) # DOWN
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors .append(grid[self.row - 1][self.col]) #UP
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors .append(grid[self.row][self.col - 1]) #LEFT
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors .append(grid[self.row][self.col + 1]) # RIGHT 

    def draw(self,win):
        pygame.draw.rect(win,self.colour,(self.x,self.y,self.width,self.width))
    def __lt__(self,other):
        return False


def h(p1,p2):
    x1,y1 = p1
    x2, y2 = p2
    h = (abs(x1 - x2))**2 + abs ((y1 - y2))**2#######
    h = math.sqrt(h)
    
    return h

def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range (rows):
        grid.append([])
        for j in range (rows):
            spot = Spot(i,j,rows,gap)
            grid[i].append(spot)
    return grid


def draw_grid(win,rows,width):
    #print(width,rows)
    gap = width//rows
    for i in range (rows):
        pygame.draw.line(win,BLACK,((i*gap),0),(i*gap,800))
    for i in range(rows):
        pygame.draw.line(win,BLACK,(0,i*gap),(800,i*gap))

def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            #print(spot.x)
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_click(pos,width,rows):
    gap = width // rows
    x, y = pos
    col = y // gap
    row = x // gap
    return row,col

def reconstruct_path(CameFrom,current,draw):
    while current in CameFrom:
        current = CameFrom[current]
        current.colour = PURPLE
        #print(rows,width)
        draw()
    draw()
    

def algo(grid,start,end,draw,fast):
    count = 0
    OpenSet = PriorityQueue()
    OpenSet.put((0,count,start))
    CameFrom = {}
    GScore = {}
    FScore = {}
##    for row in grid:
##        for spot in row:
##            GScore[spot] = float("inf")
##            FScore[spot] = float("inf")
    GScore = {spot: float("inf") for row in grid for spot in row}
    FScore = {spot: float("inf") for row in grid for spot in row}
    GScore[start] = 0
    FScore[start] = h(start.get_pos(),end.get_pos())

    HashSet = {start}

    while not OpenSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = OpenSet.get()[2]
        HashSet.remove(current)
        
        if current == end:
            reconstruct_path(CameFrom,end,draw)
            end.colour = TURQUOISE
            return True

        for neighbor in current.neighbors:
            tempG = GScore[current] + 1
            
            if tempG < GScore[neighbor]:
                CameFrom[neighbor] = current
                GScore[neighbor] = tempG
                FScore[neighbor] = tempG + h(neighbor.get_pos(),end.get_pos())
                
                if neighbor not in HashSet:
                    count += 1
                    OpenSet.put((FScore[neighbor],count,neighbor))
                    HashSet.add(neighbor)
                    neighbor.colour = GREEN
                    
             
         
        if not fast: 
            draw()######

        if current != start:
            current.colour = RED#####
            
    return False


def main(win,width):
    rows = 50
    grid  = make_grid(rows,width)
    start = None
    end  = None
    running = True
   
    
    while running:
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        draw(win,grid,rows,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                
            if click[0]:
                row,col = get_click(pos,width,rows)
                spot = grid[row][col]
                if start == None and spot != end:
                    start = spot
                    spot.colour = ORANGE
                    
                elif end == None and spot != start:
                    end = spot
                    spot.colour = TURQUOISE
                    
                elif spot != end and spot != start:
                    spot.colour = BLACK 
                    
                    
            if click[2]:
                row,col = get_click(pos,width,rows)
                spot = grid[row][col]
                if spot == start:
                    start = None
                elif spot == end:
                    end = None 
                spot.reset()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    for row in grid:
                        for spot in row:
                            start = None
                            end = None 
                            spot.reset()
                            
                if event.key == pygame.K_SPACE:
                     if start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        algo(grid,start,end,lambda:draw(win,grid,rows,width),False)
                                
                if event.key == pygame.K_RETURN:
                    if start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        algo(grid,start,end,lambda:draw(win,grid,rows,width),True)
                if event.key == pygame.K_p:
                    start = None
                    end = None
                    for row in grid:
                        for spot in row:
                            if spot.is_barrier() == True:
                                pass
                            else:
                                spot.reset()
                
                

                        
main(win,Width)
