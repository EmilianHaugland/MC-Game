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

player = pygame.Rect(100, (SCREEN_HEIGHT - CAR_HEIGHT) // 2, 60, 20)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

wall = pygame.Rect(-800, 0, 100, SCREEN_HEIGHT)
car1 = pygame.image.load("carh.png").convert_alpha()
car2 = pygame.image.load("car2h.png").convert_alpha()
car3 = pygame.image.load("car3h.png").convert_alpha()
car4 = pygame.image.load("car4h.png").convert_alpha()
car5 = pygame.image.load("car5h.png").convert_alpha()
car6 = pygame.image.load("car6h.png").convert_alpha()

motorcycle = pygame.image.load("motorcycle.png").convert_alpha()

grass = pygame.image.load("grass.png").convert_alpha()

tank = pygame.image.load("tankh.png").convert_alpha()
trailer = pygame.image.load("Trailerh.png").convert_alpha()
motorcycle = pygame.image.load("motorcycle.png").convert_alpha()
motorcycle1 = motorcycle
carnumber = 0

carcrashX = None
carcrashY = None

angle = 0

car_list = [car1, car2, car3, car4, car5, car6, trailer, tank]

font = pygame.font.Font('freesansbold.ttf', 32)

ape = 7

run = True
game_state = "start"

color = (50, 50, 50)

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
    def __init__(self, image, x, y, width, height, speed, lane_index):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=(x, y - 5))
        self.speed = speed
        self.vehicle = image
        self.index = lane_index
        self.bool1 = False
        self.bool2 = False

grassgroup = pygame.sprite.Group()

linegroup = []

cars = pygame.sprite.Group()

def spawn_car():
    lane_index = random.randint(0, NUM_LANES - 1)
    lane_y = lane_positions[lane_index]
    image = random.choice(car_list)
    car_width = CAR_WIDTH
    car_height = CAR_HEIGHT
    speed = random.randint(int(CAR_SPEED) - 10, int(CAR_SPEED))
    if image == trailer:
        speed = CAR_SPEED + 3
        car_width = 675
    if image == tank:
        if Score_value > 5000:
            speed = CAR_SPEED + 20
            car_height = 280
            car_width = 700
        else: 
            return
    y = lane_y + (LANE_WIDTH - car_height) // 2 + LANE_WIDTH // 2

    new_car = Car(image, SCREEN_WIDTH - 600, y, car_width, car_height, speed, lane_index)

    # Don't spawn if there's a collision
    for car in cars:
        if car.rect.colliderect(new_car.rect):
            return
    cars.add(new_car)
    return

class grassclass(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=(x, y - 5))


def spawn_grass(gx, gy):
    size = random.randint(50, 100)
    y = random.randint(gx, gy)
    new_grass = grassclass(grass, 2100, y, size, size)

    for grs in grassgroup:
        if grs.rect.colliderect(new_grass):
            return
    grassgroup.add(new_grass)

switch = False

prob = 0.01

linespeed = 60

