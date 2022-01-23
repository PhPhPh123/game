import random

import pygame
from random import randint

pygame.init()
pygame.mixer.init()

'''
Loaded images and files
'''

main_map_image = pygame.image.load('zombie_game/main_map.png')

'''
Base parameters of game include colors, game window, etc
'''

width_window = 1800
height_window = 1000
fps = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

''' В этом словаре находятся все координаты блоков(стены, край карты, баррикады, иные блоки). Ключем служит номер
объекта, а значением его координаты, где первые два значения это промежуток между x1 и x2, а последующие два значения
это промежутки между y1 и y2. По ходу игры могу добавляться новые блоки и убираться старые, поэтому данный словарь
актуален лишь на начало игры'''
blocksdict = {1: (650, 1190, 170, 245), 2: (1030, 1150, 300, 420), 3: (1330, 1390, 410, 480),
              4: (1260, 1400, 480, 777), 5: (1310, 1367, 780, 920), 6: (480, 550, 250, 300),
              7: (450, 480, 280, 350), 8: (400, 450, 350, 490), 9: (390, 440, 600, 730),
              10: (400, 450, 700, 800), 11: (410, 470, 800, 900), 12: (540, 1270, 950, 1000)}

maingunlist = []


class MainPlayer(pygame.sprite.Sprite):  # class about actions of main player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('1.png'), pygame.image.load('2.png'), pygame.image.load('3.png'),
                       pygame.image.load('4.png')]  # список загруженных изображений основного игрока
        self.imageindex = 0  # индекс списка изображений, который меняется в методе imgform
        self.image = self.images[self.imageindex]  # основное изображение игрока отображаемое на экране
        self.rect = self.image.get_rect()  # параметр определяющий положение игрока на экране
        self.rect.center = (width_window / 2, height_window / 2)  # стартовая точка положения в начале игры
        self.noworientation = 0  # текущее ориентация(направление взгляда)игрока в пространстве
        self.blocksdict = blocksdict  # актуальный список блоков(преград) на игровой карте
        self.speed = 10  # параметр скорости основного игрока
        self.leftflag = False
        self.rightflag = False
        self.upflag = False
        self.downflag = False

    def orientation(self, angle: int):  # ротирует изображение исходя из угла полученного в параметре angle
        rotated_image = pygame.transform.rotate(self.image, angle)
        win.blit(rotated_image, (self.rect.centerx, self.rect.centery))  # отрисовка разворота игрока
        return None

    def imgform(self):  # определяет индекс изображения и возвращает текущее изображение для отрисовки
        if any((self.leftflag, self.rightflag, self.upflag, self.downflag)):
            self.imageindex += 1
            if self.imageindex > 3:
                self.imageindex = 0
            self.image = self.images[self.imageindex]
        return self.image

    def moving(self, keys):  # передвигает объект игрока на экране согласно ограничений по недоступным местам(блокам)
        if keys[pygame.K_a] and self.rect.centerx > 20 and blocks(self.rect.centerx, self.rect.centery, 'left',
                                                                  self.speed):
            self.rect.centerx -= self.speed
            self.leftflag = True
        else:
            self.leftflag = False

        if keys[pygame.K_d] and self.rect.centerx < width_window - 20 and blocks(self.rect.centerx, self.rect.centery,
                                                                                 'right', self.speed):
            self.rect.centerx += self.speed
            self.rightflag = True
        else:
            self.rightflag = False

        if keys[pygame.K_w] and self.rect.centery > 20 and blocks(self.rect.centerx, self.rect.centery, 'up',
                                                                  self.speed):
            self.rect.centery -= self.speed
            self.upflag = True
        else:
            self.upflag = False

        if keys[pygame.K_s] and self.rect.centery < height_window - 20 and blocks(self.rect.centerx, self.rect.centery,
                                                                                  'down', self.speed):
            self.rect.centery += self.speed
            self.downflag = True
        else:
            self.downflag = False

        return self.rect.centery, self.rect.centerx

    '''Метод определяет ориентацию игрока в пространстве согласно нажатию клавиш направления игрока(стрелки направления) 
    По умолчанию и на старте игры - направо. Int значения - угол разворота'''

    def orientkeys(self, keys):
        rightorientation = 0
        leftorientation = 180
        downorientation = 270
        uporientation = 90
        '''определение направление игрока согласно нажатой клавише, при отсутствии нажатия сохраняет прошлое значение
        через переменную noworintation '''
        if keys[pygame.K_RIGHT]:
            self.noworientation = rightorientation
            self.orientation(rightorientation)
        elif keys[pygame.K_UP]:
            self.noworientation = uporientation
            self.orientation(uporientation)
        elif keys[pygame.K_LEFT]:
            self.noworientation = leftorientation
            self.orientation(leftorientation)
        elif keys[pygame.K_DOWN]:
            self.noworientation = downorientation
            self.orientation(downorientation)
        else:
            self.orientation(self.noworientation)
        return None

    def startshooting(self, keys):
        if keys[pygame.K_f]:
            maingunlist.append(MainPlayerGun(self.rect.centerx, self.rect.centery, 2, RED, 50))

    def update(self, *args, **kwargs):  # центральный метод обновления, вызывающий иные методы
        keys = pygame.key.get_pressed()
        self.moving(keys)  # метод перемещающий игрока по экрану
        self.imgform()  # метод определения текущего изображения главного игрока
        self.orientkeys(keys)  # метод принимающий ввод клавиш для смены направления взгляда
        self.startshooting(keys)
        return None


