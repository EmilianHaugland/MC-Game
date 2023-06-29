import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    KEYDOWN,
    QUIT,
)

pygame.init()

highscore = 0

with open("data.txt", "r") as f:
    highscore = f.read(99999)

print(highscore)

# Constants for lanes
LANE_WIDTH = 150
NUM_LANES = 5

# player position
postextX = 30
postextY = 1000

# Constants for score
Score_value = 1
Score_num = 1
textX = 30
textY = 30
# Constants for car dimensions and speed
CAR_WIDTH = 250
CAR_HEIGHT = 140
CAR_SPEED = 5
PLAYER_SPEED = 5

# Constants for screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Calculate lane positions
lane_positions = [(SCREEN_HEIGHT - NUM_LANES * LANE_WIDTH) // 2 + x * LANE_WIDTH for x in range(NUM_LANES)]
middle_line_positions = [lane + LANE_WIDTH // 2 for lane in lane_positions]

player = pygame.Rect(200, (SCREEN_HEIGHT - CAR_HEIGHT) // 2, 35, 50)


wall = pygame.Rect(-500, 0, 100, SCREEN_HEIGHT)
cars = []
carnumber = 0

car1 = pygame.image.load("car.png")
#car2 = pygame.image.load("car2.png")
car3 = pygame.image.load("car3.png")
motorcycle = pygame.image.load("motorcycle.png")

car_list = [car1, car3]


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font('freesansbold.ttf', 32)

ape = random.randint(0,1)

run = True

clock = pygame.time.Clock()

def timer(posx, posy):
    Time = pygame.time.get_ticks() / 1000
    time_text = font.render("Time: " + str("{0:.1f}".format(Time)), True, (255, 255, 255))
    screen.blit(time_text, (posx, posy + 50))

def position(posx, posy):
    position_textY = font.render("PlayerY : " + str(player.y), True, (255, 255, 255))
    diff = font.render("Car speed: " + str(round(CAR_SPEED)), True, (255, 255, 255))
    screen.blit(position_textY, (posx, posy - 50))
    screen.blit(diff, (posx, posy))

def show_score(posx, posy):
    score_text = font.render("Score: " + str(round(Score_value)), True, (255, 255, 255))
    screen.blit(score_text, (posx, posy))

class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))


cars = pygame.sprite.Group()

# ...

def spawn_car():
    lane_index = random.randint(0, NUM_LANES - 1)
    lane_y = lane_positions[lane_index]
    image = random.choice(car_list)
    car_width = CAR_WIDTH
    car_height = CAR_HEIGHT
    y = lane_y + (LANE_WIDTH - car_height) // 2 + LANE_WIDTH // 2
    new_car = Car(image, SCREEN_WIDTH + 200, y, car_width, car_height)
    for car in cars:
        if car.rect.colliderect(new_car.rect):
            return  # Don't spawn if there's a collision
    cars.add(new_car)
    return

while run:
    clock.tick(90)  # Limit the frame rate to 60 FPS

    if Score_value > 1000 and Score_value < 3000 and CAR_SPEED < 10:
         Score_num = 1.5
         CAR_SPEED = CAR_SPEED * 1.01
    elif Score_value > 3000 and Score_value < 6000 and CAR_SPEED < 15:
        Score_num = 2
        CAR_SPEED = CAR_SPEED * 1.01
    elif Score_value > 6000 and Score_value < 10000 and CAR_SPEED < 20:
        Score_num = 2.5
        PLAYER_SPEED = 7
        CAR_SPEED = CAR_SPEED * 1.01
    elif Score_value > 10000 and Score_value < 15000 and CAR_SPEED < 30:
        Score_num = 3
        PLAYER_SPEED = 10 
        CAR_SPEED = CAR_SPEED * 1.01
    PLAYER_SPEED = PLAYER_SPEED * 1.0001

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    screen.fill((50,50,50))

    # Draw the lanes
    for lane_y, middle_line_y in zip(lane_positions, middle_line_positions):
        pygame.draw.line(screen, (255, 255, 255), (0, lane_y), (SCREEN_WIDTH, lane_y), 4)

    # Draw white line for the bottom lane
    bottom_lane_y = lane_positions[NUM_LANES - 1]
    pygame.draw.line(screen, (255, 255, 255), (0, bottom_lane_y + LANE_WIDTH), (SCREEN_WIDTH, bottom_lane_y + LANE_WIDTH), 4)

    # Draw grass
    pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 0, SCREEN_WIDTH, lane_positions[0]))
    pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, lane_positions[NUM_LANES - 1] + LANE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.blit(motorcycle, player)

    # Move and draw each car
    for car in cars:
        car.rect.move_ip(-CAR_SPEED, 0)  # Increase the movement amount to make cars go faster
        screen.blit(car.image, car.rect)

        # Check if the car collides with the player
        if car.rect.colliderect(player):
            run = False

        # Check if the car collides with the wall
        if car.rect.colliderect(wall):
            cars.remove(car)
            carnumber += 1

    # Spawn a new car randomly
    if random.random() < 0.02:  # Adjust the probability to your liking
        spawn_car()

    key = pygame.key.get_pressed()
    if key[K_UP] or key[K_w]:
        player.move_ip(0, -PLAYER_SPEED)
    elif key[K_DOWN] or key[K_s]:
        player.move_ip(0, PLAYER_SPEED)

    position(postextX, postextY)

    timer(textX, textY)

    show_score(textX, textY)

    Score_value += Score_num

    pygame.display.update()


if Score_value > float(highscore):
    with open("data.txt", "w") as f:
        f.write(str(round(Score_value)))

pygame.quit()