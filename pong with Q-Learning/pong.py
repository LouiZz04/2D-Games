import pygame
import random
import math
import enum
import time

class gamemode(enum.Enum):
    Start=enum.auto()
    Playing=enum.auto()
    Gameover=enum.auto()

pygame.init()


#colors
white = 250, 250, 250
black = 0,0,0
grey = 150, 150, 150

#fonts
font = pygame.font.SysFont("Arial", 50)
fonttxt = pygame.font.SysFont("Arial", 30)

#movement
movements = ["UP", "DOWN", "NOTHING"]
rrate = 1


# Human against trained agent
class Pong():

    def __init__(self, width=840, height=420):

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((840, 420))

        self.reset()


    def reset(self):
        self.clock = pygame.time.Clock()
        self.dt=0

        self.game = gamemode.Start
    
        self.rate = 1
        self.nb_of_bounces = 0
        self.bounce = False

        self.counter = 0

        self.ball_position=[self.width/2, self.height/2]
        r = random.randint(-45, 45)
        r = r+180 if random.randint(0,1) == 1 else r
        self.angle = r if r>=0 else 360-r

        self.radius = self.height/30

        self.p1_position = self.p2_position = self.height/2 - self.height/10.2
        self.p1_prev = self.p2_prev = 0

        self.p1_score = self.p2_score = 0


        self.p1font = font.render(f"{self.p1_score}", False, grey)
        self.p2font = font.render(f"{self.p1_score}", False, grey)
        self.start = fonttxt.render("press SPACE     to start", False, grey)
        self.gameover = fonttxt.render("GAME   OVER", False, grey)
        self.aitxt = fonttxt.render("AI", False, grey)
        self.Human = fonttxt.render("Hum.", False, grey)

        self.showstart = True
        self.showgameover = False

        self.keys = any

    def gameplay(self, ai_action):
        global rrate

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, self.p1_position, self.ball_position[1]

        self.keys = pygame.key.get_pressed()
        self.counter += 1

        # check gameplay
        if self.game == gamemode.Start:
            if self.keys[pygame.K_SPACE]:
                self.game = gamemode.Playing
                self.showstart = False

        elif self.game == gamemode.Gameover:
            if self.keys[pygame.K_SPACE]: 
                time.sleep(0.1)
                self.reset()

        elif self.game == gamemode.Playing:

            # moving players 1 and 2
            self.p1_prev, self.p2_prev = self.p1_position, self.p2_position
            self.p2_position = movingplayers(self.keys, self.p2_position, self.height, self.dt, self.rate)
            self.p1_position = move(ai_action, self.p1_position, self.height)

            # bouncing the ball over the edges and the players
            self.counter, self.bounce, self.angle = ballbouncing(self.counter, self.angle, self.ball_position, self.radius, self.height, self.width, self.p1_position, self.p2_position)

            # game over
            if self.ball_position[0] <= self.radius or self.ball_position[0] >= self.width - self.radius:
                self.game = gamemode.Gameover
                self.showgameover = True


            else:
                # position of ball
                if self.nb_of_bounces % 5 == 0 and self.nb_of_bounces != 0:
                    self.rate = self.rate + 0.005
                    rrate = self.rate
                self.ball_position[0] += 250 * self.rate * self.dt * math.cos(self.angle * math.pi / 180)
                self.ball_position[1] += 250 * self.rate * self.dt * math.sin(self.angle * math.pi / 180)



                if self.bounce:
                    self.nb_of_bounces+=1
                    if self.ball_position[0]>self.width/2: 
                        self.p2_score+=1
                        self.p2font= font.render(f"{self.p2_score}", False, grey)

                        if self.p2_prev > self.p2_position: self.angle = self.angle + 20 if self.angle + 20 < 225 else 225 # upwards
                        elif self.p2_prev < self.p2_position: self.angle = self.angle - 20 if self.angle -20 > 135 else 135 # downwards

                    else: 
                        self.p1_score+=1
                        self.p1font= font.render(f"{self.p1_score}", False, grey)

                        if self.p1_prev > self.p1_position: 
                            self.angle = self.angle - 20
                        if self.angle < 0: 
                            self.angle = 360 - self.angle
                            self.angle = self.angle if self.angle > 315 else 315
                        elif self.p1_prev < self.p2_position: 
                            self.angle = self.angle + 20 
                        if self.angle >= 360: 
                            self.angle = self.angle - 360
                            self.angle = self.angle if self.angle < 45 else 45
                        # different approach fromn p2 since the angle changes sometimes from + to -

        # Draw background
        self.screen.fill(black)
        pygame.draw.rect(self.screen, grey, (5, 5, self.width-10, self.height-10), 5) # border
        pygame.draw.line(self.screen, grey, (self.width/2, 5), (self.width/2, self.height-5), 5) # middle line

        self.screen.blit(self.p1font, (self.width/2 - 67, 10))
        self.screen.blit(self.p2font, (self.width/2 + 50, 10))
        if self.showstart : self.screen.blit(self.start, (self.width/2 - 200, self.height - 50))
        elif self.showgameover : self.screen.blit(self.gameover, (self.width/2 - 100, self.height - 50))

        self.screen.blit(self.aitxt, (self.width/2 - 100, self.height/2))
        self.screen.blit(self.Human, (self.width/2 + 50, self.height/2))

        # Drawing players 1 and 2
        pygame.draw.rect(self.screen, white, (10, self.p1_position, 20, self.height/5.1), 0, 100)
        pygame.draw.rect(self.screen, white, (self.width - 30, self.p2_position, 20, self.height/5.1), 0, 100)

        # Drawing the ball
        pygame.draw.circle(self.screen, white, self.ball_position, self.radius) # radius = height/21

        pygame.display.flip()

        self.dt = self.clock.tick(60)/1000          

        return True, self.p1_position, self.ball_position[1]

