import os
import pygame
import sys
import random

pygame.init()
size = WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
SHAG = 50
zmi = None
all_sprites = pygame.sprite.Group()
tt_group = pygame.sprite.Group()
zm_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'empty': load_image('grass.jpg')
}
player_image = load_image('golova.png', -1)
tail = load_image('zmeya.png', -1)
tail_tail = load_image('tail.png', -1)
povor = load_image('povorotzmeu.png', -1)
apple = load_image('apple.png', -1)

tile_width = tile_height = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tt_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Apple(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tt_group, all_sprites)
        self.image = apple
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 2)


class Tail_tail(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tt_group, all_sprites)
        self.image = tail_tail
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tail(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tt_group, all_sprites)
        self.image = tail
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Zmeya(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(zm_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 2)


def generate_level(level):
    new_zm, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)  # TODO потом добавить стенки
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_zm = Zmeya(x, y)
    x1 = random.randint(1, 23)
    y1 = random.randint(1, 11)
    applee = Apple(x1, y1)
    tail = Tail(0, 0)
    Taill = Tail_tail(0, 0)
    return new_zm, x, y, applee, x1, y1, tail, Taill


def start_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
picture = pygame.image.load('Data/map.png')
rect = picture.get_rect()
rect = rect.move((0, 0))
zmi, level_x, level_y, applee, xap, yap, tail, Tail_tail = generate_level(load_level('pole.txt'))
running = True
napr = '-x'
coor = [5, 5]
timer = 75
posl = '+x'
rotate = 0
Tail_tail.rect.x = SHAG * (coor[0] + 1)
Tail_tail.rect.y = SHAG * (coor[1] - 1)
tail.rect.x = SHAG * (coor[0]) - 20
tail.rect.y = SHAG * (coor[1] - 1)
applee.rect.y, applee.rect.x = SHAG * yap, SHAG * xap
apcoor = [xap + 1, yap + 1]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and posl != '+y':
                zmi.image = pygame.transform.rotate(player_image, 270)
                napr = '-y'
            if event.key == pygame.K_LEFT and posl != '+x':
                zmi.image = pygame.transform.rotate(player_image, 0)
                napr = '-x'
            if event.key == pygame.K_DOWN and posl != '-y':
                zmi.image = pygame.transform.rotate(player_image, 90)
                napr = '+y'
            if event.key == pygame.K_RIGHT and posl != '-x':
                zmi.image = pygame.transform.rotate(player_image, 180)
                napr = '+x'
    if apcoor[0] == coor[0] and apcoor[1] == coor[1]:
        xx = random.randint(1, 23)
        yy = random.randint(1, 11)
        applee.rect.y, applee.rect.x = SHAG * yy, SHAG * xx
        apcoor = [xx + 1, yy + 1]
    print(coor, apcoor, applee.rect.x)
    timer -= 1
    if timer == 0:
        timer = 75
        if napr == '-y':
            coor[1] -= 1
            if coor[1] == 0:
                zmi.rect.y += SHAG * 12
                coor[1] = 12
            zmi.rect.y -= SHAG
        elif napr == '-x':
            coor[0] -= 1
            if coor[0] == 0:
                zmi.rect.x += SHAG * 24
                coor[0] = 24
            zmi.rect.x -= SHAG
        elif napr == '+y':
            coor[1] += 1
            if coor[1] == 13:
                zmi.rect.y -= SHAG * 12
                coor[1] = 1
            zmi.rect.y += SHAG
        elif napr == '+x':
            coor[0] += 1
            if coor[0] == 25:
                zmi.rect.x -= SHAG * 24
                coor[0] = 1
            zmi.rect.x += SHAG
        posleposl = posl
        posl = napr

    screen.blit(pygame.transform.scale(load_image("map.png"), (WIDTH, HEIGHT)), (0, 0))  # TODO сделать музыку.
    tt_group.draw(screen)
    zm_group.draw(screen)
    pygame.display.flip()
    clock.tick(100)
