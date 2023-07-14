import pygame
import random
from Variables import *
from Functions import *
from Img import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    KEYDOWN,
    QUIT,
)

pygame.init()

linespawn = 2100

# Spawns a set of white lines at startup
for _ in range(9):
    liness(linespawn)
    linespawn -= 250

while run:

    # Limit the frame rate to 90 FPS
    clock.tick(90)

    linetimer += 1

    # Timer to change the line disctance
    if linetimer > linelimit:
        if spawn2:
            linetimer = 0
            liness(2100)

    # Checks the score to change difficulty
    if Score_value > 1000 and Score_value < 3000 and CAR_SPEED < 15:
        Score_num = 1.5
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == False:
            linelimit = 12
            difficulty = "Medium"
            switch = True
    elif Score_value > 3000 and Score_value < 6000 and CAR_SPEED < 20:
        Score_num = 2
        PLAYER_SPEED = 7
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == True:
            difficulty = "Hard"
            switch = False
    elif Score_value > 6000 and Score_value < 10000 and CAR_SPEED < 25:
        Score_num = 2.5
        PLAYER_SPEED = 10
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == False:
            linelimit = 8
            difficulty = "Very hard"
            switch = True
    elif Score_value > 10000 and Score_value < 15000 and CAR_SPEED < 30:
        Score_num = 3
        PLAYER_SPEED = 15  
        CAR_SPEED = CAR_SPEED * 1.005
        if switch == True:
            prob = 0.02
            difficulty = "Extreme"
            switch = False


    # Event listener
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == KEYDOWN:
            if game_state == "start":
                if event.key == pygame.K_SPACE:
                    game_state = "starting"
                    startbool = True
                    Time = 0
                    waiter = 0
                    spawn = False
            elif game_state == "game_over":

                # Restarts the game
                if event.key == pygame.K_r:
                    game_state = "starting"
                    Time = 0
                    linelimit = 20
                    spawn = False
                    spawn2 = True
                    animstart = False
                    startbool= True
                    postextX = -100
                    player.x = -100
                    player.y = (SCREEN_HEIGHT - CAR_HEIGHT) // 2 + 50
                    prob = 0.02
                    difficulty = "Easy"
                    Score_num = 1
                    CAR_SPEED = 10
                    linespeed = 7
                    for car in cars:
                        car.speed = random.randint(10, 15)
                    carnumber = 0
                    PLAYER_SPEED = 5

                # Quits the game
                elif event.key == pygame.K_q:
                    run = False

    screen.fill((50,50,50))

    # Spawns the white lines
    for line in linegroup:
        pygame.draw.rect(screen, (255, 255, 255), line)
        line.move_ip(-CAR_SPEED - linespeed, 0)
        if line.colliderect(wall):
            linegroup.remove(line)
        
    if Time == 0:
        Time = pygame.time.get_ticks() / 1000

    # Draw grass
    pygame.draw.rect(screen, (57, 126, 1), pygame.Rect(0, 0, SCREEN_WIDTH, lane_positions[0]))
    pygame.draw.rect(screen, (57, 126, 1), pygame.Rect(0, lane_positions[NUM_LANES - 1] + LANE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Draw white line for the bottom and top lane
    tb_lane_y = lane_positions[NUM_LANES - 1]
    pygame.draw.line(screen, (255, 255, 255), (0, tb_lane_y + LANE_WIDTH), (SCREEN_WIDTH, tb_lane_y + LANE_WIDTH), 4)
    tb_lane_y = lane_positions[NUM_LANES - 5]
    pygame.draw.line(screen, (255, 255, 255), (0, tb_lane_y + LANE_WIDTH - 150), (SCREEN_WIDTH, tb_lane_y + LANE_WIDTH - 150), 4)

    # Spawns the cars
    for car in cars:
        if car.vehicle == tank and car.index == 0:
            cars.remove(car)

        # Randomly chooses which cars changes lanes
        if car.vehicle != tank and car.rect.x < SCREEN_WIDTH - 200:
            if not car.bool2 and not car.bool1 and random.random() < 0.01:
                car.bool1 = True
                if car.index != 0:            
                    car.index -= 1

            if not car.bool1 and not car.bool2  and random.random() < 0.01:
                car.bool2 = True
                if car.index != 4:
                    car.index += 1
            
        car.rect.move_ip(-car.speed, 0)
        screen.blit(car.image2, car.rect)
            
        # Check if a car collides with the player
        if game_state == "running":
            if car.rect.colliderect(player):
                if Score_value > int(highscore):
                    with open("data.txt", "w") as f:
                        f.write(str(round(Score_value)))
                CAR_SPEED = 0
                linespeed = 0
                linelimit = 0
                waiter = 0
                spawn = False
                spawn2 = False
                for car in cars:
                    car.speed = 0
                carcrashX = car.rect.x
                carcrashY = car.rect.y
                game_state = "game_over"

        # Check if a car collides with another car and changes lane if there is no car in the way
        if game_state != "game_over":
            for othercar in cars:

                if othercar != car and car != othercar:
                    if car.vehicle != tank:

                        # Handles lane change upwards
                        if car.bool1:
                            if car.index != 0:

                                if any(othercar.rect.y < car.rect.y and othercar.rect.y > car.rect.y - 400 and othercar.rect.x > car.rect.x - 700 and othercar.rect.x < car.rect.x + 700 + 200 for othercar in cars):
                                    if car.angle > 0: 
                                        car.angle -= 0.2
                                        car.image2 = pygame.transform.rotate(car.image, car.angle)
                                else:
                                    car.moving = True
                                    
                                if car.moving:
                                    if car.rect.y > car.y - 220:
                                        if car.vehicle != trailer:
                                            if car.angle >= 0 and car.angle < 5:
                                                car.angle += 0.2
                                                car.image2 = pygame.transform.rotate(car.image, car.angle)
                                            elif car.angle >= 0 and car.angle < 2:
                                                car.angle += 0.2
                                                car.image2 = pygame.transform.rotate(car.image, car.angle)
                                            car.rect.move_ip(0, -1)
                                    elif car.rect.y < car.y - 219:
                                        if car.angle > 0:
                                            car.angle -= 0.2
                                            car.image2 = pygame.transform.rotate(car.image, car.angle)

                        # Handles lane change downwards                                        
                        elif car.bool2:
                            if car.index != 4:

                                if any(othercar.rect.y > car.rect.y and othercar.rect.y < car.rect.y + 250 and othercar.rect.x > car.rect.x - 700 and othercar.rect.x < car.rect.x + 700 + 200 for othercar in cars):
                                    if car.angle < 0: 
                                        car.angle += 0.2
                                        car.image2 = pygame.transform.rotate(car.image, car.angle)
                                else:
                                    car.moving = True
                                    
                                if car.moving:
                                    if car.rect.y < car.y + 70:
                                        if car.vehicle != trailer:
                                            if car.angle <= 0 and car.angle > -5:
                                                car.angle -= 0.2
                                                car.image2 = pygame.transform.rotate(car.image, car.angle)
                                            elif car.angle <= 0 and car.angle > -2:
                                                car.angle -= 0.2
                                                car.image2 = pygame.transform.rotate(car.image, car.angle)
                                            car.rect.move_ip(0, 1)
                                    elif car.rect.y > car.y + 69:
                                        if car.angle < 0:
                                            car.angle += 0.2
                                            car.image2 = pygame.transform.rotate(car.image, car.angle)

                    if car.speed < 4:
                        car.speed += 7
                    
                    # Chekcs if two different cars collide and makes sure they dont pass through each other
                    if car.rect.colliderect(othercar.rect):
                        if car.vehicle != tank:
                            if car.speed > othercar.speed:
                                othercar.speed += 5
                                car.speed -= 5
                        elif car.vehicle == tank:
                            othercar.speed = car.speed

        # Check if a car collides with the wall
        if car.rect.colliderect(wall):
            cars.remove(car)
            carnumber += 1

    # Randomly fires the spawn_car function
    if spawn:
        if random.random() < prob:
            spawn_car(Score_value)

    # Randomly fires the spawn_grass function
    if spawn2:
        if random.random() < 0.05:
            spawn_grass(1, 125)

        if random.random() < 0.05:
            spawn_grass(980, 1080)

    screen.blit(motorcycle1, (player.x - int(motorcycle1.get_width() / 2 - 20), player.y - int(motorcycle1.get_height() / 2 - 10)))
    # Spawns the moving grass
    for grs in grassgroup:
        grs.rect.move_ip(-CAR_SPEED - linespeed, 0)
        screen.blit(grs.image, grs.rect)
        if grs.rect.colliderect(wall):
            grassgroup.remove(grs)

    # Player movement and rotation animation
    if game_state == "running":
        key = pygame.key.get_pressed()
        if key[K_UP] or key[K_w]:
            if player.y > 165:
                if angle < 20:
                    angle = angle + 1 * 2.5
                    motorcycle1 = pygame.transform.rotate(motorcycle, angle)
                player.move_ip(0, -PLAYER_SPEED)
        elif key[K_DOWN] or key[K_s]:
            if player.y < 890:
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

        position(postextX, postextY, difficulty)

        show_score(postextX, textY, Score_value)

        current_time = pygame.time.get_ticks() / 1000 - Time
        timer(postextX, textY, current_time)

        Score_value += Score_num

    # Show start menu
    elif game_state == "start":

        # Draws and animates the text up
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        the_highscore = font.render("The highscore is " + str(highscore), True, (255, 255, 255))
        screen.blit(the_highscore, (SCREEN_WIDTH // 2 - the_highscore.get_width() // 2, highscorestarttext))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, pressspacetext))

        waiter += 1

        # Changes the position of the text
        if highscorestarttext > 490 and waiter > 10:
            highscorestarttext = highscorestarttext * 0.99
        if pressspacetext > 540 and waiter > 30:
            pressspacetext = pressspacetext * 0.99


    elif game_state == "starting":

        # Initiates the start cutscene
        if CAR_SPEED < 50 and startbool:
            CAR_SPEED = CAR_SPEED  * 1.005
            for car in cars:
                car.speed = car.speed * 1.006
        elif CAR_SPEED > 10:
            startbool = False
            CAR_SPEED = CAR_SPEED  * 0.99
            for car in cars:
                car.speed = car.speed * 0.99
        else:
            game_state = "running"
            animstart = True
            spawn = True
            startbool = True
            Time = 0
            linelimit = 20
            Score_value = 1

        # Makes the line distance shorter compared to the speed
        if CAR_SPEED < 15 and CAR_SPEED > 10 and startswitch:
            linelimit = 13
            startswitch = False
        elif CAR_SPEED < 25 and CAR_SPEED > 15 and not startswitch:
            linelimit = 10
            startswitch = True
        elif CAR_SPEED < 35 and CAR_SPEED > 25  and startswitch:
            linelimit = 7
            startswitch = False
        elif CAR_SPEED < 50 and CAR_SPEED > 35  and not startswitch:
            linelimit = 5
            startswitch = True

        # Draws and animates the text down
        score_text = font.render("You got the score of " + str(round(Score_value)), True, (255, 255, 255))
        new_highscore_text = font.render("You got the new highscore of " + str(round(Score_value)), True, (255, 255, 255))

        screen.blit(the_highscore, (SCREEN_WIDTH // 2 - the_highscore.get_width() // 2, highscorestarttext))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, pressspacetext))

        if Score_value < int(highscore):
            screen.blit(the_highscore, (SCREEN_WIDTH // 2 - the_highscore.get_width() // 2, highscoretext))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, scoretext))
        
        if Score_value > int(highscore):
            screen.blit(new_highscore_text, (SCREEN_WIDTH // 2 - new_highscore_text.get_width() // 2, highscoretext))
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, gameovertext))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, restarttext))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, quittext))

        # Changes the position of the text
        if highscorestarttext < 1200:
            highscorestarttext = highscorestarttext * 1.01
        if pressspacetext < 1250:
            pressspacetext = pressspacetext * 1.01

        if gameovertext < 1200:
            gameovertext = gameovertext * 1.01
        if scoretext < 1250:
            scoretext = scoretext * 1.01
        if highscoretext < 1300:
            highscoretext = highscoretext * 1.01
        if restarttext < 1350:
            restarttext = restarttext * 1.01
        if quittext < 1400:
            quittext = quittext * 1.01

    # Show game over menu
    elif game_state == "game_over":
        
        # Draws and animates the text up
        score_text = font.render("You got the score of " + str(round(Score_value)), True, (255, 255, 255))
        new_highscore_text = font.render("You got the new highscore of " + str(round(Score_value)), True, (255, 255, 255))

        if Score_value < int(highscore):
            screen.blit(the_highscore, (SCREEN_WIDTH // 2 - the_highscore.get_width() // 2, highscoretext))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, scoretext))
        
        if Score_value > int(highscore):
            screen.blit(new_highscore_text, (SCREEN_WIDTH // 2 - new_highscore_text.get_width() // 2, highscoretext))
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, gameovertext))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, restarttext))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, quittext))

        waiter += 1

        # Changes the position of the text
        if gameovertext > 440 and waiter > 10:
            gameovertext = gameovertext * 0.99
        if scoretext > 490 and waiter > 30:
            scoretext = scoretext * 0.99
        if highscoretext > 540 and waiter > 50:
            highscoretext = highscoretext * 0.99
        if restarttext > 590 and waiter > 70:
            restarttext = restarttext * 0.99
        if quittext > 640 and waiter > 90:
            quittext = quittext * 0.99

    # Initiates the player animation after the cutscene
    if animstart:
        if player.x < 100:
            player.move_ip(2, 0)
        if postextX < 30:
            postextX += 2

    # Reads the highscore data for saved file
    with open("data.txt", "r") as f:
        highscore = f.read(99999)

    pygame.display.update()

# Saving Adams data
with open ("AdamsData.txt", "w") as f:
    f.write("Time alive: " + str("{0:.1f}".format(Time)) + " seconds!")
    f.write("\n")
    f.write("The difficulty was: " + difficulty + ", WOW that is difficult")
    f.write("\n")
    f.write("You passed: " + str(carnumber) + " cars!")
    f.write("\n")
    f.write("You crashed at: " + str(player.x + 40) + "X " + str(player.y) + "Y")
    f.write("\n")
    f.write("The car you crashed with was at: " + str(carcrashX) + "X " + str(carcrashY) + "Y")

pygame.quit()