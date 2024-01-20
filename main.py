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


def loadsave(dataindex: int | str, vartype = int, toprint = ''):
    one = "<class '"
    two = "'>"
    with open(SAVEFILE, 'rt') as savein:
        gottensave = savein.read()
        sgsave = gottensave.split('\n')
        if type(dataindex) == int or type(dataindex) == bool: gottendata = sgsave[dataindex].split(':')
        else:
            for i in range(len(sgsave)):
                if sgsave[i].split(':')[1] == dataindex:
                    print(f'"{dataindex}" found in {i}({sgsave[i]})!')
                    gottendata = sgsave[i].split(':')
                    dataindex = i
                    break
                #print(f'"{dataindex}" not in {i}({sgsave[i]})...')

        if toprint == '': toprint = f'accessed {dataindex}({gottendata[1]}) as {str(vartype).removeprefix(one).removesuffix(two)}'
        truedata = vartype(gottendata[0])

        if gottendata[0].casefold() == 'false': truedata = False
        elif gottendata[0].casefold() == 'true': truedata = True

        print(toprint + f', with a value of {str(truedata)}\n')
        return truedata

if not Path(SAVEFILE).exists():
    print('no savefile detected! creating new...')
    with open(SAVEFILE, 'xt') as save404:
        save404.write('''0:points
1:pointsMultiplier
10:pMultiCost
false:autoclickersUnlocked
0:autoclickers
1:autoclickerMultiplier
40:autoclickerCost
600:autoclickerinterval
20:acMultiCost
20:acIntervalCost''')
    print('new savefile successfully created')



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
smallfont = pygame.font.Font('freesansbold.ttf', 15)
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

clickerMultiButtonX = 59
clickerMultiButtonY = 387
clickerMultiButtonSize = clickerButtonSize // 5

clickerIntervalButtonX = 40
clickerIntervalButtonY = 367
clickerIntervalButtonSize = clickerButtonSize // 5
#buttons end

#mouse things
mouseX = 0
mouseY = 0
extraMouseRange = 5
##buttonpressed bools
isPressingPoints = False
isPressingMulti = False
isPressingClicker = False
isPressingClickerMulti = False
isPressingClickerInterval = False
##buttonpressed bools end
#mouse things end

#button bools
getPoint = True
getMulti = True
getClicker = True
getClickerMulti = True
getClickerInterval = True
#button bools end

#points
points = 0 + loadsave('points')
pointsMultiplier = 0 + loadsave('pointsMultiplier')
pMultiCost = loadsave('pMultiCost')
if pointsMultiplier == 0: pointsMultiplier = 1
#points end

