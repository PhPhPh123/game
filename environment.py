from global_names_and_imports import *


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
