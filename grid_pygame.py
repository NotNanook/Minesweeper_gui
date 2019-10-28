import pygame
import random as rd
import sys
rd.seed()
pygame.init()

LEFT = 1
RIGHT = 3
leben = 1

# Change size of the field
fgröse = 18

nkl = []
cl = []

field = [["O" for i in range(fgröse)] for i in range(fgröse)]
bomben = [[rd.randint(0,fgröse-1), rd.randint(0,fgröse-1)] for x in range(round((10*(fgröse**2))//100))]
print("Bomben", bomben)
rn = int(fgröse**2-len(bomben))

color = 1
weis = (255, 255, 255)
rot = (255, 0, 0)
grau = (238,232,170)
orange = (255,165,0)
schwarz = (0,0,0)
colors = [(50,205,50), (152,251,152)]

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

def c3x3(field, mx, my):
    zr = range(mx-1, mx+2)
    sr = range(my-1, my+2)
    for i in zr:
        for j in sr:
            if field[i][j] != "+":
                pygame.draw.rect(screen, grau, (i*gröse+(i*1)+1, j*gröse+(j*1)+1, gröse, gröse))
                myfont = pygame.font.SysFont('Comic Sans MS', int(gröse/2.5))
                textsurface = myfont.render(field[i][j], False, (0, 0, 0))
                screen.blit(textsurface,(i*gröse+(i*1)+gröse/2.3, j*gröse+(j*1)+gröse/3.7))
                if field[i][j] == "0":
                    if [i, j] not in nkl and field[i][j] != "+":
                        if i < 0 or j < 0 or i > fgröse or j > fgröse:
                            pass
                        else:
                            nkl.append([i, j])


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
            pos = pygame.mouse.get_pos()
            mx, my = pos
            mx = int((mx-(int(mx/gröse)*1))/gröse)
            my = int((my-(int(my/gröse)*1))/gröse)
            print(mx, my)

            try:
                if field[mx][my] != "+" and pygame.Surface.get_at(screen, pos) != grau and pygame.Surface.get_at(screen, pos) != schwarz and field[mx][my] != "0":
                    pygame.draw.rect(screen, grau, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))
                    myfont = pygame.font.SysFont('Comic Sans MS', int(gröse/2.5))
                    textsurface = myfont.render(field[mx][my], False, (0, 0, 0))
                    screen.blit(textsurface,(mx*gröse+(mx*1)+gröse/2.3, my*gröse+(my*1)+gröse/3.7))
                elif field[mx][my] == "+":
                    pygame.draw.rect(screen, rot, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))
                    if leben != 0:
                        leben -= 1
                    elif leben == 0:
                        game_over = True
                elif field[mx][my] == "0":
                    nkl = []
                    c3x3(field, mx, my)
                    while len(nkl) != 1:
                        mx = nkl[0][0]
                        my = nkl[0][1]
                        c3x3(field, mx, my)
                        print("NKL", nkl)
                        nkl.pop(0)
                else:
                    pass
            except IndexError:
                print("IndexError")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            pos = pygame.mouse.get_pos()
            mx, my = pos
            mx = int((mx-(int(mx/gröse)*1))/gröse)
            my = int((my-(int(my/gröse)*1))/gröse)

            if pygame.Surface.get_at(screen, pos) == colors[0] or pygame.Surface.get_at(screen, pos) == colors[1]:
                cc = pygame.Surface.get_at(screen, pos)
                pygame.draw.rect(screen, orange, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))
            else:
                pygame.draw.rect(screen, cc, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))



    while z != fgröse - 1 and s != fgröse - 1:
        colo = rd.randint(0,1)
        for z in range(len(field)):
            for s in range(len(field[z])):
                if s == fgröse - 1:
                    if colors[colo] == (50,205,50):
                        pygame.draw.rect(screen, colors[colo], (x, y, gröse, gröse))
                        colo = (colo + 1) % 2

                    elif colors[colo] == (152,251,152):
                        pygame.draw.rect(screen, colors[colo], (x, y, gröse, gröse))
                        colo = (colo + 1) % 2

                    colo = (colo + 1) % 2
                    y+= gröse+1
                    x = 1

                else:
                    if colors[colo] == (50,205,50):
                        pygame.draw.rect(screen, colors[colo], (x, y, gröse, gröse))
                        x += gröse+1
                        colo = (colo + 1) % 2

                    elif colors[colo] == (152,251,152):
                        pygame.draw.rect(screen, colors[colo], (x, y, gröse, gröse))
                        x += gröse+1
                        colo = (colo + 1) % 2

                #print(z, s)

    pygame.display.update()