# Agent against agent to train
class PongAI():

    # State: takes as argument -1 if bar is beneath the ball, 1 if above and 0 of both at same y-level
    # Action: Either move UP, DOWN, or NOTHING(global list movements in line 25)

    def __init__(self, alpha=0.5, epsilon=0.1):
        self.alpha = alpha
        self.epsilon = epsilon
        self.q = dict()

    def get_q_value(self, state, action):
        # return q value, or reward of a past event
        try:
            return self.q[state, action]
        except KeyError:
            return 0  


    def update(self, state, action, new_state, reward):

        #update q value of current state
        old = self.q[state, action] if (state, action) in self.q else 0
        best_future = self.bestfuture(new_state)
        self.q[state, action] = old + self.alpha * (reward + best_future - old)
        

    def bestfuture(self, new_state):

        # search for old states where an action performed the best
        best_reward = -float("inf")


        for i in movements:
            best_reward = max(self.get_q_value(new_state, i), best_reward)

        return best_reward
    

    def choose_action(self, state, randomness=True):
        
        # take best action, or choose a random action if there wasn't no reward
        # or allow the agent to explore for probable better solutions

        best_reward = -float("inf")
        action = None

        for i in movements:
            a=self.get_q_value(state, i)
            if(a>best_reward):
                best_reward=a
                action = i

        if best_reward==0:
            return random.choice(tuple(movements))
        
        if randomness and random.random() <= self.epsilon:
            return random.choice(tuple(movements))
        
        return action



def movingplayers(keys, p2_position, height, dt, rate):

        if keys[pygame.K_UP]:
            p2_position = p2_position - 200 * rate * dt if p2_position > 0 else 0
        if keys[pygame.K_DOWN]:
            p2_position = p2_position + 200 * rate * dt if p2_position < height - height/5.1 else height - height/5.1

        return p2_position

def ballbouncing(counter, angle, ball_position, radius, height, width, p1_position, p2_position) -> float:

        bounce = False

        # bounce on the upper and lower boundaries
        if ball_position[1] <= radius or ball_position[1] >= height-radius:
            angle = -angle

        # player bounce
        if counter>=30 and ball_position[0] <= 30 and p1_position < ball_position[1] < p1_position + height/5.1:
            alpha = abs(angle - 180) # angle between x axis and the direction
            angle = 360-alpha if angle > 180 else alpha
            # knowing that the positive sense is clockwise
            # and to keep the ball on the same y direction i needed to check whether the angle
            # was over or under the x axis to redirect my ball
            # having alpha in the case always in the second or third quadrant
            bounce = True
            counter = 0


        elif counter>=30 and ball_position[0] >= width - 30 and p2_position < ball_position[1] < p2_position + height/5.1:
            angle = 180 - angle if angle < 90 else 180 + 360 - angle
            bounce = True
            counter = 0

        return counter, bounce, angle

def move(action, position, height):
    
    if action == "UP":
        position = position - 2.5 * rrate
    elif action == "DOWN":
        position = position + 2.5 * rrate

    if position < 0:
        position = 0
    if position > height - height/5.1:
        position = height - height/5.1

    return position



# Train PongAI and play against this trained agent
def train(n):
    player = PongAI()

    for i in range(n):
        print(f"Training Agent round {i+1}")

        width, height = 840, 420
        bounce = False
        counter = 0

        ball_position=[width/2, height/2]
        r = random.randint(-45, 45)
        r = r+180 if random.randint(0,1) == 1 else r
        angle = r if r>=0 else 360-r

        radius = height/30

        p1_position =p2_position = height/2 -height/10.2
        p1_prev = p2_prev = 0

        while True:
            z = p1_position + height/10.2 - ball_position[1]
            state = ( 1 if z > 0 else -1 if z<0 else 0 )

            counter += 1

            p1_prev, p2_prev = p1_position, p2_position
            action = player.choose_action(state)

            p1_position = p2_position = move(action, p1_position, height)


            z = p1_position + height/10.2 - ball_position[1]
            new_state = ( 1 if z > 0 else -1 if z<0 else 0 )

            counter, bounce, angle = ballbouncing(counter, angle, ball_position, radius, height, width, p1_position, p2_position)

            #ball position
            ball_position[0] += 2 * math.cos(angle * math.pi / 180)
            ball_position[1] += 2 * math.sin(angle * math.pi / 180)


            # if bounce change the direction of the ball with respect to the movement of the bar
            if bounce:
                if ball_position[0]>width/2: 
                    if p2_prev > p2_position: angle = angle + 20 if angle + 20 < 225 else 225 # upwards
                    elif p2_prev < p2_position: angle = angle - 20 if angle -20 > 135 else 135 # downwards

                else: 
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

                player.update(state, action, new_state, 1)


            #gameover
            if ball_position[0] <= radius or ball_position[0] >= width - radius:
                player.update(state, action, new_state, -1)
                break

            if not bounce:
                player.update(state, action, new_state, 0)



    print("Done Training\n")
    return player

def play(ai):

    game = Pong()
    running = True

    #initially
    p1_position = game.p1_position 
    height = game.height/10.2 
    ball_position = game.ball_position[1]


    while running:

        z = p1_position + height - ball_position
        state = ( 1 if z > 0 else -1 if z<0 else 0 )# check if the agent is under, above, or on the same level as the ball

        ai_action = ai.choose_action(state, False)
        running, p1_position, ball_position = game.gameplay(ai_action)


    print("Closing game...")
    pygame.quit()