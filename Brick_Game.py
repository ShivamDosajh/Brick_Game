import sys
import time
import numpy as np
import pygame

# Variables
width = 1000
height = 660
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
blue = pygame.Color('blue')
green = pygame.Color('green')
brown = (100, 40, 0)
wall_thickness = 30
paddle_thickness = 20
paddle_length = 150
caption = 'Brick Game'
score = 0

layer_length = 7
layer_n = 5

brick_width = 20
brick_length = 80

init_speed = 4

x = np.random.randint(0, 2)

a = np.linspace(wall_thickness, height - wall_thickness, layer_length + 1, dtype=int)

pygame.init()
gameSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption(caption)
collision_sound = pygame.mixer.Sound('collision.wav')
pong_sound = pygame.mixer.Sound('pong.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')
victory_sound = pygame.mixer.Sound('victory.wav')


def score_print(score):
    gameSurface.fill(white, (0, 0, width, wall_thickness))
    msg_to_screen(f'Score: {score}', red, 25, -315, False)

def msg_to_screen(msg, color, size, y_displace=0, update = True):
    font = pygame.font.SysFont('comicsansms', size)
    text = font.render(msg, True, color)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2 + y_displace)
    gameSurface.blit(text, textRect)
    if update:
        pygame.display.update()

def Victory():
    msg_to_screen('YOU WON!', green, 70)
    pygame.mixer.Sound.play(victory_sound)
    msg_to_screen('Press R to Restart or Q to Quit', white, 30, 50)
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r:
                GameLoop()
        pygame.display.update()


def game_over_screen():
    msg_to_screen('GAME OVER', red, 75)
    pygame.mixer.Sound.play(game_over_sound)
    time.sleep(1.5)
    msg_to_screen('Press R to Restart or Q to Quit', white, 30, 50)
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                GameLoop()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()


def StartScreen():
    msg_to_screen('BRICK GAME', brown, 70, -50)
    msg_to_screen('Press P to Play or Q to Quit', white, 30, 50)
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                GameLoop()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()


def GameLoop():
    global score
    score = 0

    class Ball:
        radius = 20

        def __init__(self, x, y, vx, vy):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy

        def show(self, color):
            global gameSurface
            pygame.draw.circle(gameSurface, color, (self.x, self.y), self.radius)

        def update(self):

            if self.x + self.vx < wall_thickness + self.radius:
                self.vx *= -1
                pygame.mixer.Sound.play(pong_sound)
            elif self.y + self.vy > (
                    height - wall_thickness - self.radius) or self.y + self.vy < wall_thickness + self.radius:
                self.vy *= -1
                pygame.mixer.Sound.play(pong_sound)
            elif self.x + self.vx + self.radius >= width - paddle_thickness and paddleObject.y <= self.y <= paddleObject.y + paddle_length:
                pygame.mixer.Sound.play(pong_sound)
                self.vx *= -1
            else:
                self.x += self.vx
                self.y += self.vy
                self.show(green)

    class Paddle:
        def __init__(self, y):
            self.y = y

        def print_paddle(self):
            global gameSurface
            pygame.draw.rect(gameSurface, red, (width - paddle_thickness, self.y, paddle_thickness, paddle_length))

        def update(self):
            cur = pygame.mouse.get_pos()
            if cur[1] > wall_thickness and (cur[1] + paddle_length) < (height - wall_thickness):
                self.y = cur[1]
            self.print_paddle()

    class Bricks:
        hit = False
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def show(self, color):
            global gameSurface
            pygame.draw.rect(gameSurface, color, (self.x, self.y, brick_width, brick_length))

        def update(self):
            global score
            if not self.hit:
                self.show(brown)
                if (self.x <= ballObject.x - ballObject.radius <= self.x + brick_width and ballObject.y > self.y and ballObject.y < self.y + brick_length) or (
                    self.x <= ballObject.x + ballObject.radius <= self.x + brick_width and ballObject.y > self.y and ballObject.y < self.y + brick_length):
                    self.hit = True
                    score += 1
                    pygame.mixer.Sound.play(collision_sound)
                    ballObject.vx *= -1
                    for layer in brickObjects:
                        if self in layer:
                            layer.remove(self)

    paddleObject = Paddle(height // 2)
    paddleObject.print_paddle()

    if x == 0:
        y_chooser = 1
    else:
        y_chooser = -1

    ballObject = Ball(width - 3 * Ball.radius, height // 4, -init_speed, init_speed * y_chooser)
    ballObject.show(green)

    brickObjects = []
    for i in range(layer_n):
        layer = []
        for j in range(layer_length):
            layer.append(Bricks(wall_thickness * (i + 1), a[j]))
        brickObjects.append(layer)
    GameOver = False

    # Draw Walls
    pygame.draw.rect(gameSurface, white, (0, 0, width, wall_thickness))
    pygame.draw.rect(gameSurface, white, (0, 0, wall_thickness, height))
    pygame.draw.rect(gameSurface, white, (0, height - wall_thickness, width, wall_thickness))

    clock = pygame.time.Clock()

    while not GameOver:
        gameSurface.fill(black, (wall_thickness, wall_thickness, width, height - 2 * wall_thickness))
        score_print(score)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if ballObject.x + ballObject.radius > width - paddle_thickness:
            game_over_screen()

        if score == layer_n * (layer_length):
            Victory()

        # For Testing
        '''if score == 2:
            Victory()'''

        for layer in brickObjects:
            for obj in layer:
                obj.update()

        ballObject.update()
        paddleObject.update()

        pygame.display.update()
        clock.tick(120)

StartScreen()