#autoclickers
autoclickersUnlocked = loadsave('autoclickersUnlocked', bool)
#print(f'autoclickersUnlocked:{autoclickersUnlocked}')
autoclickers = 0 + loadsave('autoclickers')
autoclickerMultiplier = 0 + loadsave('autoclickerMultiplier')
autoclickerCost = 0 + loadsave('autoclickerCost')
autoclickerinterval = 0 + loadsave('autoclickerinterval')
autoclickerticker = autoclickerinterval
autoclickerCost = 0 + loadsave('autoclickerCost')
acMultiCost = 0 + loadsave('acMultiCost')
acIntervalCost = 0 + loadsave('acIntervalCost')
if autoclickerMultiplier == 0: autoclickerMultiplier = 1
if autoclickersUnlocked == None: autoclickersUnlocked = False
if pointsMultiplier >= 10: autoclickersUnlocked = True
#autoclickers end

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
{autoclickerinterval}:autoclickerinterval
{acMultiCost}:acMultiCost
{acIntervalCost}:acIntervalCost''')
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

def drawClickerMultiButton(x, y, size):
    pygame.draw.circle(screen, (125, 100, 150), (x, y), size)
    buttonInnerColor = 200
    if isPressingClickerMulti: buttonInnerColor -= 100
    pygame.draw.circle(screen, (buttonInnerColor, buttonInnerColor, buttonInnerColor), (x, y), size - (2 * (size // 10)))
    #shopclicker = storefont.render(f'AC', True, (255, 255, 255))
    #screen.blit(shopclicker, (x - 20, y - 13))

def drawClickerIntervalButton(x, y, size):
    pygame.draw.circle(screen, (125, 100, 150), (x, y), size)
    buttonInnerColor = 200
    if isPressingClickerInterval: buttonInnerColor -= 100
    pygame.draw.circle(screen, (buttonInnerColor, buttonInnerColor, buttonInnerColor), (x, y), size - (2 * (size // 10)))
    #shopclicker = storefont.render(f'AC', True, (255, 255, 255))
    #screen.blit(shopclicker, (x - 20, y - 13))


def showticks(x, y):
    tick = smallfont.render(f'tick:{gameticks}', True, (255, 255, 255))
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
    poi = smallfont.render(f'points: {points}', True, (255, 255, 255))
    screen.blit(poi, (x, y))
    mul = smallfont.render(f'points multiplier(PM): {pointsMultiplier}', True, (255, 255, 255))
    screen.blit(mul, (x, y + 33))
    if autoclickersUnlocked:
        aclickers = smallfont.render(f'autoclickers(AC): {autoclickers}', True, (255, 255, 255))
        screen.blit(aclickers, (x, y + 66))
        aclickersmulti = smallfont.render(f'AC Multiplier: {autoclickerMultiplier}', True, (255, 255, 255))
        screen.blit(aclickersmulti, (x, y + 101))
        aclickersmulti = smallfont.render(f'AC interval: {autoclickerinterval}', True, (255, 255, 255))
        screen.blit(aclickersmulti, (x, y + 136))



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

            if event.key == pygame.K_p: print(f'mouseX:{mouseX},mouseY:{mouseY}')

            if event.key == pygame.K_RETURN: points += 1 * pointsMultiplier

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
                
            elif isWithinRange(mouseX, mouseY, clickerMultiButtonX, clickerMultiButtonY, clickerMultiButtonSize - (2 * (clickerMultiButtonSize // 10))):
                isPressingClickerMulti = True
                if acMultiCost <= points:
                    if getClickerMulti: autoclickerMultiplier += 1; points -= acMultiCost; acMultiCost += 25; getClickerMulti = False

            elif isWithinRange(mouseX, mouseY, clickerIntervalButtonX, clickerIntervalButtonY, clickerIntervalButtonSize - (2 * (clickerIntervalButtonSize // 10))) and autoclickerinterval > 1:
                isPressingClickerInterval = True
                if acIntervalCost <= points:
                    if getClickerInterval: autoclickerinterval -= 10; points -= acIntervalCost; acIntervalCost += 25; getClickerInterval = False

        if event.type == pygame.MOUSEBUTTONUP:
            isPressingPoints = False
            isPressingMulti = False
            isPressingClicker = False
            isPressingClickerMulti = False
            isPressingClickerInterval = False
            getPoint = True
            getMulti = True
            getClicker = True
            getClickerMulti = True
            getClickerInterval = True

    mouseX, mouseY = pygame.mouse.get_pos()

    clock.tick(60)

    if autoclickersUnlocked and autoclickers != 0:
        #for i in range(autoclickers):
            #if gameticks > 2 and 
            if gameticks >= autoclickerticker:
                points += (1 * autoclickerMultiplier) * autoclickers
                autoclickerticker += autoclickerinterval

    autoclickerinterval = limitmin(autoclickerinterval, 0)

    drawPointsButton(pointsButtonX, pointsButtonY, pointsButtonSize)
    drawMultiplierButton(multiplierButtonX, multiplierButtonY, multiplierButtonSize)
    if autoclickersUnlocked:
        drawClickerButton(clickerButtonX, clickerButtonY, clickerButtonSize)
        drawClickerMultiButton(clickerMultiButtonX, clickerMultiButtonY, clickerMultiButtonSize)
        drawClickerIntervalButton(clickerIntervalButtonX, clickerIntervalButtonY, clickerIntervalButtonSize)
    showinfo(2, 0)

    if showTicks: showticks(0, windratio[1] - 60)
    if showCursorPos: showcursorpos(0, 35)
    pygame.display.update()
    gameticks += 1