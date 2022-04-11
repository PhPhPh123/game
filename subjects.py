from guns import MainPlayerGun
from environment import blocks
from global_names_and_imports import *


class Base_Subjects(pygame.sprite.Sprite):  # class about actions of main player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()  # параметр определяющий положение игрока на экране
        self.rect.center = (width_window / 2, height_window / 2)  # стартовая точка положения в начале игры


class MainPlayer(Base_Subjects):  # class about actions of main player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('1.png'), pygame.image.load('2.png'), pygame.image.load('3.png'),
                       pygame.image.load('4.png')]  # список загруженных изображений основного игрока
        self.imageindex = 0  # индекс списка изображений, который меняется в методе imgform
        self.image = self.images[self.imageindex]  # основное изображение игрока отображаемое на экране
        self.rect = self.image.get_rect()  # параметр определяющий положение игрока на экране
        self.rect.center = (width_window / 2, height_window / 2)  # стартовая точка положения в начале игры
        self.noworientation = 0  # текущее ориентация(направление взгляда)игрока в пространстве
        self.speed = 10  # параметр скорости основного игрока

        self.leftflag_Moving = False
        self.rightflag_Moving = False
        self.upflag_Moving = False
        self.downflag_Moving = False

        self.leftflag_Orientation = False
        self.rightflag_Orientation = False
        self.upflag_Orientation = False
        self.downflag_Orientation = False

    def orientation(self, angle: int):  # ротирует изображение исходя из угла полученного в параметре angle
        rotated_image = pygame.transform.rotate(self.image, angle)
        win.blit(rotated_image, (self.rect.centerx, self.rect.centery))  # отрисовка разворота игрока
        return None

    def imgform(self):  # определяет индекс изображения и возвращает текущее изображение для отрисовки
        if any((self.leftflag_Moving, self.rightflag_Moving, self.upflag_Moving, self.downflag_Moving)):
            self.imageindex += 1
            if self.imageindex > 3:
                self.imageindex = 0
            self.image = self.images[self.imageindex]
        return self.image

    def moving(self, keys):  # передвигает объект игрока на экране согласно ограничений по недоступным местам(блокам)
        if keys[pygame.K_a] and self.rect.centerx > 20 and blocks(self.rect.centerx, self.rect.centery, 'left',
                                                                  self.speed):
            self.rect.centerx -= self.speed
            self.leftflag_Moving = True
        else:
            self.leftflag_Moving = False

        if keys[pygame.K_d] and self.rect.centerx < width_window - 20 and blocks(self.rect.centerx,
                                                                                 self.rect.centery,
                                                                                 'right', self.speed):
            self.rect.centerx += self.speed
            self.rightflag_Moving = True
        else:
            self.rightflag_Moving = False

        if keys[pygame.K_w] and self.rect.centery > 20 and blocks(self.rect.centerx, self.rect.centery, 'up',
                                                                  self.speed):
            self.rect.centery -= self.speed
            self.upflag_Moving = True
        else:
            self.upflag_Moving = False

        if keys[pygame.K_s] and self.rect.centery < height_window - 20 and blocks(self.rect.centerx,
                                                                                  self.rect.centery,
                                                                                  'down', self.speed):
            self.rect.centery += self.speed
            self.downflag_Moving = True
        else:
            self.downflag_Moving = False

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
            self.rightflag_Orientation = True
            self.leftflag_Orientation = False
            self.upflag_Orientation = False
            self.downflag_Orientation = False

        elif keys[pygame.K_UP]:
            self.noworientation = uporientation
            self.orientation(uporientation)
            self.upflag_Orientation = True
            self.rightflag_Orientation = False
            self.leftflag_Orientation = False
            self.downflag_Orientation = False

        elif keys[pygame.K_LEFT]:
            self.noworientation = leftorientation
            self.orientation(leftorientation)
            self.leftflag_Orientation = True
            self.rightflag_Orientation = False
            self.upflag_Orientation = False
            self.downflag_Orientation = False

        elif keys[pygame.K_DOWN]:
            self.noworientation = downorientation
            self.orientation(downorientation)
            self.downflag_Orientation = True
            self.rightflag_Orientation = False
            self.upflag_Orientation = False
            self.leftflag_Orientation = False

        else:
            self.orientation(self.noworientation)
        return None

    def startshooting(self, keys):
        if keys[pygame.K_LCTRL]:
            if self.upflag_Orientation:
                maingunlist.append(MainPlayerGun(self.rect.centerx, self.rect.centery, 2, RED, 50, "up"))
            if self.downflag_Orientation:
                maingunlist.append(MainPlayerGun(self.rect.centerx, self.rect.centery, 2, RED, 50, "down"))
            if self.rightflag_Orientation:
                maingunlist.append(MainPlayerGun(self.rect.centerx, self.rect.centery + 34, 2, RED, 50, "right"))
            if self.leftflag_Orientation:
                maingunlist.append(MainPlayerGun(self.rect.centerx, self.rect.centery + 34, 2, RED, 50, "left"))

    def update(self, *args, **kwargs):  # центральный метод обновления, вызывающий иные методы
        keys = pygame.key.get_pressed()
        self.moving(keys)  # метод перемещающий игрока по экрану
        self.imgform()  # метод определения текущего изображения главного игрока
        self.orientkeys(keys)  # метод принимающий ввод клавиш для смены направления взгляда
        self.startshooting(keys)
        return None


class Zombie(Base_Subjects):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load('Screenshot_9.png')]  # список загруженных изображений основного игрока
        self.imageindex = 0  # индекс списка изображений, который меняется в методе imgform
        self.image = self.images[self.imageindex]  # основное изображение игрока отображаемое на экране
        self.rect = self.image.get_rect()  # параметр определяющий положение игрока на экране
        self.rect.center = (150, 150)

    def update(self, *args, **kwargs):  # центральный метод обновления, вызывающий иные методы
        return None
