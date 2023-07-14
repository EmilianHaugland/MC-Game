
import pygame

pygame.display.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

car1 = pygame.image.load("imgs\carh.png").convert_alpha()
car2 = pygame.image.load("imgs\car2h.png").convert_alpha()
car3 = pygame.image.load("imgs\car3h.png").convert_alpha()
car4 = pygame.image.load("imgs\car4h.png").convert_alpha()
car5 = pygame.image.load("imgs\car5h.png").convert_alpha()
car6 = pygame.image.load("imgs\car6h.png").convert_alpha()
car7 = pygame.image.load("imgs\car7h.png").convert_alpha()
car8 = pygame.image.load("imgs\car8h.png").convert_alpha()
car9 = pygame.image.load("imgs\car9h.png").convert_alpha()

motorcycle = pygame.image.load("imgs\motorcycle.png").convert_alpha()
motorcycle1 = motorcycle

grass = pygame.image.load("imgs\grass.png").convert_alpha()
tree = pygame.image.load("imgs\Tree.png").convert_alpha()
tree2 = pygame.image.load("imgs\Tree2.png").convert_alpha()

tank = pygame.image.load("imgs\Tankh.png").convert_alpha()
trailer = pygame.image.load("imgs\Trailerh.png").convert_alpha()