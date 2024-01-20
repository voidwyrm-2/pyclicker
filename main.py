import pygame
from random import randint
import math
from pathlib import Path



LUDICROUSDEBUG = False


SAVEFILE = './pyclickersave.txt'

def limitmax(input, max):
    if input > max: return max
    return input

def limitmin(input, min):
    if input < min: return min
    return input


def isWithinRange(collideeX: int | float, collideeY: int | float, collidedX: int | float, collidedY: int | float, colrange: int | float):
    distance = math.sqrt(math.pow(collideeX - collidedX, 2) + (math.pow(collideeY - collidedY, 2)))
    if distance < colrange: return True
    return False


def work(): 'makes the code work'


def loadsave(dataindex = 0, type = int, toprint = ''):
    one = "<class '"
    two = "'>"
    if toprint == '': toprint = f'accessed {dataindex} as {str(type).removeprefix(one).removesuffix(two)}'
    with open(SAVEFILE, 'rt') as savein:
        gottensave = savein.read()
        sgsave = gottensave.split('\n')
        gottendata = type(sgsave[dataindex])
        print(toprint + f', with a value of {str(gottendata)}')
        return gottendata

if not Path(SAVEFILE).exists():
    print('no savefile detected! creating new...')
    with open(SAVEFILE, 'xt') as save404: save404.write('''0
1
10'''); print('new savefile successfully created')



# initialize game
if LUDICROUSDEBUG: print('=====PREINIT LOGS=====')
if LUDICROUSDEBUG: print('initializing game...')
pygame.init()

# creating a screen
if LUDICROUSDEBUG: print('creating screen...')
windratio = 600, 600
screen = pygame.display.set_mode(windratio)  # passing width and height
if LUDICROUSDEBUG: print(f'screen created with ratio {windratio[0]}, {windratio[1]}')

if LUDICROUSDEBUG: print('prepping screen for game...')
screen.fill("black")
pygame.display.flip()
if LUDICROUSDEBUG: print('screen loading complete!')

# title and icon
if LUDICROUSDEBUG: print('loading game title...')
pygame.display.set_caption("Pyclicker")
if LUDICROUSDEBUG: print('game title loaded!')

if LUDICROUSDEBUG: print('loading game icon...')
icon = pygame.image.load('Pyclicker-icon.png') # Welcome to Rhythm Doctor- I mean Pyclicker
pygame.display.set_icon(icon)
if LUDICROUSDEBUG: print('game icon loaded!')

if LUDICROUSDEBUG: print('loading clock...')
clock = pygame.time.Clock()
if LUDICROUSDEBUG: print('clock loaded!')

if LUDICROUSDEBUG: print('initializing font module...')
pygame.font.init()
if LUDICROUSDEBUG: print('loading fonts...')
mainfont = pygame.font.Font('freesansbold.ttf', 32)
storefont = pygame.font.Font('freesansbold.ttf', 30)
if LUDICROUSDEBUG: print('fonts loaded!')
if LUDICROUSDEBUG: print('=====PREINIT LOGS END=====\n\n')



print('====VARIABLE LOG====')
print('loading game variables...')
shouldTheCodeWork = True


gameticks = 0
showTicks = False
showCursorPos = False

pointsButtonX = windratio[0] // 2
pointsButtonY = windratio[1] // 2
pointsButtonSize = 100

multiplierButtonX = 100
multiplierButtonY = 150
multiplierButtonSize = 50

mouseX = 0
mouseY = 0
extraMouseRange = 5
isPressingPoints = False
isPressingMulti = False


savedpoints = loadsave(0)
points = 0 + savedpoints
getPoint = True
getMulti = True
pointsMultiplier = 0 + loadsave(1)
pMultiCost = loadsave(2)
if pointsMultiplier == 0: pointsMultiplier = 1
if LUDICROUSDEBUG: print('all variables loaded!')
print('====VARIABLE LOG END====')



def save():
    with open(SAVEFILE, 'wt') as saveout:
        saveout.write(f'''{points}
{pointsMultiplier}
{pMultiCost}''')
        print('====SAVE LOG====')
        print(f'saved "points" with a value of {points}')
        print(f'saved "pointsMultiplier" with a value of {pointsMultiplier}')
        print(f'saved "pMultiCost" with a value of {pMultiCost}')
        print('All data saved!')
        print('====SAVE LOG END====')

def drawPointsButton(x, y, size):
    pygame.draw.circle(screen, (150, 150, 150), (x, y), size)
    buttonInnerColor = 255
    if isPressingPoints: buttonInnerColor -= 100
    pygame.draw.circle(screen, (buttonInnerColor, 0, 0), (x, y), size - (2 * (size // 10)))

def drawMultiplierButton(x, y, size):
    pygame.draw.circle(screen, (150, 100, 150), (x, y), size)
    buttonInnerColor = 200
    if isPressingMulti: buttonInnerColor -= 100
    pygame.draw.circle(screen, (buttonInnerColor, buttonInnerColor, buttonInnerColor), (x, y), size - (2 * (size // 10)))
    shopmulti = storefont.render(f'PM', True, (255, 255, 255))
    screen.blit(shopmulti, (x - 20, y - 13))


def showticks(x, y):
    tick = mainfont.render(f'tick:{gameticks}', True, (255, 255, 255))
    screen.blit(tick, (x, y))

def showcursorpos(x, y):
    global mouseX
    global mouseY
    cp = mainfont.render(f'mouse_pos:{mouseX},{mouseY}', True, (255, 255, 255))
    screen.blit(cp, (x, y))

def showShapePos(x, y, Sx, Sy, Si):
    tick = mainfont.render(f'shapePos({Si}):{Sx}, {Sy}', True, (255, 255, 255))
    screen.blit(tick, (x, y))

def showinfo(x, y):
    poi = mainfont.render(f'points: {points}', True, (255, 255, 255))
    screen.blit(poi, (x, y))
    mul = mainfont.render(f'points multiplier: {pointsMultiplier}', True, (255, 255, 255))
    screen.blit(mul, (x, y + 33))



running = True
while running:
    if shouldTheCodeWork: work()
    screen.fill((0, 0, 0)) #background

    #poll for events
    #pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT: print('Game was quit!'); save(); running = False

        if event.type == pygame.KEYDOWN:
            #print("you pressed a key")
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: print('Game was quit!'); save(); running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if isWithinRange(mouseX, mouseY, pointsButtonX, pointsButtonY, pointsButtonSize - (2 * (pointsButtonSize // 10))):
                isPressingPoints = True
                if getPoint: points += 1 * pointsMultiplier; getPoint = False

            elif isWithinRange(mouseX, mouseY, multiplierButtonX, multiplierButtonY, multiplierButtonSize - (2 * (multiplierButtonSize // 10))):
                isPressingMulti = True
                if pMultiCost <= points:
                    if getMulti: pointsMultiplier += 1; points -= pMultiCost; pMultiCost += 20; getMulti = False

        if event.type == pygame.MOUSEBUTTONUP:
            isPressingPoints = False
            isPressingMulti = False
            getPoint = True
            getMulti = True

    mouseX, mouseY = pygame.mouse.get_pos()

    clock.tick(60)

    drawPointsButton(pointsButtonX, pointsButtonY, pointsButtonSize)
    drawMultiplierButton(multiplierButtonX, multiplierButtonY, multiplierButtonSize)
    showinfo(30, 0)

    if showTicks: showticks(0, 0)
    if showCursorPos: showcursorpos(0, 35)
    pygame.display.update()
    gameticks += 1