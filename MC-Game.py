import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Constants for lanes
LANE_WIDTH = 150
NUM_LANES = 5

# Constants for score
Score_value = 1
textX = 30
textY = 30
# Constants for car dimensions and speed
CAR_WIDTH = 160
CAR_HEIGHT = 100
CAR_SPEED = 5
PLAYER_SPEED = 5

# Constants for screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Calculate lane positions and middle line positions
lane_positions = [(SCREEN_HEIGHT - NUM_LANES * LANE_WIDTH) // 2 + x * LANE_WIDTH for x in range(NUM_LANES)]
middle_line_positions = [lane + LANE_WIDTH // 2 for lane in lane_positions]

player = pygame.Rect(200, (SCREEN_HEIGHT - CAR_HEIGHT) // 2, 35, 50)


wall = pygame.Rect(-500, 0, 100, SCREEN_HEIGHT)
cars = []

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font('freesansbold.ttf', 32)

run = True

clock = pygame.time.Clock()

def show_score(textX, textY):
    score_text = font.render("Score: " + str(round(Score_value)), True, (255, 255, 255))
    screen.blit(score_text, (textX, textY))


def spawn_car():
    lane_index = random.randint(0, NUM_LANES - 1)
    lane_y = lane_positions[lane_index]
    new_car = pygame.Rect(SCREEN_WIDTH, lane_y + (LANE_WIDTH - CAR_HEIGHT) // 2, CAR_WIDTH, CAR_HEIGHT)
    for car in cars:
        if car.colliderect(new_car):
            return  # Don't spawn if there's a collision
    cars.append(new_car)
    return

while run:
    clock.tick(60)  # Limit the frame rate to 60 FPS

    CAR_SPEED = CAR_SPEED * 1.0003

    PLAYER_SPEED = PLAYER_SPEED * 1.0001

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    screen.fill((0,0,0))

    # Draw the lanes
    for lane_y, middle_line_y in zip(lane_positions, middle_line_positions):
        pygame.draw.line(screen, (255, 255, 255), (0, lane_y), (SCREEN_WIDTH, lane_y), 4)

    # Draw white line for the bottom lane
    bottom_lane_y = lane_positions[NUM_LANES - 1]
    pygame.draw.line(screen, (255, 255, 255), (0, bottom_lane_y + LANE_WIDTH), (SCREEN_WIDTH, bottom_lane_y + LANE_WIDTH), 4)

    # Draw grass
    pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 0, SCREEN_WIDTH, lane_positions[0]))
    pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, lane_positions[NUM_LANES - 1] + LANE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.draw.rect(screen, (0, 255, 0), player)

    # Move and draw each car
    for car in cars:
        car.move_ip(-CAR_SPEED, 0)  # Increase the movement amount to make cars go faster
        pygame.draw.rect(screen, (255, 0, 0), car)

        # Check if the car collides with the player
        if car.colliderect(player):
            run = False

        # Check if the car collides with the wall
        if car.colliderect(wall):
            cars.remove(car)

    # Spawn a new car randomly
    if random.random() < 0.02:  # Adjust the probability to your liking
        spawn_car()

    key = pygame.key.get_pressed()
    if key[K_UP]:
        player.move_ip(0, -PLAYER_SPEED)
    elif key[K_DOWN]:
        player.move_ip(0, PLAYER_SPEED)

    Score_value = Score_value * 1.0005 + 0.1
    
    show_score(textX, textY)
    pygame.display.update()
print("You got the score of", round(Score_value))
pygame.quit()