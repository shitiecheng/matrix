try:
    import pygame
    import sys
    from pygame.locals import *
    from random import randint
except:
    print("Load modules error!!")
    exit()

# 屏幕大小
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

# 速度区间
LOW_SPEED = 7
HIGH_SPEED = 30

# 文字大小区间
LOW_SIZE = 5
HIGH_SIZE = 30
FONT_SIZE = 20
FREQUENCE = 30

# 屏幕最大允许的字幕雨数量
MAX_WORD_RAIN = 128
# 每一步最大可以添加的字幕雨数量
MAX_WORD_INCREASEMENT= 7


def green_color():
    return (0, 238, 0)


def deep_green_color():
    return (0, 139, 69)


def gray_color():
    return (190, 190, 190)


def light_gray_color():
    return (211, 211, 211)


# 随机生成速度
def random_speed():
    return randint(LOW_SPEED, HIGH_SPEED)


# 随机生成8位二进制字幕
def random_byte32():
    return '{:08b}'.format(randint(0, 128))


# 随机生成字体大小
def random_font_size():
    return randint(LOW_SIZE, HIGH_SIZE)


# 单个字符精灵
class Word(pygame.sprite.Sprite):
    def __init__(self, bornposition, value, speed, font_size, color):
        pygame.sprite.Sprite.__init__(self)
        self.value = value
        self.font = pygame.font.SysFont("arial", font_size)
        self.image = self.font.render(str(self.value), True, color)

        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.topleft = bornposition

    def update(self):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# 8位字符组
class WordGroup(pygame.sprite.Group):
    def __init__(self, born_position_x, born_position_y, char_seq, speed, font_size):
        pygame.sprite.Group.__init__(self)
        # 创建一个字幕组
        # self.group = pygame.sprite.Group()
        for i in range(len(char_seq)):
            if i == 0:
                self.add(Word((born_position_x, born_position_y * i), char_seq[i], speed, font_size, gray_color()))
            elif i == 1:
                self.add(Word((born_position_x, born_position_y * i), char_seq[i], speed, font_size, green_color()))
            else:
                self.add(Word((born_position_x, born_position_y * i), char_seq[i], speed, font_size, deep_green_color()))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("字幕雨")

# 初始化字幕雨list 存放所有的单个字幕组
groups = [WordGroup(randint(0, SCREEN_WIDTH), -FONT_SIZE, random_byte32(), random_speed(),
                    randint(LOW_SIZE, HIGH_SIZE))]


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    screen.fill((0, 0, 0))

    for g in groups:
        g.update()
        g.draw(screen)
        if g.__len__() == 0:
            groups.remove(g)
    # print('当前字幕雨数量:', groups.__len__())
    if groups.__len__() < MAX_WORD_RAIN:
        for i in range(MAX_WORD_INCREASEMENT):
            if groups.__len__() < MAX_WORD_RAIN:
                font_size = random_font_size()
                w_group = WordGroup(randint(0, SCREEN_WIDTH), -font_size, random_byte32(), random_speed(),
                                    font_size)
                groups.append(w_group)
            else:
                break

    pygame.display.update()
