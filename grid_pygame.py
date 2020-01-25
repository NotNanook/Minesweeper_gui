import pygame
import random as rd
import os
import time
import tkinter as tk


rd.seed()
pygame.init()

# different mouseclicks
LEFT = 1
RIGHT = 3

# leben
leben = 1

# temp variable to check for first playthrough
first_t_start = True

# temp variable
temp = True
temp2 = True

# fieldsize
fgröse = 14

# percent of bombs
bomb_perc = 20

# how many bombs
bomb_anz = round((bomb_perc*(fgröse**2))//100)

# masks for different playstyles

Standard = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)]
Kreuz = [(-1,0),(0,-1),(0,0),(0,1),(1,0)]

masklist = {"Default":Standard, "Cross":Kreuz}

# window to choose the playstyle
main = tk.Tk("Minesweeper")

# variable for index of playstyle
var = tk.IntVar()
var.set(0)

# button function
def quit_loop():
    global selection
    selection = var.get()
    main.destroy()

tk.Label(main, text="Choose playstyle", font=("Default", 15)).grid(row=0)

for masksnum in range(len(masklist)):

    # create a radiobutton for every element in masklist
    tk.Radiobutton(main, text=list(masklist.keys())[masksnum], variable=var, value=masksnum, font=("Default", 15)).grid(row=masksnum+1)

# start button
button = tk.Button(main, text="Start", command=quit_loop, font=("Default", 15)).grid(row=len(masklist)+1)

main.mainloop()

try:
    mask = list(masklist.values())[selection]
except:
    os._exit(1)

# for fields that have 0 bombs around them
nkl = []

# list for counting bombs on start of the game
cl = []

# all correctly clicked fields
rfelder = set()

# generating field
field = [["O" for i in range(fgröse)] for i in range(fgröse)]

color = 1

# colors
grün = (50,205,50)
weis = (255, 255, 255)
rot = (255, 0, 0)
grau = (238,232,170)
orange = (255,165,0)
schwarz = (0,0,0)

# colors for the board
colors = [(50,205,50), (152,251,152)]

# how much fields you have to click to win (Changes as soon as game starts)
rn = 1

x = 1
y = 1
z = 0
s = 0

gröse = 50

def add_bombs(field, mx, my):

    # list of start coordinates
    startcords = []

    for tup_mask in mask:

                # tupel
                addx, addy = tup_mask

                # add tupel coords to clicked coords
                addedx, addedy = addx + mx, addy + my

                if addedx >= 0 and addedy >= 0 and addedx < fgröse and addedy < fgröse:

                    # add startcoords to startcords list
                    startcords.append((addedx, addedy))

    # generate bombs
    global bomben
    bomben = set()

    while len(bomben) != bomb_anz:
        bombe = (rd.randint(0,fgröse-1), rd.randint(0,fgröse-1))

        if bombe not in startcords:

            bomben.add(bombe)

    # add bombs
    for i in bomben:
            b_höhe, b_breite = i
            field[b_höhe][b_breite] = "+"




for a in range(len(field)):
    for b in range(len(field[a])):

        # check if not a bomb
        if field[a][b] != "+":

            for tup_mask in mask:

                # tupel
                addx, addy = tup_mask
                # add tupel coords to clicked coords
                addedx, addedy = addx + a, addy + b

                if addedx >= 0 and addedy >= 0 and addedx < fgröse and addedy < fgröse:

                    # add fields to cl to count them
                    cl.append(field[addedx][addedy])


            bomb_count = cl.count("+")
            field[a][b] = str(bomb_count)
            cl = []

width = fgröse * gröse + (fgröse - 1) * 1
height = fgröse * gröse + (fgröse - 1) * 1

game_over = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")

