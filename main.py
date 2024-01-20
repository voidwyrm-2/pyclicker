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
    with open(SAVEFILE, 'rt') as savein:
        gottensave = savein.read()
        sgsave = gottensave.split('\n')
        gottendata = sgsave[dataindex].split(':')

        if toprint == '': toprint = f'accessed {dataindex}({gottendata[1]}) as {str(type).removeprefix(one).removesuffix(two)}'
        truedata = type(gottendata[0])
        if gottendata[0].casefold() == 'false': truedata = False
        elif gottendata[0].casefold() == 'true': truedata = True
        print(toprint + f', with a value of {str(truedata)}')
        return truedata

if not Path(SAVEFILE).exists():
    print('no savefile detected! creating new...')
    with open(SAVEFILE, 'xt') as save404: save404.write('''0:points
1:pointsMultiplier
10:pMultiCost
false:autoclickersUnlocked
0:autoclickers
1:autoclickerMultiplier
40:autoclickerCost
1000:autoclickerinterval'''); print('new savefile successfully created')



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
showTicks = True
showCursorPos = False

#buttons
pointsButtonX = windratio[0] // 2
pointsButtonY = windratio[1] // 2
pointsButtonSize = 100

multiplierButtonX = 100
multiplierButtonY = 170
multiplierButtonSize = 50

clickerButtonX = 100
clickerButtonY = 340
clickerButtonSize = 50
#buttons end

#mouse things
mouseX = 0
mouseY = 0
extraMouseRange = 5
isPressingPoints = False
isPressingMulti = False
isPressingClicker = False
#mouse things end


getPoint = True
points = 0 + loadsave(0)

getMulti = True
pointsMultiplier = 0 + loadsave(1)
pMultiCost = loadsave(2)
if pointsMultiplier == 0: pointsMultiplier = 1

getClicker = True
autoclickersUnlocked = loadsave(3, bool)
#print(f'autoclickersUnlocked:{autoclickersUnlocked}')
autoclickers = 0 + loadsave(4)
autoclickerMultiplier = 0 + loadsave(5)
autoclickerCost = 0 + loadsave(6)
autoclickerinterval = 0 + loadsave(7)
autoclickerticker = autoclickerinterval
if autoclickerMultiplier == 0: autoclickerMultiplier = 1
if autoclickersUnlocked == None: autoclickersUnlocked = False
if pointsMultiplier >= 10: autoclickersUnlocked = True

if LUDICROUSDEBUG: print('all variables loaded!')
print('====VARIABLE LOG END====')



def save():
    with open(SAVEFILE, 'wt') as saveout:
        saveout.write(f'''{points}:points
{pointsMultiplier}:pointsMultiplier
{pMultiCost}:pMultiCost
{autoclickersUnlocked}:autoclickersUnlocked
{autoclickers}:autoclickers
{autoclickerMultiplier}:autoclickerMultiplier
{autoclickerCost}:autoclickerCost
{autoclickerinterval}:autoclickerinterval''')
        print('====SAVE LOG====')
        #print(f'saved "points" with a value of {points}')
        #print(f'saved "pointsMultiplier" with a value of {pointsMultiplier}')
        #print(f'saved "pMultiCost" with a value of {pMultiCost}')
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

def drawClickerButton(x, y, size):
    pygame.draw.circle(screen, (150, 100, 150), (x, y), size)
    buttonInnerColor = 200
    if isPressingClicker: buttonInnerColor -= 100
    pygame.draw.circle(screen, (buttonInnerColor, buttonInnerColor, buttonInnerColor), (x, y), size - (2 * (size // 10)))
    shopclicker = storefont.render(f'AC', True, (255, 255, 255))
    screen.blit(shopclicker, (x - 20, y - 13))


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
    global autoclickersUnlocked
    poi = mainfont.render(f'points: {points}', True, (255, 255, 255))
    screen.blit(poi, (x, y))
    mul = mainfont.render(f'points multiplier(PM): {pointsMultiplier}', True, (255, 255, 255))
    screen.blit(mul, (x, y + 33))
    if autoclickersUnlocked:
        aclickers = mainfont.render(f'autoclickers(AC): {autoclickers} AC interval:{autoclickerinterval}', True, (255, 255, 255))
        screen.blit(aclickers, (x, y + 66))



running = True
while running:
    #if shouldTheCodeWork: work()
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
            
            elif isWithinRange(mouseX, mouseY, clickerButtonX, clickerButtonY, clickerButtonSize - (2 * (clickerButtonSize // 10))):
                isPressingClicker = True
                if autoclickerCost <= points:
                    if getClicker: autoclickers += 1; points -= autoclickerCost; autoclickerCost += 30; getClicker = False

        if event.type == pygame.MOUSEBUTTONUP:
            isPressingPoints = False
            isPressingMulti = False
            isPressingClicker = False
            getPoint = True
            getMulti = True
            getClicker = True

    mouseX, mouseY = pygame.mouse.get_pos()

    clock.tick(60)

    if autoclickersUnlocked and autoclickers != 0:
        #for i in range(autoclickers):
            if gameticks == autoclickerticker:
                points += (1 * autoclickerMultiplier) * autoclickers
                autoclickerticker += autoclickerinterval

    drawPointsButton(pointsButtonX, pointsButtonY, pointsButtonSize)
    drawMultiplierButton(multiplierButtonX, multiplierButtonY, multiplierButtonSize)
    if autoclickersUnlocked: drawClickerButton(clickerButtonX, clickerButtonY, clickerButtonSize)
    showinfo(30, 0)

    if showTicks: showticks(0, windratio[1] - 60)
    if showCursorPos: showcursorpos(0, 35)
    pygame.display.update()
    gameticks += 1