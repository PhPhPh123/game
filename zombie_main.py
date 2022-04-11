from global_names_and_imports import *
from subjects import MainPlayer
from guns import main_gun_func
from environment import blocks


pygame.init()
pygame.mixer.init()

'''
Loaded images and files
'''

main_map_image = pygame.image.load('main_map_blocks.png')

'''
Base parameters of game include colors, game window, etc
'''

''' В этом словаре находятся все координаты блоков(стены, край карты, баррикады, иные блоки). Ключем служит номер
объекта, а значением его координаты, где первые два значения это промежуток между x1 и x2, а последующие два значения
это промежутки между y1 и y2. По ходу игры могу добавляться новые блоки и убираться старые, поэтому данный словарь
актуален лишь на начало игры'''

game = True  # Flag of active game

pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()  # список спрайтов для обновления методами update
main_player = MainPlayer()
# экземпляр класса главного игрока в котором будет выполняться главный метод update
all_sprites.add(main_player)  # добавление экзепляров классов для выполнения в них методов update

if __name__ == "__main__":

    while game:  # Main game cycle
        clock.tick(fps)  # опеределяет количество обновлений экрана в секунду

        for event in pygame.event.get():  # This event will closed the game
            if event.type == pygame.QUIT:
                game = False

        win.blit(main_map_image, (0, 0))  # создание на экране главной карты
        main_gun_func()
        all_sprites.update()  # вызов методов update для отрисовки всех спрайтов
        pygame.display.flip()