while True:

    if len(rfelder) >= rn and temp2:
        print("You have won!")

        for bombs in bomben:

            # tupel
            bx, by = bombs

            # show every bomb on field with red color
            pygame.draw.rect(screen, grün, (bx*gröse+(bx*1)+1, by*gröse+(by*1)+1, gröse, gröse))

        game_over = True
        temp2 = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and game_over == False:

            pos = pygame.mouse.get_pos()
            mx, my = pos
            mx = int((mx-(int(mx/gröse)*1))/gröse)
            my = int((my-(int(my/gröse)*1))/gröse)

            if first_t_start:
                add_bombs(field, mx, my)

                for a in range(len(field)):
                    for b in range(len(field[a])):

                        # check if not a bomb
                        if field[a][b] != "+":

                            for tup_mask in mask:

                                # tupel
                                addx, addy = tup_mask

                                # add tupel coords to clicked coords
                                addedx, addedy = addx + a, addy + b

                                if addedx >= 0 and addedy >= 0 and addedx < fgröse and addedy < fgröse:

                                    # add fields to cl to count them
                                    cl.append(field[addedx][addedy])


                            bomb_count = cl.count("+")
                            field[a][b] = str(bomb_count)
                            cl = []

                # how much fields to win
                rn = int(fgröse**2-len(bomben))
                print("Correct needed:", rn)
                first_t_start = False

            if field[mx][my] != "+" and pygame.Surface.get_at(screen, pos) != grau and pygame.Surface.get_at(screen, pos) != schwarz and field[mx][my] != "0":
                pygame.draw.rect(screen, grau, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))
                myfont = pygame.font.SysFont('Comic Sans MS', int(gröse/2.5))
                textsurface = myfont.render(field[mx][my], False, (0, 0, 0))
                screen.blit(textsurface,(mx*gröse+(mx*1)+gröse/2.3, my*gröse+(my*1)+gröse/3.7))

                # add correct field to rfelder
                rfelder.add((mx,my))
                print("Correct:", len(rfelder))

            elif field[mx][my] == "+":

                pygame.draw.rect(screen, rot, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))
                pygame.display.update()

                # give the player time to process what they have done
                time.sleep(0.5)

                game_over = True

            elif field[mx][my] == "0" and pygame.Surface.get_at(screen, pos) != grau and pygame.Surface.get_at(screen, pos) != schwarz:

                # add first coords
                nkl.append((mx,my))

                # loop as long all fields are checked
                while len(nkl) != 0:

                    # take mx, my from the list
                    mx, my = nkl[0]

                    for tup_mask in mask:


                        # tupel
                        addx, addy = tup_mask

                        # add tupel coords to clicked coords
                        addedx, addedy = addx + mx, addy + my

                        # try/except because of bug in last row
                        try:
                            if addedx >= 0 and addedy >= 0 and addedx <= fgröse-1 and addedy <= fgröse-1:

                                # make field yellow/grey
                                pygame.draw.rect(screen, grau, (addedx*gröse+(addedx*1)+1, addedy*gröse+(addedy*1)+1, gröse, gröse))

                                # show numbers
                                myfont = pygame.font.SysFont('Comic Sans MS', int(gröse/2.5))
                                textsurface = myfont.render(field[addedx][addedy], False, (0, 0, 0))
                                screen.blit(textsurface,(addedx*gröse+(addedx*1)+gröse/2.3, addedy*gröse+(addedy*1)+gröse/3.7))

                                # add field to nkl if not in rfelder
                                if field[addedx][addedy] == "0" and field[addedx][addedy] != "+" and (addedx,addedy) not in rfelder:

                                    nkl.append((addedx, addedy))

                                # add field to rfelder
                                rfelder.add((addedx,addedy))



                        except IndexError:
                            continue

                    # pop first element
                    nkl.pop(0)

                print("Correct:", len(rfelder))

        # still bugy
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and not game_over:
            pos = pygame.mouse.get_pos()
            mx, my = pos
            mx = int((mx-(int(mx/gröse)*1))/gröse)
            my = int((my-(int(my/gröse)*1))/gröse)

            if pygame.Surface.get_at(screen, pos) == colors[0] or pygame.Surface.get_at(screen, pos) == colors[1]:
                cc = pygame.Surface.get_at(screen, pos)
                pygame.draw.rect(screen, orange, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))
            elif pygame.Surface.get_at(screen, pos) == orange:
                pygame.draw.rect(screen, cc, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))

    # show all bombs if lost
    if game_over and temp and temp2:

        # iterate over all bombs
        for bombs in bomben:

            # tupel
            bx, by = bombs

            # show all bombs red
            pygame.draw.rect(screen, rot, (bx*gröse+(bx*1)+1, by*gröse+(by*1)+1, gröse, gröse))

        # so it doesnt draw the screen everytime some event happens
        temp = False


    # drawing the board
    while z != fgröse - 1 and s != fgröse - 1:

        #choose random color
        colo = rd.randint(0,1)

        for z in range(len(field)):

            # switch color every row if fgröse is even
            colo = (colo + 1) % 2 if fgröse % 2 == 0 else colo

            for s in range(len(field[z])):

                colo = (colo + 1) % 2

                pygame.draw.rect(screen, colors[colo], (x, y, gröse, gröse))

                # assign x, y coords
                y = y+gröse+1 if s == fgröse-1 else y
                x = x+gröse+1 if s != fgröse-1 else 1

    try:
        pygame.display.update()
    except:
        break
