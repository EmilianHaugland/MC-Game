
import pygame
import random
from Img import *
from Variables import *

def timer(posx, posy, current_time):
    time_text = font.render("Time: " + str("{0:.1f}".format(current_time)), True, (255, 255, 255))
    screen.blit(time_text, (posx, posy + 50))

def position(posx, posy, diffi):
    position_textY = font.render("PlayerY : " + str(player.y), True, (255, 255, 255))
    diff = font.render("Difficulty: " + diffi, True, (255, 255, 255))
    screen.blit(position_textY, (posx, posy - 50))
    screen.blit(diff, (posx, posy))

def show_score(posx, posy, score):
    score_text = font.render("Score: " + str(round(score)), True, (255, 255, 255))
    screen.blit(score_text, (posx, posy))

class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed, lane_index):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (width, height))
        self.image2 = self.image
        self.rect = self.image.get_rect(center=(x, y - 5))
        self.speed = speed
        self.vehicle = image
        self.index = lane_index
        self.bool1 = False
        self.bool2 = False
        self.angle = 0
        self.moving = False

def spawn_car(score):
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
        if score > 5000:
            speed = CAR_SPEED + 20
            car_height = 280
            car_width = 700
        else: 
            return
    y = lane_y + (LANE_WIDTH - car_height) // 2 + LANE_WIDTH // 2

    new_car = Car(image, SCREEN_WIDTH + 600, y, car_width, car_height, speed, lane_index)

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
    image = random.choice(nature_list)

    if image == tree or image == tree2:
        size = random.randint(250, 350)
        y = random.randint(gx - 100, gy - 145)

    new_grass = grassclass(image, 2100, y, size, size)

    for grs in grassgroup:
        if grs.rect.colliderect(new_grass):
            return
    grassgroup.add(new_grass)

def liness(x):

    lines = pygame.Rect(x, 315, 100, 3)
    linegroup.append(lines)

    lines = pygame.Rect(x, 465, 100, 3)
    linegroup.append(lines)

    lines = pygame.Rect(x, 615, 100, 3)
    linegroup.append(lines)

    lines = pygame.Rect(x, 765, 100, 3)
    linegroup.append(lines)
