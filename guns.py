from global_names_and_imports import *


class MainPlayerGun(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, speedproj, direction_of_fire):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speedproj = speedproj
        self.direction_of_fire = direction_of_fire

    def DrawProjectile(self):
        pygame.draw.circle(win, self.color, (self.x + 55, self.y + 25), self.radius)


def main_gun_func():
    for proj in maingunlist:
        if proj.y > 0 and proj.direction_of_fire == "up":
            proj.y -= proj.speedproj - random.randint(-10, 10)
            proj.DrawProjectile()

        if proj.y < height_window and proj.direction_of_fire == "down":
            proj.y += proj.speedproj + random.randint(-10, 10)
            proj.DrawProjectile()

        if proj.x < width_window and proj.direction_of_fire == "right":
            proj.x += proj.speedproj + random.randint(-10, 10)
            proj.DrawProjectile()

        if proj.x > 0 and proj.direction_of_fire == "left":
            proj.x -= proj.speedproj - random.randint(-10, 10)
            proj.DrawProjectile()



