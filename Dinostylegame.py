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

pygame.display.set_caption("Dino Run")


run = True
highscore = 0
game_speed = 1
score = 0
x_pos_bg = 0
y_pos_bg = 0
points = 0
obstacles = []
name = ''
l = 0


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
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, highscore, run, score, name
    run = True
    player = Dinosaur()
    clock = pygame.time.Clock()
    game_speed = 20
    cloud = Cloud()
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []

    def Score():
        global points, game_speed, highscore, run, l
        points += 1

        if points % 100 == 0:
            game_speed += 1

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
        if points % 50 == 0:
            obstacles.append(Obstacle())

        for obstacle in obstacles:
            obstacle.draw(Screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                player.image = Dead
                run = False
                file = open('score.csv', 'a', newline='')
                filewriter = csv.writer(file)
                scoredata = [str(name), points]
                filewriter.writerow(scoredata)
                file.close()
                if points > highscore:
                    highscore = points
                menu()

        background()

        player.draw(Screen)
        player.update(user_input)

        Score()

        cloud.Draw(Screen)
        cloud.update()

        clock.tick(30)
        pygame.display.update()


def highscore_page():
    run = True
    file = open('score.csv', 'r')
    filereader = csv.reader(file)
    font = pygame.font.Font('freesansbold.ttf', 70)

    names = []
    for x in filereader:
        names.append(x)
    names.sort(key=lambda x: int(x[1]), reverse=True)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

        ypos = 190
        count = 0
        first = 1

        Screen.fill((0, 0, 0))
        text = font.render("Leaderboard", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 100)

        Screen.blit(text, textrect)
        if (pygame.key.get_pressed()[pygame.K_ESCAPE]):
            menu()

        for name, score in names:
            if count < 6:
                if first == 1:
                    pygame.draw.line(Screen, (255, 255, 255),
                                     (350, ypos+20), (740, ypos+20), 2)
                    first = 0
                    text1 = font.render("Player Name", True, (255, 255, 255))
                    text2 = font.render("Score", True, (255, 255, 255))
                    textrect1 = text1.get_rect()
                    textrect2 = text2.get_rect()
                    textrect1.center = (450, ypos)
                    textrect2.center = (675, ypos)
                    Screen.blit(text1, textrect1)
                    Screen.blit(text2, textrect2)
                    ypos += 50
                    count += 1
                text1 = font.render(name, True, (255, 255, 255))
                text2 = font.render(score, True, (255, 255, 255))
                textrect1 = text1.get_rect()
                textrect2 = text2.get_rect()
                textrect1.center = (450, ypos)
                textrect2.center = (675, ypos)
                Screen.blit(text1, textrect1)
                Screen.blit(text2, textrect2)
                ypos += 50
                count += 1
            else:
                pass

        file.close()
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press Esc to go Back", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 500)

        Screen.blit(text, textrect)
        pygame.draw.rect(Screen, (255, 255, 255), (360, 475, 375, 50), 3, 30)
        pygame.display.update()


def nameinputpage():
    global name
    name = ''
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if event.unicode.isalpha():
                        name += event.unicode
                if event.key == pygame.K_RETURN:
                    main()
                    run = False
        Screen.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render("Please Enter Your Name", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 100)

        Screen.blit(text, textrect)
        if (pygame.key.get_pressed()[pygame.K_ESCAPE]):
            menu()
            run = False

        input_rect = pygame.Rect(360, 250, 375, 50)

        color_active = pygame.Color('grey')
        color_passive = pygame.Color('white')
        color = color_passive

        pygame.draw.rect(Screen, color, input_rect)

        nameInput = font.render(name, True, (0, 0, 0))
        nameInputRect = nameInput.get_rect()
        nameInputRect.center = (547.5, 275)
        Screen.blit(nameInput, nameInputRect)

        pygame.display.update()


def menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
        user_input = pygame.key.get_pressed()

        if (user_input[pygame.K_p]):
            nameinputpage()
            run = False

        if (user_input[pygame.K_l]):
            highscore_page()
            run = False

        if user_input[pygame.K_q]:
            run = False
            exit()

        Screen.fill((0, 0, 0))

        font = pygame.font.Font('freesansbold.ttf', 70)
        text = font.render("Dino Run", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 100)

        Screen.blit(text, textrect)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press P to Play", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 200)

        Screen.blit(text, textrect)
        pygame.draw.rect(Screen, (255, 255, 255), (400, 175, 300, 50), 3, 30)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press L for Leaderboard", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 300)

        Screen.blit(text, textrect)
        pygame.draw.rect(Screen, (255, 255, 255), (325, 275, 450, 50), 3, 30)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press Q to Quit", True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.center = (550, 400)

        Screen.blit(text, textrect)
        pygame.draw.rect(Screen, (255, 255, 255), (400, 375, 300, 50), 3, 30)

        pygame.display.update()


menu()
