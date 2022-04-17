from global_names_and_imports import *
from subjects import MainPlayer, Zombie, main_player, main_zombie
from guns import main_gun_func
from environment import blocks


pygame.init()
pygame.mixer.init()

'''
Loaded images and files
'''

main_map_image = pygame.image.load('Images/main_map_blocks.png')

'''
Base parameters of game include colors, game window, etc
'''



game = True  # Flag of active game

pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()  # список спрайтов для обновления методами update
all_sprites.add(main_player, main_zombie) # добавление экзепляров классов для выполнения в них методов update

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
