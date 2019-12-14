import pygame, os, pandas as pd, random, time
from pygame.locals import *


def load_png(filename, fit_w, fit_h):
    png = pygame.image.load(filename)
    w, h = png.get_rect().width, png.get_rect().height

    scale_w = float(fit_w) / w
    scale_h = float(fit_h) / h
    scale = min([scale_h, scale_w])
    req_w = int(w * scale)
    req_h = int(h * scale)

    return pygame.transform.scale(png, (req_w, req_h))


pygame.init()
windowSurface = pygame.display.set_mode((600,900), 0, 32)
pygame.display.set_caption('Guess the Flag!')

WHITE = (255, 255, 255)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
basicFont = pygame.font.SysFont(None, 48)

correct_answer_position = 0
answer_names = ["","",""]

def draw_flag():
    global correct_answer_position

    windowSurface.fill(WHITE)
    countries = pd.read_csv(os.path.join('data', 'countries.csv'))
    print(len(countries))
    country_count = len(countries)
    country_index = random.randint(1, country_count) - 1

    fake_country_one_index = country_index
    while fake_country_one_index == country_index:
        fake_country_one_index = random.randint(1, country_count) - 1

    fake_country_two_index = country_index
    while fake_country_two_index == country_index or fake_country_two_index == fake_country_one_index:
        fake_country_two_index = random.randint(1, country_count) - 1

    print(countries['code'][country_index])
    country_code = countries['code'][country_index]
    country_file = country_code + ".png"
    picture = load_png(os.path.join('images', 'flags', 'png', country_file), 600, 400)
    windowSurface.blit(picture, (0, 0))

    country_name = countries['name'][country_index]
    country_name_1 = countries['name'][fake_country_one_index]
    country_name_2 = countries['name'][fake_country_two_index]

    correct_answer_position = random.randint(1, 3)
    if correct_answer_position == 1:
        other_position_1 = 2
        other_position_2 = 3
    elif correct_answer_position == 2:
        other_position_1 = 1
        other_position_2 = 3
    elif correct_answer_position == 3:
        other_position_1 = 1
        other_position_2 = 2

    draw_country_name(country_name, correct_answer_position )
    draw_country_name(country_name_1, other_position_1)
    draw_country_name(country_name_2, other_position_2)
    pygame.display.update()


def draw_country_name(country_name, answer_position, colour = BLUE):
    text = basicFont.render(country_name, True, colour, WHITE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = 400 + 100 * answer_position
    windowSurface.blit(text, textRect)
    answer_names[answer_position - 1] = country_name

def guess(my_guess):
    draw_country_name(answer_names[my_guess - 1], my_guess, GREEN)
    global correct_answer_position
    if my_guess == correct_answer_position:
        text = basicFont.render('YAY!', True, GREEN, WHITE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = 800
        windowSurface.blit(text, textRect)
    else:
        text = basicFont.render('BOO!', True, RED, WHITE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = 800
        windowSurface.blit(text, textRect)
    pygame.display.update()
    time.sleep(3)
    draw_flag()

draw_flag()


active = True

while active:
    pygame.event.pump()
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.display.quit()
        active = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            draw_flag()
        if event.key == pygame.K_1:
            guess(1)
        if event.key == pygame.K_2:
            guess(2)
        if event.key == pygame.K_3:
            guess(3)
