from pygame import *
import pygame as pygame
import os
import random
import csv

pygame.init()

# Global Constants
Screen_Height = 600
Screen_Width = 1100

Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

Running = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

''' Running = [pygame.image.load(os.path.join("Assets", "art.png")),
           pygame.image.load(os.path.join("Assets", "art (1).png"))] '''

Jumping = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

Dead = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))

Obstacles = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
             pygame.image.load(os.path.join(
                 "Assets/Cactus", "LargeCactus2.png")),
             pygame.image.load(os.path.join(
                 "Assets/Cactus", "LargeCactus3.png")),
             pygame.image.load(os.path.join(
                 "Assets/Cactus", "SmallCactus1.png")),
             pygame.image.load(os.path.join(
                 "Assets/Cactus", "SmallCactus2.png")),
             pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

Track = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

Clouds = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

pygame.display.set_caption("Dino Game")


class Dinosaur:
    X_pos = 80
    Y_pos = 310
    Jump_vel = 8.5

    def __init__(self):
        self.run_img = Running
        self.jump_img = Jumping

        self.dino_run = True
        self.dino_jump = False

        self.step = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.jump_vel = self.Jump_vel

        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos

    def update(self, userInput):
        # self.animate()
        if(self.dino_jump):
            self.jump()

        if(self.dino_run):
            self.run()

        if self.step >= 10:
            self.step = 0

        if((userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump):
            self.dino_jump = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel*4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.Jump_vel:
            self.dino_jump = False
            self.jump_vel = self.Jump_vel

    def run(self):
        self.image = self.run_img[self.step // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos
        self.step += 1

    def draw(self, Screen):
        Screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Obstacle:
    def __init__(self):
        self.image = Obstacles[random.randint(0, 5)]
        self.rect = self.image.get_rect(
            topleft=(Screen_Width, 400-self.image.get_size()[1]))

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, Screen):
        Screen.blit(self.image, self.rect)


class Cloud:
    def __init__(self):
        self.x = Screen_Width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = Clouds
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = Screen_Width
            self.y = random.randint(50, 100)

    def Draw(self, Screen):
        Screen.blit(self.image, (self.x, self.y))


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, highscore, run, l
    run = True
    player = Dinosaur()
    clock = pygame.time.Clock()
    game_speed = 20
    cloud = Cloud()
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    highscore = [0]
    l = len(highscore)
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []

    def Score():
        global points, game_speed, highscore, run, l
        points += 1

        if points % 100 == 0:
            game_speed += 1

            if run is False:
                l = len(highscore)
                if points > highscore[l-1]:
                    highscore.append(points)

        text = font.render("Score: " + str(points), True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.center = (1000, 40)
        Screen.blit(text, textrect)


        text1 = font.render("HI: " + str(highscore[l-1]), True, (0, 0, 0))
        text1rect = text1.get_rect()
        text1rect.center = (875, 40)
        Screen.blit(text1, text1rect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = Track.get_width()

        Screen.blit(Track, (x_pos_bg, y_pos_bg))
        Screen.blit(Track, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg < - image_width:
            Screen.blit(Track, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0

        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        Screen.fill((255, 255, 255))

        user_input = pygame.key.get_pressed()
        if points % 50 == 0:
            obstacles.append(Obstacle())

        for obstacle in obstacles:
            obstacle.draw(Screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                player.image = Dead
                menu()

        background()

        player.draw(Screen)
        player.update(user_input)

        Score()

        cloud.Draw(Screen)
        cloud.update()

        clock.tick(30)
        pygame.display.update()


""" main() """


def score():
    run = True
    while run:
        global highscore
        highscore = [0]

        Screen.fill((0, 0, 0))

        font = pygame.font.Font('freesansbold.ttf', 70)
        text = font.render("Leaderboard", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 100)

        Screen.blit(text, textrect)

        file = open('score.txt', 'w+')

        file.writelines(highscore)

        for x in range(1, 5):
            read = file.readline()
            score = read
            font = pygame.font.Font('freesansbold.ttf', 70)
            text = font.render(score, True, (255, 255, 255))
            textrect = text.get_rect()
            textrect.center = (550, 100)
            Screen.blit(text, textrect)
            pygame.draw.rect(Screen, (255, 255, 255),
                             (400, 375, 300, 50), 3, 30)

        file.close()


def menu():
    run = True
    while run:

        Screen.fill((0, 0, 0))

        font = pygame.font.Font('freesansbold.ttf', 70)
        text = font.render("Dino Game", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 100)

        Screen.blit(text, textrect)

        user_input = pygame.key.get_pressed()

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press P to Play", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 200)

        Screen.blit(text, textrect)
        pygame.draw.rect(Screen, (255, 255, 255), (400, 175, 300, 50), 3, 30)

        if (user_input[pygame.K_p]):
            main()

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press L for Leaderboard", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 300)

        Screen.blit(text, textrect)
        pygame.draw.rect(Screen, (255, 255, 255), (350, 275, 400, 50), 3, 30)

        if user_input[pygame.K_l]:
            score()

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press Q to Quit", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 400)

        Screen.blit(text, textrect)
        pygame.draw.rect(Screen, (255, 255, 255), (400, 375, 300, 50), 3, 30)

        if user_input[pygame.K_q]:
            run = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


menu()
