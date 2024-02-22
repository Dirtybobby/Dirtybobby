#Імпорт потрібних бібліотек та модулів
import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

# Кольори
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0 ,0, 255)
COLOR_YELLOW = (255, 255, 0)

# Розмір екрану
HEIGHT = 800
WIDTH = 1200 

FONT = pygame.font.SysFont('Verdana', 20)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

# Властивості гравця
player_size = (20, 20)
player = pygame.image.load("player.png").convert_alpha()
player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Рух гравця
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

# Властивості ворога
def create_enemy():
    # Завантаження зображення та визначення його розміру
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy_size = enemy.get_size()
    
    # Створення ворога та його початкові координати
    enemy_rect = pygame.Rect(WIDTH + 20, random.randint(0, HEIGHT), *enemy_size)
    
    # Визначення випадкового руху ворога
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

# Властивості бонусів
def create_bonus():
    # Завантаження зображення та визначення його розміру
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_size = bonus.get_size()
    
    # Створення бонусу та його початкові координати
    bonus_rect = pygame.Rect(random.randint(20, WIDTH - 20), 0, *bonus_size)
    
    # Визначення випадкового руху бонусу
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500) 
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500) 
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

bonuses = []
enemies = []

score = 0

image_index = 0

playing = True

while playing:
    FPS.tick(360)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            # Зміна зображення гравця за подією
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
        image_index += 1
        if image_index >= len(PLAYER_IMAGES):
            image_index = 0

    # Зміщення фону гри
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    # Відображення фону гри
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    # Рух гравця за допомогою клавіш
    if keys[K_DOWN] and player_rect.bottom <= HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right <= WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)

    # Відображення ворогів та взаємодія гравця з ними
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    # Відображення бонусів та взаємодія гравця з ними
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    # Відображення рахунку гравця
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))

    # Відображення гравця
    main_display.blit(player, player_rect)

    # Оновлення екрану
    pygame.display.flip()

    # Видалення ворогів, які виходять за межі екрану
    enemies = [enemy for enemy in enemies if enemy[1].left > 0]

    # Видалення бонусів, які виходять за межі екрану
    bonuses = [bonus for bonus in bonuses if bonus[1].top < HEIGHT]
