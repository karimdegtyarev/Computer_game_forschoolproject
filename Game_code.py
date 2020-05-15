import pygame
import sys
import os


# Функция для выхода из игры
def terminate():
    pygame.quit()
    sys.exit()


# Загрузка фотографии
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Далее идут индивидуальные фукции для загрузки отдельных фотографий
# Изображение шипа повёрнутого вправо
def load_image_thorn_right(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((150, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Изображение шипа повёрнутого влево
def load_image_thorn_left(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((1, 5))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Изображение шипа повёрнутого вверх
def load_image_thorn_top(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((6, 12))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Изображение шипа повёрнутого вниз
def load_image_thorn_down(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 160))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Загружаем уровень
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Создаем и размещаем все объекты по местам
def generate_level(levelmap):
    global door
    global key
    first_player, x, y = None, None, None
    fon = pygame.transform.scale(
        load_image('game_back_fon.png'),
        (width, height))
    screen.blit(fon, (0, 0))
    for y in range(len(levelmap)):
        for x in range(len(levelmap[y])):
            if levelmap[y][x] == '.':
                Tile('wall', x, y)
            elif levelmap[y][x] == '1':
                Tile("right", x, y)
            elif levelmap[y][x] == '2':
                Tile("left", x, y)
            elif levelmap[y][x] == '3':
                Tile("top", x, y)
            elif levelmap[y][x] == '4':
                Tile("down", x, y)
    door = Door(49, 25.7)
    first_player = Player(5, 13)
    key = Key(52, 6)
    return first_player, x, y


# Создаем объект - ключ
class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(key_group, all_sprites)
        self.image = key_image
        self.type = "key"
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


# Создаем объект - дверь
class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.image = door_image
        self.type = "door"
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


# Создаем стены и все виды шипов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# Создаем игрока и все его способности
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.jump_power = 35
        self.jump_check = False
        self.image = player_image
        self.type = "player"
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    # Анимация движения влево и вправо
    def update(self):
        global walk_r_count
        global walk_l_count
        clock.tick(fps)
        if move_1 == "Right":
            if not self.jump_check:
                player.image = walkRight[walk_r_count]
                walk_r_count += 1
                if walk_r_count == 12:
                    walk_r_count = 0
            player.move(+step, 0)
        if move_1 == "Left":
            if not self.jump_check:
                player.image = walkLeft[walk_l_count]
                walk_l_count += 1
                if walk_l_count == 12:
                    walk_l_count = 0
            player.move(-step, 0)

    # Само движение игрока путем изменения координат объекта - Player
    # ,а также реакция на шипы,на удар об потолок или об пол
    def move(self, dx, dy):
        global gravity_step
        global door
        global key
        global jump_step
        global which_level
        self.rect.x += dx
        self.rect.y += dy
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        test1 = pygame.sprite.spritecollide(self, key_group, False)
        test2 = pygame.sprite.spritecollide(self, door_group, False)
        if width - 60 < self.rect.x < width:
            which_level += 1
        for obj in test1:
            Key.kill(obj)
            Door.kill(door)
        for obj in test2:
            self.rect.x -= dx
            self.rect.y -= dy
            break
        for obj in test:
            self.image = player_image
            if obj.type == "right":
                self.rect.x = tile_width * self.pos_x + 15
                self.rect.y = tile_height * self.pos_y + 5
                break
            elif obj.type == "left":
                self.rect.x = tile_width * self.pos_x + 15
                self.rect.y = tile_height * self.pos_y + 5
                break
            elif obj.type == "top":
                self.rect.x = tile_width * self.pos_x + 15
                self.rect.y = tile_height * self.pos_y + 5
                break
            elif obj.type == "down":
                self.rect.x = tile_width * self.pos_x + 15
                self.rect.y = tile_height * self.pos_y + 5
                self.jump_check = False
                self.jump_power = 35
                gravity_step = 2
                jump_step = 8
                break
        for obj in test:
            if obj.type == "wall":
                if dy > 0:
                    gravity_step = 2
                    jump_step = 8
                    self.jump_power = 35
                    self.jump_check = False
                    self.image = player_image
                    while not bool(test):
                        self.rect.y -= 0.0001
                elif dy < 0:
                    gravity_step = 2
                    jump_step = 8
                    self.jump_power = 35
                    self.jump_check = False
                self.rect.x -= dx
                self.rect.y -= dy
                break

    # Осуществляет функцию прыжка
    def move_up(self):
        global JUMP_GRAVITY
        global jump_step
        self.move(0, -jump_step)
        jump_step *= JUMP_GRAVITY
        self.jump_power -= 1
        if self.jump_power == 0:
            self.jump_check = False

    # Сила гравитации
    def gravity(self):
        global GRAVITY
        global gravity_step
        self.jump_power = 35
        self.move(0, gravity_step)
        gravity_step /= GRAVITY

    # Проверка объект на земле или нет
    def on_ground_or_not(self):
        global step
        self.rect.y += step
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        if len(test) > 0:
            self.rect.y -= step
            return True
        else:
            return False


# Создание фона, названий уровней, обновление груп и экрана
def start_screen():
    global tiles_group
    global all_sprites
    global player_group
    global key_group
    global door_group
    global freeze
    global stop
    global GRAVITY
    global JUMP_GRAVITY
    global jump_step
    global gravity_step
    global player
    global move_1
    global walk_r_count
    global walk_l_count
    global which_level
    global which_level_past
    global key
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    key_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    fon = pygame.transform.scale(
        load_image('game_start_fon.jpg'),
        (width, height))
    fon1 = pygame.transform.scale(
        load_image('game_back_fon.png'),
        (width, height))
    intro_text_levels = [""]
    move_1 = "Stop"
    if which_level != which_level_past:
        which_level_past += 1
        if which_level != 1:
            player.kill()
        player, level_x, level_y = generate_level(load_level('map'))
        intro_text_levels = ["01.Тут всё просто"]
    running = True
    # Основной цикл :принятие информации с клавиш
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                stop = 0
            # Пауза
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB and stop == 0:
                freeze = (freeze + 1) % 2
            if freeze == 0 and stop == 0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    move_1 = "Left"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    move_1 = "Right"

                if event.type == pygame.KEYUP and \
                        event.key == pygame.K_LEFT and move_1 == "Left":
                    move_1 = "Stop"
                    walk_l_count = 0
                    if not player.jump_check:
                        player.image = player_image

                if event.type == pygame.KEYUP and \
                        event.key == pygame.K_RIGHT and move_1 == "Right":
                    move_1 = "Stop"
                    walk_r_count = 0
                    if not player.jump_check:
                        player.image = player_image

                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    move_1 = "Left"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    move_1 = "Right"

                if event.type == pygame.KEYUP and event.key == pygame.K_a and move_1 == "Left":
                    move_1 = "Stop"
                    walk_l_count = 0
                    if not player.jump_check:
                        player.image = player_image

                if event.type == pygame.KEYUP and event.key == pygame.K_d and move_1 == "Right":
                    move_1 = "Stop"
                    walk_r_count = 0
                    if not player.jump_check:
                        player.image = player_image

                if player.on_ground_or_not():
                    if event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_UP:
                        move_1 = "Up"
                        player.jump_check = True
                    if event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_w:
                        move_1 = "Up"
                        player.jump_check = True
        if freeze == 0 and stop == 0:
            if player.jump_check:
                player.image = jump
                player.move_up()
            elif not player.on_ground_or_not() and not player.jump_check:
                player.image = fall
                player.gravity()
        if stop == 1:
            intro_text = ["Press 'space' to start"]
            screen.blit(fon, (0, 0))
            pygame.init()
            font = pygame.font.Font(None, 50)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('grey'))
                intro_rect = string_rendered.get_rect()
                text_coord += 570
                intro_rect.top = text_coord
                intro_rect.x = 475
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

            pygame.display.flip()
        # Определение уровня и включение особенностей этого уровня
        if freeze == 0 and stop == 0:
            if which_level != which_level_past:
                which_level_past += 1
                GRAVITY = 0.95
                gravity_step = 2
                JUMP_GRAVITY = 0.98
                jump_step = 8
                walk_r_count = 0
                walk_l_count = 0
                if which_level != 1:
                    player.kill()
                if which_level == 2:
                    player, level_x, level_y = generate_level(load_level('map'))
                    intro_text_levels = ["02.Ключ невидимка"]
                    key.image = invisible
                    key.rect.x = 300
                    key.rect.y = 640
                elif which_level == 3:
                    player, level_x, level_y = generate_level(load_level('map'))
                    intro_text_levels = ["03.Смертельный номер"]
                    key.rect.x = 850
                    key.rect.y = 220
                elif which_level == 4:
                    run = True
                    the_end_image = load_image("the_end_of_game_fon.jpg")
                    while run:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                        congratulations = ["Мои поздравления-вы прошли игру.",
                                           "Спасибо вам за прохождение!",
                                           "Надеюсь моя игра подарила вам хорошие впечатления.",
                                           'Продолжение следует.']
                        screen.blit(the_end_image, (0, 0))
                        pygame.init()
                        font = pygame.font.Font(None, 50)
                        text_coord = 50
                        for line in congratulations:
                            string_rendered = font.render(line, 1, (150, 150, 150))
                            intro_rect = string_rendered.get_rect()
                            text_coord += 10
                            intro_rect.top = text_coord
                            intro_rect.x = 250
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)
                        pygame.display.flip()
                    break

            player.update()
            screen.fill((0, 0, 0))
            screen.blit(fon1, (0, 0))
            tiles_group.draw(screen)
            key_group.draw(screen)
            door_group.draw(screen)
            pygame.init()
            font = pygame.font.Font(None, 50)
            text_coord = 50
            for line in intro_text_levels:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 220
                intro_rect.top = text_coord
                intro_rect.x = 400
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            player_group.draw(screen)
            pygame.display.flip()


# Постоянные переменные а также фотографии
size = width, height = 1260, 690
screen = pygame.display.set_mode(size)
pygame.display.set_caption("One Level")
clock = pygame.time.Clock()
step = 4
GRAVITY = 0.95
gravity_step = 2
JUMP_GRAVITY = 0.98
jump_step = 8
walk_r_count = 0
walk_l_count = 0
stop = 1
freeze = 0
v = 200
fps = 30
which_level = 1
which_level_past = 0
wall_image = load_image('wall.png')
door_image = pygame.transform.scale(load_image("door.png", -1), (30, 150))
player_image = pygame.transform.scale(load_image("standing.png", -1), (28, 57))
jump = pygame.transform.scale(load_image('jump.png', -1), (28, 57))
fall = pygame.transform.scale(load_image('fall.png', -1), (28, 57))
walkRight = [pygame.transform.scale(load_image('r1.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r1.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r2.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r2.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r3.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r3.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r4.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r4.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r5.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r5.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r6.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r6.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r7.png', -1), (28, 57)),
             pygame.transform.scale(load_image('r7.png', -1), (28, 57))]
walkLeft = [pygame.transform.scale(load_image('l1.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l1.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l2.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l2.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l3.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l3.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l4.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l4.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l5.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l5.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l6.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l6.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l7.png', -1), (28, 57)),
            pygame.transform.scale(load_image('l7.png', -1), (28, 57))]

key_image = pygame.transform.scale(load_image('key.png', -1), (40, 44))
invisible = pygame.transform.scale(load_image('invisible.jpg', -1), (40, 44))
tile_images = {"wall": load_image("wall.png"),
               "right": pygame.transform.scale(load_image_thorn_right("right_normal.png", -1),
                                               (21, 21)),
               "left": pygame.transform.scale(load_image_thorn_left("left_normal.png", -1),
                                              (21, 21)),
               "top": pygame.transform.scale(load_image_thorn_top("top_normal.png", -1), (21, 21)),
               "down": pygame.transform.scale(load_image_thorn_down("down_normal.png", -1),
                                              (21, 21))}
tile_width = tile_height = 21
if __name__ == "__main__":
    start_screen()
