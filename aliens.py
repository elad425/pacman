import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,size,color,birthpos,home,blocksize):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets\\pacman\\aliens\\'+ color +' right.png').convert_alpha(),(size,size))
        self.retreat_sound=pygame.mixer.Sound('sounds\\retreating.wav')
        self.size=size
        self.speed_x = 0
        self.speed_y = 0
        self.speed= 1

        self.check_up=False
        self.check_down=False
        self.check_left=False
        self.check_right=False
        self.ghost_mode=False
        self.alien_mode=False
        self.dead_mode=False
        self.corner_time=False
        self.locked=True
        self.rush=False

        self.history=''
        self.angry=''
        self.color=color
        self.dead_time=300
        self.dead_timer=self.dead_time
        self.start_haunt_time=0
        self.start_haunt_list=[0,300,700,1200]
        self.home_list=home
        self.ghost_time=0
        self.block_size=blocksize

        self.corner=[]
        self.x,self.y=0,0
        self.alien_birth_list = birthpos
        self.alien_birth_place = []
        self.create_identity()
        self.corner_timer = self.x
        self.haunt_timer = self.y
        self.rect = self.image.get_rect(topleft=(self.alien_birth_place[0], self.alien_birth_place[1]))

    def haunt(self,player_pos,alien_pos,corner,walls,road,width,is_okay,rush):
        self.go_to_corner()
        self.start_haunting(is_okay)
        self.rush=rush

        if self.corner_time or self.ghost_mode:
            player_pos=self.corner
        if self.dead_mode or self.locked or not is_okay:
            player_pos=self.alien_birth_place

        distance_y = player_pos[1] - alien_pos[1]
        distance_x = player_pos[0] - alien_pos[0]

        if alien_pos in corner:
            if abs(distance_x)<=abs(distance_y):
                if distance_y>0:
                    if distance_x>0:
                        if not self.check_down and self.history!='up':self.move_down()
                        elif not self.check_right and self.history!='left':self.move_right()
                        elif not self.check_left and self.history!='right':self.move_left()
                        elif not self.check_up and self.history!='down':self.move_up()
                    else:
                        if not self.check_down and self.history!='up':self.move_down()
                        elif not self.check_left and self.history!='right':self.move_left()
                        elif not self.check_right and self.history!='left':self.move_right()
                        elif not self.check_up and self.history!='down':self.move_up()
                else:
                    if distance_x>0:
                        if not self.check_up and self.history!='down':self.move_up()
                        elif not self.check_right and self.history!='left':self.move_right()
                        elif not self.check_left and self.history!='right':self.move_left()
                        elif not self.check_down and self.history!='up':self.move_down()
                    else:
                        if not self.check_up and self.history!='down':self.move_up()
                        elif not self.check_left and self.history!='right':self.move_left()
                        elif not self.check_right and self.history!='left':self.move_right()
                        elif not self.check_down and self.history!='up':self.move_down()
            else:
                if distance_x>0:
                    if distance_y>0:
                        if not self.check_right and self.history!='left':self.move_right()
                        elif not self.check_down and self.history!='up':self.move_down()
                        elif not self.check_up and self.history!='down':self.move_up()
                        elif not self.check_left and self.history!='right':self.move_left()
                    else:
                        if not self.check_right and self.history!='left':self.move_right()
                        elif not self.check_up and self.history!='down':self.move_up()
                        elif not self.check_down and self.history!='up':self.move_down()
                        elif not self.check_left and self.history!='right':self.move_left()
                else:
                    if distance_y>0:
                        if not self.check_left and self.history!='right':self.move_left()
                        elif not self.check_down and self.history!='up':self.move_down()
                        elif not self.check_up and self.history!='down':self.move_up()
                        elif not self.check_right and self.history!='left':self.move_right()
                    else:
                        if not self.check_left and self.history!='right':self.move_left()
                        elif not self.check_up and self.history!='down':self.move_up()
                        elif not self.check_down and self.history!='up':self.move_down()
                        elif not self.check_right and self.history!='left':self.move_right()

        self.check_on_road(alien_pos,road)
        self.check_crashing(walls)

        self.rect.y+=self.speed_y
        self.rect.x+=self.speed_x

        if self.rect.x<-10:
            self.rect.x=width+self.rect.width/2
        if self.rect.x>width+self.rect.width/2+5:
            self.rect.x=-10

        self.revive()
        self.warning()
        self.write_history(alien_pos,road)
        self.rush_mode()

    def check_on_road(self,alien_pos,road):
        if alien_pos in road:
            self.check_up = False
            self.check_down = False
            self.check_left = False
            self.check_right = False

    def move_right(self):
        self.speed_x = self.speed
        self.speed_y = 0
        if self.alien_mode:
            self.image = pygame.transform.scale(pygame.image.load('assets\\pacman\\aliens\\'+self.angry+self.color+' right.png').convert_alpha(),(self.size,self.size))

    def move_left(self):
        self.speed_x = -self.speed
        self.speed_y = 0
        if self.alien_mode:
            self.image = pygame.transform.scale(pygame.image.load('assets\\pacman\\aliens\\'+self.angry+self.color+' left.png').convert_alpha(),(self.size,self.size))

    def move_up(self):
        self.speed_y = -self.speed
        self.speed_x = 0
        if self.alien_mode:
            self.image = pygame.transform.scale(pygame.image.load('assets\\pacman\\aliens\\'+self.angry+self.color+' up.png').convert_alpha(),(self.size,self.size))

    def move_down(self):
        self.speed_y = self.speed
        self.speed_x = 0
        if self.alien_mode:
            self.image = pygame.transform.scale(pygame.image.load('assets\\pacman\\aliens\\'+self.angry+self.color+' down.png').convert_alpha(),(self.size,self.size))

    def check_crashing(self,walls):
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.speed_x == self.speed:
                    self.rect.x -= (self.block_size-(self.size-self.block_size)+self.speed)
                    self.speed_x=0
                    self.check_right=True
                elif self.speed_x == -self.speed:
                    self.rect.x += (self.block_size+self.speed)
                    self.speed_x=0
                    self.check_left=True
                elif self.speed_y == self.speed:
                    self.rect.y -= (self.block_size-(self.size-self.block_size)+self.speed)
                    self.speed_y=0
                    self.check_down=True
                elif self.speed_y == -self.speed:
                    self.rect.y += (self.block_size+self.speed)
                    self.speed_y=0
                    self.check_up=True

    def get_pos(self):
        return [self.rect.x,self.rect.y]

    def go_to_corner(self):
        self.corner_timer-=1
        if self.corner_timer<0:
            self.corner_time=True
            self.haunt_timer-=1
        if self.haunt_timer<=0 and self.corner_time:
            self.corner_time=False
            self.corner_timer=self.x
            self.haunt_timer=self.y

    def create_identity(self):
        if self.color=='red':
            self.x, self.y = 5000, 50
            self.corner=self.home_list[0]
            self.alien_birth_place=self.alien_birth_list[0]
            self.start_haunt_time=self.start_haunt_list[0]
            self.speed_x=self.speed
        if self.color=='blue':
            self.x,self.y=1000,400
            self.corner = self.home_list[1]
            self.alien_birth_place=self.alien_birth_list[1]
            self.start_haunt_time=self.start_haunt_list[1]
            self.speed_x = -self.speed
        if self.color=='pink':
            self.x,self.y=750,400
            self.corner = self.home_list[2]
            self.alien_birth_place=self.alien_birth_list[2]
            self.start_haunt_time=self.start_haunt_list[2]
            self.speed_x = self.speed
        if self.color=='yellow':
            self.x,self.y=500,400
            self.corner = self.home_list[3]
            self.alien_birth_place=self.alien_birth_list[3]
            self.start_haunt_time=self.start_haunt_list[3]
            self.speed_x = -self.speed

    def turn_ghost(self):
        if not self.locked:
            self.ghost_mode=True
            self.alien_mode=False
            self.dead_mode=False
            self.speed=1
            self.ghost_time=500
            self.image= pygame.transform.scale(pygame.image.load('assets\\pacman\\ghost.png').convert_alpha(),(self.size,self.size))

    def turn_alien(self):
        self.alien_mode=True
        self.ghost_mode=False
        self.dead_mode=False
        self.locked=False
        self.speed=1
        self.ghost_time=0
        self.image= pygame.transform.scale(pygame.image.load('assets\\pacman\\aliens\\'+self.color+' right.png').convert_alpha(),(self.size,self.size))

    def turn_dead(self):
        self.alien_mode = False
        self.ghost_mode = False
        self.dead_mode = True
        self.speed=4
        self.ghost_time=0
        self.image= pygame.transform.scale(pygame.image.load('assets\\pacman\\ghost eyes.png').convert_alpha(),(self.size,self.size))

    def warning(self):
        if self.ghost_time:self.ghost_time-=1
        if 0<self.ghost_time <=150 and self.ghost_mode:
            if self.ghost_time % 30 == 0:
                self.image = pygame.transform.scale(pygame.image.load('assets\\pacman\\white ghost.png').convert_alpha(),(self.size,self.size))
            elif self.ghost_time % 15 == 0:
                self.image = pygame.transform.scale(pygame.image.load('assets\\pacman\\ghost.png').convert_alpha(),(self.size,self.size))

    def get_ghost_state(self):
        return self.ghost_mode

    def get_alien_state(self):
        return self.alien_mode

    def get_dead_state(self):
        return self.dead_mode

    def revive(self):
        if self.dead_mode:
            if self.dead_timer==self.dead_time:
                self.retreat_sound.play(-1)
            self.dead_timer-=1
        if self.dead_timer==0:
            self.retreat_sound.stop()
            self.turn_alien()
            self.dead_timer=self.dead_time

    def start_haunting(self,is_okay):
        if is_okay:
            if self.start_haunt_time==0:
                self.turn_alien()
            self.start_haunt_time-=1

    def write_history(self,pos,road):
        if pos in road:
            if self.speed_x==self.speed:self.history='right'
            elif self.speed_x==-self.speed:self.history='left'
            elif self.speed_y==self.speed:self.history='down'
            elif self.speed_y==-self.speed:self.history='up'
        if pos==self.alien_birth_place:self.history=''

    def rush_mode(self):
        if self.rush and self.alien_mode:
            if self.color=='red':
                self.speed=2
                self.angry='angry '
