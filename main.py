import os
import pygame
import sys

pygame.init()
size = WIDTH, HEIGHT = 800, 400
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
player_image = load_image('G_zmeya.png')

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


class Zmeya(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(zm_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def generate_level(level):
    new_zm, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)  # TODO потом добавить стенки
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_zm = Zmeya(x, y)
    return new_zm, x, y


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    timer = 400
    while True:
        timer -= 1
        if timer == 0:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)
        # TODO сделать меню с кнопками


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
zmi, level_x, level_y = generate_level(load_level('pole.txt'))
running = True
camera = Camera()
napr = '-y'
# TODO змейка чёрная хотя фон должен быть пустым
coor = [5, 5]  # координаты змеи
timer = 75
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                napr = '-y'
            if event.key == pygame.K_LEFT:
                napr = '-x'
            if event.key == pygame.K_DOWN:
                napr = '+y'
            if event.key == pygame.K_RIGHT:
                napr = '+x'
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
                zmi.rect.x += SHAG * 11
                coor[0] = 11
            zmi.rect.x -= SHAG
        elif napr == '+y':
            coor[1] += 1
            if coor[1] == 13:
                zmi.rect.y -= SHAG * 12
                coor[1] = 1
            zmi.rect.y += SHAG
        elif napr == '+x':
            coor[0] += 1
            if coor[0] == 12:
                zmi.rect.x -= SHAG * 11
                coor[0] = 1
            zmi.rect.x += SHAG
    camera.update(zmi)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill(pygame.Color("green"))  # TODO сделать нормальный фон а дальше музыку.
    tt_group.draw(screen)
    zm_group.draw(screen)
    pygame.display.flip()
    clock.tick(100)