class MainPlayerGun(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, speedproj):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speedproj = speedproj

    def DrawProjectile(self, win):
        pygame.draw.circle(win, self.color, (self.x+55, self.y+25), self.radius)


def blocks(x, y, move: str, speed):
    """Функция принимающая кординаты игрока и врагов по осям x и y, их скорость, направление движения в виде строки и
    возвращающая True , в случае если потенциальные координаты игрока/врага не пересекаются с координатами блоков, в ином
    случае возвращается False как знак того, что движение невозможно. Параметр скорости игрока/врага не должен превышать
    минимальную толщину объектов по любой из осей, иначе данные препятствия будут потенциально проницаемы"""
    if move == 'up':
        for block in blocksdict.values():
            if block[3] >= y - speed >= block[2] and block[0] <= x <= block[1]:
                return False
        else:
            return True
    if move == 'down':
        for block in blocksdict.values():
            if block[2] <= y + speed <= block[3] and block[0] <= x <= block[1]:
                return False
        else:
            return True
    if move == 'right':
        for block in blocksdict.values():
            if block[0] <= x + speed <= block[1] and block[2] <= y <= block[3]:
                return False
        else:
            return True
    if move == 'left':
        for block in blocksdict.values():
            if block[1] >= x - speed >= block[0] and block[2] <= y <= block[3]:
                return False
        else:
            return True



game = True  # Flag of active game

win = pygame.display.set_mode((width_window, height_window))  # главный игровой экран
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()  # список спрайтов для обновления методами update
main_player = MainPlayer()  # экземпляр класса главного игрока в котором будет выполняться главный метод update
all_sprites.add(main_player)  # добавление экзепляров классов для выполнения в них методов update

while game:  # Main game cycle
    clock.tick(fps)  # опеределяет количество обновлений экрана в секунду

    for event in pygame.event.get():  # This event will closed the game
        if event.type == pygame.QUIT:
            game = False

    win.blit(main_map_image, (0, 0))  # создание на экране главной карты

    for proj in maingunlist:
        if proj.y > 0:
            proj.y -= proj.speedproj - random.randint(-10, 10)
            proj.DrawProjectile(win)

    all_sprites.update()  # вызов методов update для отрисовки всех спрайтов
    pygame.display.flip()
