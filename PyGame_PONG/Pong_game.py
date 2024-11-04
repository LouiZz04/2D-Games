import pygame
import random
import math
import enum
import time

class gamemode(enum.Enum):
    Start=enum.auto()
    Playing=enum.auto()
    Gameover=enum.auto()

def movingplayers(keys, p1_position, p2_position, height, dt, rate):

    if keys[pygame.K_w]: 
        p1_position = p1_position - 200 * rate * dt if p1_position > 0 else 0
    if keys[pygame.K_s]: 
        p1_position = p1_position + 200 * rate * dt if p1_position < height - height/5.1 else height - height/5.1

    if keys[pygame.K_UP]:
        p2_position = p2_position - 200 * rate * dt if p2_position > 0 else 0
    if keys[pygame.K_DOWN]:
        p2_position = p2_position + 200 * rate * dt if p2_position < height - height/5.1 else height - height/5.1

    return p1_position, p2_position

def ballbouncing(counter, angle, ball_position, radius, height, width, p1_position, p2_position) -> float:

    bounce = False

    # bounce on the upper and lower boundaries
    if ball_position.y <= radius or ball_position.y >= height-radius:
        angle = -angle

    # player bounce
    if counter>=30 and ball_position.x <= 30 and p1_position < ball_position.y < p1_position + height/5.1:
        alpha = abs(angle - 180) # angle between x axis and the direction
        angle = 360-alpha if angle > 180 else alpha
        # knowing that the positive sense is clockwise
        # and to keep the ball on the same y direction i needed to check whether the angle
        # was over or under the x axis to redirect my ball
        # having alpha in the case always in the second or third quadrant
        bounce = True
        counter = 0


    elif counter>=30 and ball_position.x >= width - 30 and p2_position < ball_position.y < p2_position + height/5.1:
        angle = 180 - angle if angle < 90 else 180 + 360 - angle
        bounce = True
        counter = 0

    return counter, bounce, angle


def main():
    pygame.init()
    width, height = 840, 420
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    dt=0
    game = gamemode.Start
    rate , nb_of_bounces = 1, 0 # speed up the ball after every 10 bounces
    bounce = False

    counter = 0 
    # sometimes the ball bounces on the same player multiple times
    # so counter was created so that the ball is allowed to bounce on a player
    # once every half a second or more

    # colors
    white = 250, 250, 250
    black = 0,0,0
    grey = 150, 150, 150

    # position of ball along x and y
    ball_position=pygame.Vector2(width/2, height/2)

    # diretion of the ball in polar then changing to cartisian
    angle = random.randint(-45, 45)
    angle = angle+180 if random.randint(0,1)==1 else angle
    angle = angle if angle>=0 else 360 - angle # to keep my angle positive 
    radius = height/30

    # positions of player 1 and 2 along y since they move in 1D
    p1_position = p2_position = height/2 -height/10.2 # initially centered
    p1_prev = p2_prev = 0 
    # p1 and p2 _prev is used for the ball movement with respect for the 
    # player if moving upwards or downwards, read (if bounce) line 164

    # players scores 
    p1_score = p2_score = 0

    # font
    font = pygame.font.SysFont("Arial", 50)
    p1font = font.render(f"{p1_score}", False, grey)
    p2font = font.render(f"{p2_score}", False, grey)

    fonttxt = pygame.font.SysFont("Arial", 30)
    start = fonttxt.render("press SPACE     to start", False, grey)
    gameover = fonttxt.render("", False, grey)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        bounce = False
        counter += 1

        # check gameplay
        if game == gamemode.Start:
            if keys[pygame.K_SPACE]:
                game = gamemode.Playing
                start = fonttxt.render("", False, grey)

        elif game == gamemode.Gameover:
            if keys[pygame.K_SPACE]:
                game = gamemode.Start
                gameover = fonttxt.render("", False, grey)
                time.sleep(0.1) 
                # because without delay the same space key pressed will initiate gamemode.Playing

                # return defaults
                p1_position = p2_position = height/2 -height/10.2
                ball_position.x = width/2
                ball_position.y = height/2

                p1_score=0
                p2_score=0
                rate = 1
                nb_of_bounces=0

                angle = random.randint(-45, 45)
                angle = angle+180 if random.randint(0,1)==1 else angle
                angle = angle if angle>=0 else 360 - angle

                p1font = font.render(f"{p1_score}", False, grey)
                p2font = font.render(f"{p2_score}", False, grey)
                start = fonttxt.render("press SPACE     to start", False, grey)


        elif game == gamemode.Playing:
            # moving players 1 and 2
            p1_prev, p2_prev = p1_position, p2_position
            p1_position , p2_position = movingplayers(keys, p1_position, p2_position, height, dt, rate)

            # bouncing the ball over the edges and the players
            counter, bounce, angle = ballbouncing(counter, angle, ball_position, radius, height, width, p1_position, p2_position)

            # game over
            if ball_position.x <= radius or ball_position.x >= width - radius:
                game = gamemode.Gameover
                gameover = fonttxt.render("GAME   OVER", False, grey)
                continue

            # position of ball
            if nb_of_bounces % 5 == 0 and nb_of_bounces != 0:
                rate = rate + 0.005
            ball_position.x += 250 * rate * dt * math.cos(angle * math.pi / 180)
            ball_position.y += 250 * rate * dt * math.sin(angle * math.pi / 180)



            if bounce:
                nb_of_bounces+=1
                if ball_position.x>width/2: 
                    p2_score+=1
                    p2font= font.render(f"{p2_score}", False, grey)

                    if p2_prev > p2_position: angle = angle + 20 if angle + 20 < 225 else 225 # upwards
                    elif p2_prev < p2_position: angle = angle - 20 if angle -20 > 135 else 135 # downwards

                else: 
                    p1_score+=1
                    p1font= font.render(f"{p1_score}", False, grey)

                    if p1_prev > p1_position: 
                        angle = angle - 20
                    if angle < 0: 
                        angle = 360 - angle
                        angle = angle if angle > 315 else 315
                    elif p1_prev < p2_position: 
                        angle = angle + 20 
                    if angle >= 360: 
                        angle = angle - 360
                        angle = angle if angle < 45 else 45
                    # different approach fromn p2 since the angle changes sometimes from + to -


            

        # Draw background
        screen.fill(black)
        pygame.draw.rect(screen, grey, (5, 5, width-10, height-10), 5) # border
        pygame.draw.line(screen, grey, (width/2, 5), (width/2, height-5), 5) # middle line

        screen.blit(p1font, (width/2 - 67, 10))
        screen.blit(p2font, (width/2 + 50, 10))
        screen.blit(start, (width/2 - 200, height - 50))
        screen.blit(gameover, (width/2 - 100, height - 50))

        # Drawing players 1 and 2
        pygame.draw.rect(screen, white, (10, p1_position, 20, height/5.1), 0, 100)
        pygame.draw.rect(screen, white, (width - 30, p2_position, 20, height/5.1), 0, 100)

        # Drawing the ball
        pygame.draw.circle(screen, white, ball_position, radius) # radius = height/21

        pygame.display.flip()

        dt = clock.tick(60)/1000


    pygame.quit()


if __name__ =="__main__" : main()