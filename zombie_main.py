import random
import pygame
from subjects import MainPlayer
from guns import main_gun_func

pygame.init()
pygame.mixer.init()

'''
Loaded images and files
'''

main_map_image = pygame.image.load('main_map_blocks.png')

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
main_player = MainPlayer(blocksdict, width_window, height_window, win, blocks, maingunlist)
# экземпляр класса главного игрока в котором будет выполняться главный метод update
all_sprites.add(main_player)  # добавление экзепляров классов для выполнения в них методов update

if __name__ == "__main__":

    while game:  # Main game cycle
        clock.tick(fps)  # опеределяет количество обновлений экрана в секунду

        for event in pygame.event.get():  # This event will closed the game
            if event.type == pygame.QUIT:
                game = False

        win.blit(main_map_image, (0, 0))  # создание на экране главной карты
        main_gun_func(maingunlist, width_window, height_window, win)
        all_sprites.update()  # вызов методов update для отрисовки всех спрайтов
        pygame.display.flip()
