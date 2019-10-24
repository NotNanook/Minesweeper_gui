import pygame
import random as rd
import sys
rd.seed()
pygame.init()

LEFT = 1
RIGHT = 3
leben = 1

# Change size of the field
fgröse = 15

cl = []

field = [["O" for i in range(fgröse)] for i in range(fgröse)]
bomben = [[rd.randint(0,fgröse-1), rd.randint(0,fgröse-1)] for x in range(round((20*(fgröse**2))//100))]

weis = (255, 255, 255)
rot = (255, 0, 0)
grau = (192, 192, 192)
orange = (255,165,0)

x = 1
y = 1
z = 0
s = 0

gröse = 50

for i in bomben:
        b_höhe, b_breite = i
        if field[b_höhe][b_breite] == "O":
            field[b_höhe][b_breite] = "+"

for a in range(len(field)):
        for b in range(len(field[a])):
            zr = range(a-1, a+2)
            sr = range(b-1, b+2)
            if field[a][b] != "+":

                for i in zr:
                        for j in sr:
                            try:
                                if j >= 0 and i >= 0:
                                    cl.append(field[i][j])
                                else:
                                    pass

                            except IndexError:
                                pass

                ndb = cl.count("+")
                field[a][b] = str(ndb)
                cl = []

            else:
                pass

#for c in field:
#   print(c)

width = fgröse * gröse + (fgröse - 1) * 1
height = fgröse * gröse + (fgröse - 1) * 1

game_over = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            pos = pygame.mouse.get_pos()
            print(pos)
            mx, my = pos
            mx = int(mx / gröse)
            my = int(my / gröse)
            print(my, mx)

            try:
                if field[mx][my] != "+":
                    pygame.draw.rect(screen, grau, (mx*50+(mx*1)+1, my*50+(my*1)+1, gröse, gröse))
                    myfont = pygame.font.SysFont('Comic Sans MS', 20)
                    textsurface = myfont.render(field[mx][my], False, (0, 0, 0))
                    screen.blit(textsurface,(mx*50+(mx*1)+21, my*50+(my*1)+15))
                else:
                    pygame.draw.rect(screen, rot, (mx*50+(mx*1)+1, my*50+(my*1)+1, gröse, gröse))
                    if leben != 0:
                        leben -= 1
                    elif leben == 0:
                        game_over = True
            except IndexError:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            pos = pygame.mouse.get_pos()
            mx, my = pos
            mx = int(mx / gröse)
            my = int(my / gröse)
            if pygame.Surface.get_at(screen, pos) == weis:
                pygame.draw.rect(screen, orange, (mx*50+(mx*1)+1, my*50+(my*1)+1, gröse, gröse))
            else:
                pygame.draw.rect(screen, weis, (mx*50+(mx*1)+1, my*50+(my*1)+1, gröse, gröse))



    while z != fgröse - 1 and s != fgröse - 1:
        for z in range(len(field)):
            for s in range(len(field[z])):
                if s == fgröse - 1:
                    if field[z][s] != "+":
                        pygame.draw.rect(screen, weis, (x, y, gröse, gröse))
                    else:
                        pygame.draw.rect(screen, weis, (x, y, gröse, gröse))
                    y+= gröse+1
                    x = 1
                else:
                    if field[z][s] == "+":
                        pygame.draw.rect(screen, weis, (x, y, gröse, gröse))
                        x += gröse+1
                    else:
                        pygame.draw.rect(screen, weis, (x, y, gröse, gröse))
                        x += gröse+1
                #print(z, s)

    pygame.display.update()

