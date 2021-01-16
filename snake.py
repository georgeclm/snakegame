import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
# fo the object snake and the cube
# class for the cube object


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color="red"):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        # the position is based on the cube for x and y coordinate mean 1,4 etc is the grid that has been made
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        # i for rows and j for column
        i = self.pos[0]
        j = self.pos[1]
        # so to not cover up the white grid because if not then it will overwrite and remove the grid
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
# class for the snake object


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        # self head is for the head of the snake and postion to declare where the snake
        self.head = cube(pos)
        # self body to add after the head
        self.body.append(self.head)
        # for the movement
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # to check key that got pressed using pygame different with turtle
            keys = pygame.key.get_pressed()
            # the key that press and the movement and remeber the position where the head move so the body can follow
            for key in keys:
                if keys[pygame.K_LEFT]:
                    # to change the movement to left mean -1
                    self.dirnx = -1
                    self.dirny = 0
                    # to save the position where the head snake move so the body can move along
                    # use [:] to not change the data just to copy
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            # if the postion of body is in the position that it is going to move
            p = c.pos[:]
            # check the position if in the turn list
            if p in self.turns:
                turn = self.turns[p]
                # move the body with the turn value from p x,y
                c.move(turn[0], turn[1])
                # when the last cube hit the turn it is going to remove the turn
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                # this is for if it is going out of the screen first if going outside the edge to  the left then it is going to change to the right of the screen and the position -1 because index and the same y coord
                # second if when it is going to the outside when going right then it will go to the left side by putting zero and same y position
                # third if mean if it is going down then check if it is going outside the screen then move to the upper side by putting 0 and same x coord
                # last if mean if it is going up to outside the screen then it will go down
                # it is not moving up down left right and not at the edge of thescreen else then it is just move on the normal path
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        # put the head at the first position
        self.head = cube(pos)
        # reset body
        self.body = []
        # delete all the body
        self.body.append(self.head)
        # reset the turns
        self.turns = {}
        # set the movement
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        # to take the last body
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        # to check the direction where it is going so know where to add the cube could be left, right up or down
        # the first if if it move to the left then put the cube on the right then position -1
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        # after add then make the cube move at the tail current direction
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                # this true mean if it the first one or the head then it will draw eye on the snake to now the first one
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        # to draw line x,0 is the starting point until x,w
        # same for below 0,y until w,y in the for loops
        pygame.draw.line(surface, "white", (x, 0), (x, w))
        pygame.draw.line(surface, "white", (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill("black")
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):

    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return(x, y)


def message_box(subject, content):
    # to create window
    root = tk.Tk()
    # set the windows on top of every window use topmost
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global rows, width, s, snack
    width = 500
    rows = 20
    # to display the window for the surface
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption('Snake by George')
    s = snake("red", (10, 10))
    snack = cube(randomSnack(rows, s), color="green")
    flag = True
    # build in pygame for the program speed
    clock = pygame.time.Clock()
    # lower pygame time delay mean is the faster is gonna be
    # lower clock tick the slower is gonna be
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        # to check if the snake hit a snack then add body
        if s.body[0].pos == snack.pos:
            s.addCube()
            # generate new snack
            snack = cube(randomSnack(rows, s), color="green")
        for x in range(len(s.body)):
            # looping through every body in the snake
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                # write the messege mean the game end for colliding
                message_box("You lost ", "Score: {} Play again".format(
                    len(s.body)))
                # reset the position
                s.reset((10, 10))
                break

        redrawWindow(win)
    pass


main()
