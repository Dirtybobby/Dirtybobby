import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, K_p, K_w, K_a, K_s, K_d

pygame.init()

# Конфігураційні змінні
WIDTH = 1200
HEIGHT = 800
FPS = 60
BG_MOVE = 3
PLAYER_SPEED = 4
ENEMY_INTERVAL = 1500
BONUS_INTERVAL = 1500

# Кольори
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (255, 0, 0)

# Ініціалізація звукових ефектів
pygame.mixer.init()

# Звукові ефекти
background_music = pygame.mixer.Sound("background_music.mp3")
game_over_music = pygame.mixer.Sound("game_over.mp3")
bonus_sound = pygame.mixer.Sound("bonus_sound.mp3")
collision_sound = pygame.mixer.Sound("collision_sound.mp3")  # Додано новий звук для зіткнення
pause_unpause_sound = pygame.mixer.Sound("pause_unpause_sound.mp3")  # Додано звук для паузи та зняття з паузи

# Канали для звукових ефектів
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

# Клас гравця
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.keys = None

    def update(self):
        if self.keys:
            if (self.keys[K_s] or self.keys[K_DOWN]) and self.rect.bottom <= HEIGHT:
                self.rect = self.rect.move(0, PLAYER_SPEED)
            if (self.keys[K_d] or self.keys[K_RIGHT]) and self.rect.right <= WIDTH:
                self.rect = self.rect.move(PLAYER_SPEED, 0)
            if (self.keys[K_w] or self.keys[K_UP]) and self.rect.top >= 0:
                self.rect = self.rect.move(0, -PLAYER_SPEED)
            if (self.keys[K_a] or self.keys[K_LEFT]) and self.rect.left >= 0:
                self.rect = self.rect.move(-PLAYER_SPEED, 0)

# Клас ворога
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect(center=(WIDTH + 20, random.randint(0, HEIGHT)))
        self.move = [random.randint(-8, -4), 0]

    def update(self):
        self.rect = self.rect.move(self.move)

# Клас бонусу
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bonus.png").convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), 0))

    def update(self):
        self.rect = self.rect.move(0, random.randint(4, 8))

# Ініціалізація
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
FONT_SIZE = 30
FONT_BIG = pygame.font.SysFont('Verdana', FONT_SIZE * 3)
FONT_SMALL = pygame.font.SysFont('Verdana', FONT_SIZE)

# Групи спрайтів
all_sprites = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
bonuses_group = pygame.sprite.Group()

# Гравець
player = Player()
all_sprites.add(player)

# Таймери
pygame.time.set_timer(pygame.USEREVENT + 1, ENEMY_INTERVAL)
pygame.time.set_timer(pygame.USEREVENT + 2, BONUS_INTERVAL)
pygame.time.set_timer(pygame.USEREVENT + 3, 200)

# Зміна зображення гравця
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
image_index = 0

# Рахунок
score = 0

# Рекорд
high_score = 0

# Шлях до файлу для збереження рекорду
high_score_file_path = os.path.join(os.path.dirname(__file__), "high_score.txt")

# Завантаження попереднього рекорду з файлу, якщо він існує
if os.path.exists(high_score_file_path):
    with open(high_score_file_path, "r") as file:
        try:
            high_score = int(file.read())
        except ValueError:
            pass

# Головний цикл гри
playing = True
game_over = False
paused = False
clock = pygame.time.Clock()

# Стан фонової музики (0 - зупинено, 1 - грає)
background_music_state = 0

# Відтворення фонової музики на початку гри
channel1.play(pygame.mixer.Sound("background_music.mp3"), loops=-1)

while playing:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                playing = False
            elif event.key == K_SPACE and game_over:
                # Почати гру знову після GAME OVER
                all_sprites.empty()
                enemies_group.empty()
                bonuses_group.empty()
                player = Player()
                all_sprites.add(player)
                score = 0
                game_over = False
                paused = False
                # Відтворення фонової музики на початку гри
                channel1.play(pygame.mixer.Sound("background_music.mp3"), loops=-1)
                channel2.stop()  # Зупинити музику гейм овер
            elif event.key == K_p:
                # Зробити паузу, тільки якщо гра не завершена
                if not game_over:
                    paused = not paused
                    if paused:
                        # Зупинити фонову музику при паузі
                        channel1.pause()
                        background_music_state = 0
                        pause_unpause_sound.play()  # Відтворення звуку паузи
                    else:
                        # Відновити фонову музику при виході з паузи
                        channel1.unpause()
                        background_music_state = 1
                        pause_unpause_sound.play()  # Відтворення звуку зняття з паузи

        elif event.type == pygame.USEREVENT + 1:
            if not game_over and not paused:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies_group.add(enemy)
        elif event.type == pygame.USEREVENT + 2:
            if not game_over and not paused:
                bonus = Bonus()
                all_sprites.add(bonus)
                bonuses_group.add(bonus)
        elif event.type == pygame.USEREVENT + 3:
            if not game_over:
                player.image = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index = (image_index + 1) % len(PLAYER_IMAGES)

    if not game_over and not paused:
        bg_X1 -= BG_MOVE
        bg_X2 -= BG_MOVE

        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()

        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))

        keys = pygame.key.get_pressed()
        player.keys = keys
        player.update()

        all_sprites.update()

        if pygame.sprite.spritecollide(player, enemies_group, False):
            # Гравець стикнувся з ворогом, GAME OVER
            game_over = True
            channel1.stop()  # При GAME OVER зупиняємо фонову музику
            channel2.play(pygame.mixer.Sound("game_over.mp3"))  # Грає музика гейм овер
            collision_sound.play()  # Відтворення звуку зіткнення

        bonuses_collected = pygame.sprite.spritecollide(player, bonuses_group, True)
        if bonuses_collected:
            score += len(bonuses_collected)
            bonus_sound.play()  # Відтворення звуку отримання бонусів

        # Оновлення рекорду
        if score > high_score:
            high_score = score

        score_text = FONT_SMALL.render("SCORE: {}".format(score), True, COLOR_BLACK)
        main_display.blit(score_text, (20, 20))
        all_sprites.draw(main_display)

    if game_over:
        game_over_text = FONT_BIG.render("GAME OVER", True, COLOR_RED)
        main_display.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))

        try_again_text = FONT_SMALL.render("Try Again (Space)", True, COLOR_BLACK)
        main_display.blit(try_again_text, (WIDTH // 2 - try_again_text.get_width() // 2, HEIGHT // 2 + 50))

        escape_text = FONT_SMALL.render("Press ESC to exit", True, COLOR_BLACK)
        main_display.blit(escape_text, (WIDTH // 2 - escape_text.get_width() // 2, HEIGHT // 2 + 100))

    if paused:
        pause_text = FONT_BIG.render("PAUSED", True, COLOR_BLUE)
        main_display.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))

    # Виведення рекорду на екран
    high_score_text = FONT_SMALL.render("HIGH SCORE: {}".format(high_score), True, COLOR_RED)
    main_display.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 20))

    pygame.display.flip()

# Збереження рекорду в файлі
with open(high_score_file_path, "w") as file:
    file.write(str(high_score))

pygame.quit()
