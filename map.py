import pygame

class Map(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y,offset):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.color=color
        self.rect = self.image.get_rect(center=(x+size/2, y+offset+size/2))

    def flash_black(self):
        self.image.fill((30, 30, 30))

    def flash_white(self):
        self.image.fill(self.color)

class Cherry(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.size=24
        place=pos
        self.image=pygame.transform.scale(pygame.image.load('assets\\pacman\\cherry.png'),(self.size,self.size))
        self.rect=self.image.get_rect(topleft=place)

class SpacialWall(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y,offset):
        super().__init__()
        self.image = pygame.Surface((3, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x+5, y + offset))

class Points(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y,offset):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x + size, y + offset+size))


shape=[
    'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'x                  xx                  x',
    'x qyyyyyycyyyyyyyc xx cyyyyyyycyyyyyyq x',
    'x y      y       y xx y       y      y x',
    'x y xxxx y xxxxx y xx y xxxxx y xxxx y x',
    'x z x  x y x   x y xx y x   x y x  x z x',
    'x y x  x y x   x y xx y x   x y x  x y x',
    'x y xxxx y xxxxx y xx y xxxxx y xxxx y x',
    'x y      y       y    y       y      y x',
    'x cyyyyyycyyyycyycyyyycyycyyyycyyyyyyc x',
    'x y      y    y          y    y      y x',
    'x y xxxx y xx y xxxxxxxx y xx y xxxx y x',
    'x y xxxx y xx y xxxxxxxx y xx y xxxx y x',
    'x y      y xx y    xx    y xx y      y x',
    'x cyyyyyyc xx cyyc xx cyyc xx cyyyyyyc x',
    'x        y xx    y xx y    xx y        x',
    'xxxxxxxx y xxxxx y xx y xxxxx y xxxxxxxx',
    '       x y xxxxx y xx y xxxxx y x       ',
    '       x y xx    y    y    xx y x       ',
    '       x y xx cyycyyyycyyc xx y x       ',
    '       x y xx y          y xx y x       ',
    'xxxxxxxx y xx y xxxxxxxx y xx y xxxxxxxx',
    '         y    y i      i y    y         ',
    'bbbbbbbbbcyyyycbisaaaasibcyyyycbbbbbbbbb',
    '         y    y i      i y    y         ',
    'xxxxxxxx y xx y xxxxxxxx y xx y xxxxxxxx',
    '       x y xx y          y xx y x       ',
    '       x y xx cyyyyyyyyyyc xx y x       ',
    '       x y xx y          y xx y x       ',
    '       x y xx y xxxxxxxx y xx y x       ',
    'xxxxxxxx y xx y xxxxxxxx y xx y xxxxxxxx',
    'x        y    y    xx    y    y        x',
    'x cyyyyyycyyyycyyc xx cyycyyyycyyyyyyc x',
    'x y      y       y xx y       y      y x',
    'x y xxxx y xxxxx y xx y xxxxx y xxxx y x',
    'x y xxxx y xxxxx y xx y xxxxx y xxxx y x',
    'x y   xx y       y    y       y xx   y x',
    'x cyc xx cyyyycyycypbycyycyyyyc xx cyc x',
    'x   y xx y    y          y    y xx y   x',
    'xxx y xx y xx y xxxxxxxx y xx y xx y xxx',
    'xxx y xx y xx y xxxxxxxx y xx y xx y xxx',
    'x   y    y xx y    xx    y xx y    y   x',
    'x cycyyyyc xx cyyc xx cyyc xx cyyyycyc x',
    'x y        xx    y xx y    xx        y x',
    'x z xxxxxxxxxxxx y xx y xxxxxxxxxxxx z x',
    'x y xxxxxxxxxxxx y xx y xxxxxxxxxxxx y x',
    'x y              y    y              y x',
    'x qyyyyyyyyyyyyyycyyyycyyyyyyyyyyyyyyq x',
    'x                                      x',
    'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
]


# x= visable wall
# y= points and road
# c= nodes and points
# q= alien time out pos
# p= player starting position
# b= road but not point
# s= node but no point
# i= aliens home walls
# z= special points
# a= aliens birth position