evnt = pygame.USEREVENT+1
pygame.time.set_timer(evnt, 50)

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

    # Limit the frame rate to 60 FPS
    clock.tick(60)

    # Checks the score to change difficulty
    if Score_value > 1000 and Score_value < 3000 and CAR_SPEED < 15:
        Score_num = 1.5
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == False:
            liness()
            pygame.time.set_timer(evnt, 250)
            prob = 0.02
            switch = True
    elif Score_value > 3000 and Score_value < 6000 and CAR_SPEED < 20:
        Score_num = 2
        PLAYER_SPEED = 7
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == True:
            liness()
            pygame.time.set_timer(evnt, 200)
            prob = 0.03
            switch = False
    elif Score_value > 6000 and Score_value < 10000 and CAR_SPEED < 25:
        Score_num = 2.5
        PLAYER_SPEED = 10
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == False:
            liness()
            pygame.time.set_timer(evnt, 200)
            prob = 0.05
            switch = True
    elif Score_value > 10000 and Score_value < 15000 and CAR_SPEED < 30:
        Score_num = 3
        PLAYER_SPEED = 15  
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == True:
            liness()
            pygame.time.set_timer(evnt, 150)
            prob = 0.06
            switch = False


    # Event listener
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == KEYDOWN:
            if game_state == "start":
                if event.key == pygame.K_SPACE:
                    liness()
                    pygame.time.set_timer(evnt, 250)
                    linespeed = 7
                    color = (255, 255, 255)
                    game_state = "running"
                    Time = 0
            elif game_state == "game_over":
                pygame.time.set_timer(evnt, 250)
                if event.key == pygame.K_r:
                    # Restart the game
                    color = (255, 255, 255)
                    game_state = "running"
                    Time = 0
                    cars.empty()
                    player.y = (SCREEN_HEIGHT - CAR_HEIGHT) // 2
                    prob = 0.01
                    Score_value = 1
                    Score_num = 1
                    CAR_SPEED = 10
                    carnumber = 0
                    carcrashX = None
                    carcrashY = None
                    PLAYER_SPEED = 5
                elif event.key == pygame.K_q:
                    # Quit the game
                    run = False
        if event.type == evnt:
            liness()

    if game_state != "game_over":
        screen.fill((50,50,50))

    # Spawns the white lines
    for line in linegroup:
        if game_state != "game_over":
            pygame.draw.rect(screen, (color), line)
            line.move_ip(-CAR_SPEED - linespeed, 0)
        if line.colliderect(wall):
            linegroup.remove(line)

    # Show start menu
    if game_state == "start":
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        your_highscore = font.render("Your highscore is " + str(highscore), True, (255, 255, 255))
        screen.blit(your_highscore, (SCREEN_WIDTH // 2 - your_highscore.get_width() // 2, SCREEN_HEIGHT // 2 -50))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

    elif game_state == "running":
        
        if Time == 0:
            Time = pygame.time.get_ticks() / 1000

        # Draw grass
        pygame.draw.rect(screen, (57, 126, 1), pygame.Rect(0, 0, SCREEN_WIDTH, lane_positions[0]))
        pygame.draw.rect(screen, (57, 126, 1), pygame.Rect(0, lane_positions[NUM_LANES - 1] + LANE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Spawns the moving grass
        for grs in grassgroup:
            grs.rect.move_ip(-CAR_SPEED - 7, 0)
            screen.blit(grs.image, grs.rect)
            if grs.rect.colliderect(wall):
                grassgroup.remove(grs)
    
        # Draw white line for the bottom and top lane
        tb_lane_y = lane_positions[NUM_LANES - 1]
        pygame.draw.line(screen, (255, 255, 255), (0, tb_lane_y + LANE_WIDTH), (SCREEN_WIDTH, tb_lane_y + LANE_WIDTH), 4)
        tb_lane_y = lane_positions[NUM_LANES - 5]
        pygame.draw.line(screen, (255, 255, 255), (0, tb_lane_y + LANE_WIDTH - 150), (SCREEN_WIDTH, tb_lane_y + LANE_WIDTH - 150), 4)

        # Spawns the cars
        for car in cars:
            if car.vehicle == tank and car.index == 0:
                cars.remove(car)

            if random.random() < 0.01:
                        car.bool1 = True
                        car.index -= 1

            elif random.random() < 0.01:
                        car.bool2 = True
                        car.index += 1

            if car.bool1:
                if car.index != 0:
                    if car.rect.y > car.y - 220:
                        car.rect.move_ip(0, -10)

            elif car.bool2:
                if car.index != 4:
                    if car.rect.y < car.y + 220:
                        car.rect.move_ip(0, 10)
               
            car.rect.move_ip(-car.speed, 0)
            screen.blit(car.image, car.rect)

            # Check if a car collides with the player
            if car.rect.colliderect(player):
                if Score_value > int(highscore):
                    with open("data.txt", "w") as f:
                        f.write(str(round(Score_value)))
                color = (50, 50, 50)
                game_state = "game_over"
                carcrashX = car.rect.x
                carcrashY = car.rect.y

            # Check if a car collides with another car
            for caar in cars:
                if car.speed == 0:
                    car.speed += 5
                if caar.speed == 0:
                    caar.speed += 5
                if car.rect.colliderect(caar.rect):
                    if car.vehicle != tank:
                        if car.speed > caar.speed:
                            caar.speed += 5
                            car.speed -= 4
                    elif car.vehicle == tank:
                        caar.speed = car.speed

            # Check if a car collides with the wall
            if car.rect.colliderect(wall):
                cars.remove(car)
                carnumber += 1

        # Randomly fires the spawn_car function
        if random.random() < prob:
            spawn_car()

        # Randomly fires the spawn_grass function
        if random.random() < 0.05:
            spawn_grass(1, 125)

        if random.random() < 0.05:
            spawn_grass(980, 1080)

        current_time = pygame.time.get_ticks() / 1000 - Time
        timer(textX, textY, current_time)

        key = pygame.key.get_pressed()
        if key[K_UP] or key[K_w]:
            if player.y > 150:
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
            angle = angle - 1 * 4
            motorcycle1 = pygame.transform.rotate(motorcycle, angle)
        elif angle < 0:
            angle = angle + 1 * 4
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
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 160))
            screen.blit(your_highscore, (SCREEN_WIDTH // 2 - your_highscore.get_width() // 2, SCREEN_HEIGHT // 2 -110))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        if Score_value > int(highscore):
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 110))
            screen.blit(new_highscore_text, (SCREEN_WIDTH // 2 - new_highscore_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 - 5))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

    pygame.display.update()

with open ("AdamsData.txt", "w") as f:
    f.write("Time alive: " + str("{0:.1f}".format(Time)) + " seconds!")
    f.write("\n")
    f.write("The car speed was: " + str(round(CAR_SPEED)) + ", WOW that is difficult")
    f.write("\n")
    f.write("You passed: " + str(carnumber) + " cars!")
    f.write("\n")
    f.write("You crashed at: " + str(player.x + 40) + "X " + str(player.y) + "Y")
    f.write("\n")
    f.write("The car you crashed with was at: " + str(carcrashX) + "X " + str(carcrashY) + "Y")

pygame.quit()