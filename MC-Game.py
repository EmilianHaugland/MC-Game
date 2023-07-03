import pygame
import random
import time
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

Time = 0

# Constants for lanes
LINE_X = 1
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
CAR_SPEED = 10
PLAYER_SPEED = 5

# Constants for screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Calculate lane positions
lane_positions = [(SCREEN_HEIGHT - NUM_LANES * LANE_WIDTH) // 2 + x * LANE_WIDTH for x in range(NUM_LANES)]
middle_line_positions = [lane + LANE_WIDTH // 2 for lane in lane_positions]

player = pygame.Rect(180, (SCREEN_HEIGHT - CAR_HEIGHT) // 2, 60, 20)

wall = pygame.Rect(-800, 0, 100, SCREEN_HEIGHT)
car1 = pygame.image.load("car.png")
car2 = pygame.image.load("car2.png")
car3 = pygame.image.load("car3.png")

motorcycle = pygame.image.load("motorcycle.png")

trailer = pygame.image.load("Trailer.png")
motorcycle = pygame.image.load("motorcycle.png")
motorcycle1 = motorcycle
cars = []
carnumber = 0



carcrashX = None
carcrashY = None

angle = 0

car_list = [car1, car2, car3, trailer]


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font('freesansbold.ttf', 32)

ape = random.randint(0,1)

run = True
game_state = "start"

clock = pygame.time.Clock()

def timer(posx, posy, current_time):
    time_text = font.render("Time: " + str("{0:.1f}".format(current_time)), True, (255, 255, 255))
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
        self.rect = self.image.get_rect(center=(x, y - 5))


cars = pygame.sprite.Group()

def spawn_car():
    lane_index = random.randint(0, NUM_LANES - 1)
    lane_y = lane_positions[lane_index]
    image = random.choice(car_list)
    car_width = CAR_WIDTH
    if image == trailer:
        car_width = 675
    car_height = CAR_HEIGHT
    y = lane_y + (LANE_WIDTH - car_height) // 2 + LANE_WIDTH // 2

    new_car = Car(image, SCREEN_WIDTH + 200, y, car_width, car_height)

    new_car = Car(image, SCREEN_WIDTH + 600, y, car_width, car_height)

    for car in cars:
        if car.rect.colliderect(new_car.rect):
            return  # Don't spawn if there's a collision
    cars.add(new_car)
    return

linegroup = []

evnt, t, trail = pygame.USEREVENT+1, round(150 - (CAR_SPEED * 6)), []
pygame.time.set_timer(evnt, t)

def liness():
    y = 315
    lines = pygame.Rect(2100, y, 100, 3)
    linegroup.append(lines)
    y = 465
    lines = pygame.Rect(2100, y, 100, 3)
    linegroup.append(lines)
    y = 615
    lines = pygame.Rect(2100, y, 100, 3)
    linegroup.append(lines)
    y = 765
    lines = pygame.Rect(2100, y, 100, 3)
    linegroup.append(lines)

while run:

    clock.tick(90)  # Limit the frame rate to 90 FPS

    if Score_value > 1000 and Score_value < 3000 and CAR_SPEED < 10:
         Score_num = 1.5
         CAR_SPEED = CAR_SPEED * 1.005
    elif Score_value > 3000 and Score_value < 6000 and CAR_SPEED < 15:
        Score_num = 2
        CAR_SPEED = CAR_SPEED * 1.005
    elif Score_value > 6000 and Score_value < 10000 and CAR_SPEED < 20:
        Score_num = 2.5
        PLAYER_SPEED = 7
        CAR_SPEED = CAR_SPEED * 1.005
    elif Score_value > 10000 and Score_value < 15000 and CAR_SPEED < 30:
        Score_num = 3
        PLAYER_SPEED = 10 
        CAR_SPEED = CAR_SPEED * 1.005
    elif Score_value > 15000 and CAR_SPEED < 45:
        Score_num = 3.5
        PLAYER_SPEED = 15 
        CAR_SPEED = CAR_SPEED * 1.005

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == KEYDOWN:
            if game_state == "start":
                if event.key == pygame.K_SPACE:
                    game_state = "running"
                    Time = 0  # Reset the time when the game starts
            elif game_state == "game_over":
                if event.key == pygame.K_r:
                    # Restart the game
                    game_state = "running"
                    Time = 0  # Reset the time when the game restarts
                    cars.empty()
                    player.y = (SCREEN_HEIGHT - CAR_HEIGHT) // 2
                    Score_value = 1
                    CAR_SPEED = 5
                    carnumber = 0
                    carcrashX = None
                    carcrashY = None
                elif event.key == pygame.K_q:
                    # Quit the game
                    run = False
        if event.type == evnt:
            liness()

    screen.fill((50,50,50))

    if game_state == "start":
        # Show start menu
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        your_highscore = font.render("Your highscore is " + str(highscore), True, (255, 255, 255))
        screen.blit(your_highscore, (SCREEN_WIDTH // 2 - your_highscore.get_width() // 2, SCREEN_HEIGHT // 2 -50))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    elif game_state == "running":
        if Time == 0:
            Time = pygame.time.get_ticks() / 1000
       
        # Draw grass
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 0, SCREEN_WIDTH, lane_positions[0]))
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, lane_positions[NUM_LANES - 1] + LANE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT))

        screen.fill((50,50,50))

        # Draw grass
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, 0, SCREEN_WIDTH, lane_positions[0]))
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(0, lane_positions[NUM_LANES - 1] + LANE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT))
    
        # Draw white line for the bottom and top lane
        tb_lane_y = lane_positions[NUM_LANES - 1]
        pygame.draw.line(screen, (255, 255, 255), (0, tb_lane_y + LANE_WIDTH), (SCREEN_WIDTH, tb_lane_y + LANE_WIDTH), 4)
        tb_lane_y = lane_positions[NUM_LANES - 5]
        pygame.draw.line(screen, (255, 255, 255), (0, tb_lane_y + LANE_WIDTH - 150), (SCREEN_WIDTH, tb_lane_y + LANE_WIDTH - 150), 4)

        for line in linegroup:
         pygame.draw.rect(screen, (255, 255, 255), line)
         line.move_ip(-CAR_SPEED - 15, 0)
         if line.colliderect(wall):
            linegroup.remove(line)

            # Move and draw each car
        for car in cars:
            car.rect.move_ip(-CAR_SPEED, 0)  # Increase the movement amount to make cars go faster
            screen.blit(car.image, car.rect)

            # Check if the car collides with the player
            if car.rect.colliderect(player):
                game_state = "game_over"
                carcrashX = car.rect.x
                carcrashY = car.rect.y

            # Check if the car collides with the wall
            if car.rect.colliderect(wall):
                cars.remove(car)
                carnumber += 1

        # Spawn a new car randomly
        if random.random() < 0.02:  # Adjust the probability to your liking
            spawn_car()

        current_time = pygame.time.get_ticks() / 1000 - Time
        timer(textX, textY, current_time)

        key = pygame.key.get_pressed()
        if key[K_UP] or key[K_w]:
            if player.y > 160:
                if angle < 20:
                    angle = angle + 1 * 2.5
                    motorcycle1 = pygame.transform.rotate(motorcycle, angle)
                player.move_ip(0, -PLAYER_SPEED)
        elif key[K_DOWN] or key[K_s]:
            if player.y < 900:
                if angle > -20:
                    angle = angle - 1 * 2.5
                    motorcycle1 = pygame.transform.rotate(motorcycle, angle)
                player.move_ip(0, PLAYER_SPEED)
        elif angle > 0:
            angle = angle - 1 * 2.5
            motorcycle1 = pygame.transform.rotate(motorcycle, angle)
        elif angle < 0:
            angle = angle + 1 * 2.5
            motorcycle1 = pygame.transform.rotate(motorcycle, angle)

        screen.blit(motorcycle1, (player.x - int(motorcycle1.get_width() / 2 - 20), player.y - int(motorcycle1.get_height() / 2 - 10)))

        position(postextX, postextY)

        show_score(textX, textY)

        Score_value += Score_num

        with open("data.txt", "r") as f:
            highscore = f.read(99999)

    elif game_state == "game_over":
        # Show game over menu
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
        score_text = font.render("You got the score of " + str(round(Score_value)), True, (255, 255, 255))
        new_highscore_text = font.render("You got the new highscore of " + str(round(Score_value)), True, (255, 255, 255))
        your_highscore = font.render("Your highscore is " + highscore, True, (255, 255, 255))
        if Score_value < int(highscore):
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
            screen.blit(your_highscore, (SCREEN_WIDTH // 2 - your_highscore.get_width() // 2, SCREEN_HEIGHT // 2 -100))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        if Score_value > int(highscore):
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(new_highscore_text, (SCREEN_WIDTH // 2 - new_highscore_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()


    if Score_value > int(highscore):
        with open("data.txt", "w") as f:
            f.write(str(round(Score_value)))

with open ("AdamsData.txt", "w") as f:
    f.write("Time alive: " + str("{0:.1f}".format(Time)) + "    " + "Number of cars: " + str(carnumber))
pygame.quit()