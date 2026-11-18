import pygame
from random import randint
pygame.init()

screen_title = 'Ping Pong'
screen_width = 700
screen_height = 500
screen_color = (255, 255, 255)

class Hitbox():
    def __init__(self, screen, x, y, width, height, color, thickness):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
        if thickness < 1:
            thickness = 1
        self.thickness = thickness

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw_hitbox(self):
        pygame.draw.rect(self.screen, self.color, self.rect, self.thickness)

class Picture(Hitbox):
    def __init__(self, screen, x, y, width, height, color, thickness, image_path):
        Hitbox.__init__(self, screen, x, y, width, height, color, thickness)
        self.image_path = image_path

        self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (self.width, self.height))

    def draw_picture(self):
        # отрисоваем изображение и текст (blit)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(Picture):
    def __init__(self, screen, x, y, width, height, color, thickness, image_path, speed):
        Picture.__init__(self, screen, x, y, width, height, color, thickness, image_path)
        self.speed = speed

        self.dx = 0
        
    def move(self):
        self.rect.x += self.speed * self.dx

    def controller_words(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.dx = -1
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.dx = 1
        else:
            self.dx = 0
    
    def controller_hands(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.dx = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.dx = 1
        else:
            self.dx = 0
    
    def collide_screen(self, screen_width, screen_height):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        

class Ball(Picture): 
    def __init__(self, screen, x, y, width, height, color, thickness, image_path, speed):
        Picture.__init__(self, screen, x, y, width, height, color, thickness, image_path)
        self.speed = speed

        self.dx = -1
        self.dy = 1

    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

    def collide_screen(self, screen_width):
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = -self.dx
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.dx = -self.dx

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)

tickrate = 60
clock = pygame.time.Clock()

player1 = Player(screen, -0, -450, 150, 20, (0, 0, 0), 2, 'plate.png', 7)
player2 = Player(screen, -0, 480, 150, 20, (0, 0, 0), 2, 'plate.png', 7)

ball = Ball(screen, 350, 250, 20, 20, (0, 0, 0), 2, 'cricket-ball.png', 5)


point = 0
missed = 0

missed_text = pygame.font.SysFont(None, 30).render('Пропушено: ' + str(missed), True, (0, 0, 0))
point_text = pygame.font.SysFont(None, 30).render('Счет: ' + str(point), True, (0, 0, 0))


game_is_working = True
while game_is_working:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_is_working = False

    screen.fill(screen_color)

    screen.blit(missed_text, (0, 20))
    screen.blit(point_text, (0, 40))

    ball.move()
    ball.collide_screen(screen_width)
    ball.draw_picture()

    if ball.rect.bottom < 0:
        ball.rect.x = 350
        ball.rect.y = 250
        missed += 1
        missed_text = pygame.font.SysFont(None, 30).render('Пропушено: ' + str(missed), True, (0, 0, 0))
    
    if ball.rect.top > screen_height:
        ball.rect.x = 350
        ball.rect.y = 250
        missed += 1
        missed_text = pygame.font.SysFont(None, 30).render('Пропушено: ' + str(missed), True, (0, 0, 0))
    
    if ball.rect.colliderect(player1):
        ball.rect.top = player1.rect.bottom
        ball.dy = 1
        point += 1
        point_text = pygame.font.SysFont(None, 30).render('Счет: ' + str(point), True, (0, 0, 0))

    if ball.rect.colliderect(player2):
        ball.rect.bottom = player2.rect.top
        ball.dy = -1
        point += 1
        point_text = pygame.font.SysFont(None, 30).render('Счет: ' + str(point), True, (0, 0, 0))

    player1.move()
    player1.controller_words()
    player1.collide_screen(screen_width, screen_height)
    player1.draw_picture()

    player2.move()
    player2.controller_hands()
    player2.collide_screen(screen_width, screen_height)
    player2.draw_picture()


    pygame.display.flip()
    clock.tick(tickrate)