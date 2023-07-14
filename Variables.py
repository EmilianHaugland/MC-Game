
import pygame
from Img import *

pygame.init()

highscore = 0

with open("data.txt", "r") as f:
    highscore = f.read(99999)

Time = 0

# Constants for lanes
LINE_X = 1
LANE_WIDTH = 150
NUM_LANES = 5

# player position
postextX = -150
postextY = 1000

# Score
Score_value = 1
Score_num = 1
textY = 30
# Vehicle size and speed
CAR_WIDTH = 250
CAR_HEIGHT = 140
CAR_SPEED = 10
PLAYER_SPEED = 5

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Calculate lane positions
lane_positions = [(SCREEN_HEIGHT - NUM_LANES * LANE_WIDTH) // 2 + x * LANE_WIDTH for x in range(NUM_LANES)]

player = pygame.Rect(-100, (SCREEN_HEIGHT - CAR_HEIGHT) // 2 + 50, 60, 20)

animstart = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

wall = pygame.Rect(-1100, 0, 100, SCREEN_HEIGHT)

carnumber = 0

carcrashX = None
carcrashY = None

angle = 0

difficulty = "Easy"

font = pygame.font.Font('freesansbold.ttf', 32)

start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
the_highscore = font.render("The highscore is " + str(highscore), True, (255, 255, 255))

game_over_text = font.render("Game Over", True, (255, 255, 255))
restart_text = font.render("Press R to Restart", True, (255, 255, 255))
quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
the_highscore = font.render("The highscore is " + highscore, True, (255, 255, 255))

gameovertext = 1200
scoretext = 1250
highscoretext = 1300
restarttext = 1350
quittext = 1400
highscorestarttext = 1200
pressspacetext = 1250
waiter = 0

linespeed = 7

linetimer = 0

linelimit = 15

run = True
game_state = "start"

switch = False

startbool = False
startswitch = True

spawn = True
spawn2 = True

prob = 0.02

nature_list = [grass, tree, tree2]

car_list = [car1, car2, car3, car4, car5, car6, car7, car8, car9, trailer, tank]

grassgroup = pygame.sprite.Group()

linegroup = []

cars = pygame.sprite.Group()

clock = pygame.time.Clock()