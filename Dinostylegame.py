from pygame import *
import pygame as pygame
import os
import random
import mysql.connector

pygame.init()

# Global Constants
Screen_Height = 600
Screen_Width = 1100

Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

Running = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

Jumping = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

Obstacle = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
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
        # self.jump_vel = self.Jump_vel
        self.jump_vel = 0

        self.gravity = 0.05

        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos

    def update(self, userInput, prev):
        self.animate()

        if ((userInput[pygame.K_UP] and not prev[pygame.K_UP]) or (userInput[pygame.K_SPACE] and not prev[pygame.K_SPACE] and not self.dino_jump)):
            self.jump_vel = -4
            self.dino_jump = False

    def animate(self):
        self.jump_vel += self.gravity
        if(self.jump_vel >= 50):
            self.jump_vel = 50
        self.dino_rect.y += self.jump_vel

        if self.dino_rect.y >= self.Y_pos:
            self.image = self.run_img[self.step // 5]
            self.dino_rect.y = self.Y_pos
            self.step += 1

        if self.dino_rect.y < self.Y_pos:
            self.image = self.jump_img

        if self.step >= 10:
            self.step = 0

        x = self.dino_rect
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = x.x
        self.dino_rect.y = x.y

    def draw(self, Screen):
        Screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = Screen_Width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = Clouds
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = Screen_Width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def Draw(self, Screen):
        Screen.blit(self.image, (self.x, self.y))


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, highscore, run
    run = True
    player = Dinosaur()
    game_speed = 1
    cloud = Cloud()
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    highscore = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    previous_key = 0

    def Score():
        global points, game_speed, highscore, run
        points += 1

        if points % 10000 == 0:
            game_speed += 1

            if run is False:
                if points > highscore:
                    highscore = points

        text = font.render("Score: " + str(points), True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.center = (1000, 40)
        Screen.blit(text, textrect)

        text1 = font.render("HI: " + str(highscore), True, (0, 0, 0))
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

        background()

        player.draw(Screen)
        player.update(user_input, previous_key)
        previous_key = user_input

        Score()

        cloud.Draw(Screen)
        cloud.update()

        pygame.display.update()


main()
