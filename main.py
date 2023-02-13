import pygame
from pygame.locals import *

resolution = [800, 600]
bg = pygame.image.load('bg_castle.png')
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('p1_front.png')

        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0

    def update(self):
        self.calc_grav()

        self.rect.x += self.dx

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.dx > 0:
                self.rect.right = block.rect.left
            elif self.dx < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.dy

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.dy > 0:
                self.rect.bottom = block.rect.top
            elif self.dy < 0:
                self.rect.top = block.rect.bottom

            self.dy = 0

    def calc_grav(self):
        if self.dy == 0:
            self.dy = 1
        else:
            self.dy += .95

        if self.rect.y >= resolution[1] - self.rect.height and self.dy >= 0:
            self.dy = 0
            self.rect.y = resolution[1] - self.rect.height

    def jump(self):

        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        if len(platform_hit_list) > 0 or self.rect.bottom >= resolution[1]:
            self.dy = -24

    def go_left(self):
        self.dx = -10
        if (self.right):
            self.flip()
            self.right = False

    def go_right(self):
        self.dx = 10
        if (not self.right):
            self.flip()
            self.right = True

    def stop(self):
        self.dx = 0

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.image.load('grass.png')

        self.rect = self.image.get_rect()




class Level(object):
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()

    def draw(self, screen):
        screen.blit(bg, (0, 0))
        self.platform_list.draw(screen)


class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        # ширина, высота, x и y позиция
        level = [
            [210, 32, 500, 500],
            [210, 32, 200, 400],
            [210, 32, 600, 300],
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    pygame.init()

    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("*_*")

    player = Player()

    level_list = []
    level_list.append(Level_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = resolution[1] - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.go_left()
                if event.key == K_RIGHT:
                    player.go_right()
                if event.key == K_UP:
                    player.jump()

            if event.type == KEYUP:
                if event.key == K_LEFT and player.dx < 0:
                    player.stop()
                if event.key == K_RIGHT and player.dx > 0:
                    player.stop()

        active_sprite_list.update()

        current_level.update()

        if player.rect.right > resolution[0]:
            player.rect.right = resolution[0]

        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        pygame.draw.rect(screen, RED, player.rect, 1)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
