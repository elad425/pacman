import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,size,blocksize):
        super().__init__()
        self.sprite=[[],[],[],[]]
        self.place=0
        self.sprite[0].append(pygame.transform.scale(pygame.image.load('assets\\pacman\\Pacman.png').convert_alpha(),(size,size)))
        self.sprite[0].append(pygame.transform.scale(pygame.image.load('assets\\pacman\\pacman close.png').convert_alpha(),(size,size)))
        self.sprite[1].append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets\\pacman\\Pacman.png').convert_alpha(),(size,size)),90))
        self.sprite[1].append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets\\pacman\\pacman close.png').convert_alpha(),(size,size)),90))
        self.sprite[2].append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets\\pacman\\Pacman.png').convert_alpha(),(size,size)), 180))
        self.sprite[2].append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets\\pacman\\pacman close.png').convert_alpha(),(size,size)), 180))
        self.sprite[3].append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets\\pacman\\Pacman.png').convert_alpha(),(size,size)), 270))
        self.sprite[3].append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load('assets\\pacman\\pacman close.png').convert_alpha(),(size,size)), 270))
        self.image = self.sprite[0][self.place]
        self.rect = self.image.get_rect(topleft=(pos[0],pos[1]))
        self.speed_x=0
        self.speed_y=0
        self.speed=2
        self.animation_pos=0
        self.right=False
        self.left=False
        self.up=False
        self.down=False
        self.history=0
        self.size=size
        self.block_size=blocksize

    def animation(self):
        self.place+=0.1
        if self.place>=len(self.sprite[0]):
            self.place=0

        if self.speed_x==self.speed:self.animation_pos=0
        elif self.speed_x==-self.speed:self.animation_pos=2
        elif self.speed_y==-self.speed:self.animation_pos=1
        elif self.speed_y==self.speed:self.animation_pos=3
        self.image=self.sprite[self.animation_pos][int(self.place)]

    def get_input(self,walls,width,corner,spacial_wall,road):
        self.check_direction()
        pos=self.get_pos()

        if self.right and pos in corner or self.right and self.speed_y==0:
            self.speed_x=self.speed
            self.speed_y = 0
        elif self.left and pos in corner or self.left and self.speed_y==0:
            self.speed_x=-self.speed
            self.speed_y = 0
        elif self.up and pos in corner or self.up and self.speed_x==0:
            self.speed_y=-self.speed
            self.speed_x = 0
        elif self.down and pos in corner or self.down and self.speed_x==0:
            self.speed_y=self.speed
            self.speed_x=0

        self.animation()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x<-10:
            self.rect.x=width+self.rect.width/2
        if self.rect.x>width+self.rect.width/2+5:
            self.rect.x=-10

        self.write_history(pos,road)
        self.check_crash(walls,spacial_wall)

    def get_pos(self):
        return [self.rect.x,self.rect.y]

    def check_crash(self,walls,spacial_wall):
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.speed_x == self.speed:
                    self.speed_x = 0
                    self.rect.x -= (self.block_size-(self.size-self.block_size)+self.speed)
                    if self.history=='up':self.speed_y=-self.speed
                    elif self.history=='down':self.speed_y=self.speed
                elif self.speed_x == -self.speed:
                    self.speed_x=0
                    self.rect.x += (self.block_size+self.speed)
                    if self.history=='up':self.speed_y=-self.speed
                    elif self.history=='down':self.speed_y=self.speed
                elif self.speed_y == self.speed:
                    self.speed_y=0
                    self.rect.y -= (self.block_size-(self.size-self.block_size)+self.speed)
                    if self.history=='left':self.speed_x=-self.speed
                    elif self.history=='right':self.speed_x=self.speed
                elif self.speed_y == -self.speed:
                    self.speed_y=0
                    self.rect.y += (self.block_size+self.speed)
                    if self.history=='left':self.speed_x=-self.speed
                    elif self.history=='right':self.speed_x=self.speed
                self.rect.x+=self.speed_x
                self.rect.y+=self.speed_y

        for wall in spacial_wall:
            if self.rect.colliderect(wall):
                if self.speed_x == self.speed:
                    self.speed_x=0
                    self.rect.x -= (8+self.speed)
                if self.speed_x == -self.speed:
                    self.speed_x=0
                    self.rect.x += (16+self.speed)

    def check_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.right = True
            self.left = False
            self.up = False
            self.down = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.right = False
            self.left = True
            self.up = False
            self.down = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.right = False
            self.left = False
            self.up = True
            self.down = False
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.right = False
            self.left = False
            self.up = False
            self.down = True

    def write_history(self,pos,road):
        if pos in road:
            if self.speed_x==self.speed:
                self.right=False
                self.history='right'
            elif self.speed_x==-self.speed:
                self.left=False
                self.history='left'
            elif self.speed_y==self.speed:
                self.down=False
                self.history='down'
            elif self.speed_y==-self.speed:
                self.up=False
                self.history='up'
