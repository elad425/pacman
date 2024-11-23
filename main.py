import pygame,sys
from random import choice,randint

import pacman.map
from player import Player
from aliens import Alien
from map import Cherry

offset=30
block_size=12
ticks=60

width = len(pacman.map.shape[0])*block_size
height = len(pacman.map.shape)*block_size+offset
screen = pygame.display.set_mode((width, height))

buff_mod=pygame.USEREVENT+1
siren_play=pygame.USEREVENT+2

pygame.init()
background_music=pygame.mixer.Sound('sounds\\pacman_beginning.wav')
background_music.play(-1)


class Game:
    def __init__(self):
        self.corner_list = []
        self.road_list = []
        self.alien_time_out_list = []
        self.player_start_pos=[]
        self.alien_birth_pos=[]

        self.shape = pacman.map.shape
        self.player_size = block_size+8
        self.alien_size = block_size+8
        self.block_size = block_size
        self.point_size = int(block_size/4)
        self.walls = pygame.sprite.Group()
        self.spacial_wall=pygame.sprite.Group()
        self.points = pygame.sprite.Group()
        self.spacial = pygame.sprite.Group()
        self.create_map(0, 0)

        self.high_score = open("pacman highscore.txt", "r").read()
        self.ready_surface=pygame.transform.scale(pygame.image.load('assets\\pacman\\ready.jpg'),(100,20))
        self.live_surface=pygame.transform.scale(pygame.image.load('assets\\pacman\\Pacman.png').convert_alpha(),(self.player_size,self.player_size))
        self.font=pygame.font.Font('assets\\space invaders\\Pixeled.ttf',10)
        self.end_font = pygame.font.Font('assets\\space invaders\\Pixeled.ttf', 50)
        self.end_image = pygame.Surface((width, height))
        self.end_image.fill((30,30,30))
        self.end_rect = self.end_image.get_rect()

        self.player_start_x=self.player_start_pos[0]
        self.player_start_y=self.player_start_pos[1]
        self.player_sprite = Player((self.player_start_x, self.player_start_y),self.player_size,block_size)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.aliens=pygame.sprite.Group()
        self.alien_amount= 4
        self.aliens_colors=['red','pink','yellow','blue']
        self.alien_create()

        self.cherry_surface=pygame.transform.scale(pygame.image.load('assets\\pacman\\cherry.png'),(25,25))
        self.cherry = pygame.sprite.GroupSingle(None)
        self.cherry_timer = randint(500, 700)
        self.cherry_kill_timer=0
        self.cherry_amount=0

        self.score=0
        self.lives=3
        self.buff_time=8000
        self.check_game=True
        self.check_move=False
        self.rush_mode = False
        self.rush_points=100
        self.temp=0

        self.check_time=False
        self.time_start=0
        self.time_end=0
        self.sum_time=0

        self.munch_sound=pygame.mixer.Sound('sounds\\credit.wav')
        self.extra_life=pygame.mixer.Sound('sounds\\pacman_extrapac.wav')
        self.death_sound=pygame.mixer.Sound('sounds\\pacman_death.wav')
        self.spacial_sound=pygame.mixer.Sound('sounds\\pacman_eatfruit.wav')
        self.eat_alien_sound=pygame.mixer.Sound('sounds\\pacman_eatghost.wav')
        self.siren1_sound=pygame.mixer.Sound('sounds\\siren_1.wav')
        self.siren2_sound = pygame.mixer.Sound('sounds\\siren_3.wav')
        self.retreat_sound=pygame.mixer.Sound('sounds\\power_pellet.wav')
        self.victory_sound=pygame.mixer.Sound('sounds\\intermission.wav')

    def create_map(self,x_start,y_start):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col=='x':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = pacman.map.Map(self.block_size, (0, 0, 210), x, y,offset)
                    self.walls.add(block)
                if col=='y' or col=='c' or col=='q':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = pacman.map.Points(self.point_size, (255, 255, 255), x, y,offset)
                    self.points.add(block)
                if col=='z':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = pacman.map.Map(self.block_size, (255, 0, 0), x, y,offset)
                    self.spacial.add(block)
                if col=='y' or col=='b':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    self.road_list.append([x,y+offset])
                if col=='c' or col=='q' or col=='p' or col=='s':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    self.corner_list.append([x,y+offset])
                if col=='q':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    self.alien_time_out_list.append([x,y+offset])
                if col=='i':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = pacman.map.SpacialWall(self.block_size, (255, 255, 255), x, y,offset)
                    self.spacial_wall.add(block)
                if col=='p':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    self.player_start_pos=[x,y+offset]
                if col=='a':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    self.alien_birth_pos.append([x,y+offset])

    def flasing_special(self):
        sec=int(pygame.time.get_ticks()/100)
        if sec%2==0:
            for special in self.spacial:
                special.flash_black()
        else:
            for special in self.spacial:
                special.flash_white()

    def collect_points(self):
        if self.points:
            if pygame.sprite.spritecollide(self.player_sprite, self.points, True):
                self.score+=10
                self.temp+=1
                if self.temp%int(ticks/20)==0:
                    self.munch_sound.play()
                if len(self.points) == self.rush_points:
                    self.rush_mode=True
                    self.play_siren()

    def alien_create(self):
        for i in range(self.alien_amount):
            self.aliens.add(Alien(self.alien_size,self.aliens_colors[i],self.alien_birth_pos,self.alien_time_out_list,block_size))

    def buff(self):
        if self.spacial:
            if pygame.sprite.spritecollide(self.player_sprite, self.spacial, True):
                self.retreat_sound.stop()
                self.retreat_sound.play(-1)
                self.score+=200
                self.spacial_sound.play()
                for alien in self.aliens:
                    if not alien.get_dead_state():
                        alien.turn_ghost()
                pygame.time.set_timer(buff_mod,self.buff_time,1)

    def normal(self):
        self.retreat_sound.stop()
        for alien in self.aliens:
            if alien.get_ghost_state():
                alien.turn_alien()

    def buff_active(self):
        for alien in self.aliens:
            if alien.get_ghost_state() and alien.get_pos() not in self.corner_list:
                if pygame.sprite.spritecollide(alien,self.player,False):
                    alien.turn_dead()
                    self.eat_alien_sound.play()

    def display_score(self):
        victory_massage = self.font.render('score:'+str(self.score), False, (250, 250, 250))
        victory_rect = victory_massage.get_rect(topleft=(width-100,0))
        screen.blit(victory_massage, victory_rect)

    def display_lives(self):
        lifes_txt = self.font.render('lives:', False, (250, 250, 250))
        lifes_rect = lifes_txt.get_rect(topleft=(10, 0))
        screen.blit(lifes_txt, lifes_rect)
        for life in range(self.lives-1):
            x=60+(life*(self.live_surface.get_size()[0]+10))
            screen.blit(self.live_surface,(x,4))

    def death(self):
        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.player, False) and self.check_move and alien.get_alien_state():
                    pygame.mixer.stop()
                    self.lives-=1
                    if self.lives>0:self.death_sound.play()
                    self.player_sprite = Player((self.player_start_x, self.player_start_y),self.player_size,block_size)
                    self.player = pygame.sprite.GroupSingle(self.player_sprite)
                    self.check_move=False
                    self.sum_time+=int((self.time_end-self.time_start)/1000)

    def victory(self):
        if not self.points:
            screen.blit(self.end_image, self.end_rect)
            txt = self.end_font.render('you win', False, (255, 255, 255))
            txt_rect = txt.get_rect(center=(width/2+10, 100))
            screen.blit(txt, txt_rect)
            self.end_game()

    def game_over(self):
        if self.lives==0:
            screen.blit(self.end_image, self.end_rect)
            txt = self.end_font.render('game over', False, (255, 255, 255))
            txt_rect = txt.get_rect(center=(width/2+10, 100))
            screen.blit(txt, txt_rect)
            self.end_game()

    def end_game(self):
        if self.check_game:
            pygame.mixer.stop()
            if not self.points:
                self.victory_sound.play(0)
            if self.lives==0:
                self.death_sound.play()

        score_txt = self.font.render('score:  ' + str(self.score), False, (255, 255, 255))
        score_rect = score_txt.get_rect(center=(width / 2, height / 2))
        screen.blit(score_txt, score_rect)

        highscore_txt = self.font.render('high score:  ' + str(self.high_score), False, (255, 255, 255))
        highscore_rect = highscore_txt.get_rect(center=(width / 2, height / 2 + offset))
        screen.blit(highscore_txt, highscore_rect)

        time_massage = self.font.render('time:  ' + str(int((self.time_end - self.time_start) / 1000)+self.sum_time)+'  seconds', False, (255, 255, 255))
        time_rect = time_massage.get_rect(center=(width/2, height/2+60))
        screen.blit(time_massage, time_rect)

        restart_massage = self.font.render('PRESS R TO RESTART', False,(255, 255, 255))
        restart_rect = time_massage.get_rect(topleft=(width /2-restart_massage.get_width()/2, height / 2 + 150))
        screen.blit(restart_massage, restart_rect)

        self.check_game = False
        self.check_high_score()

    def check_if_move(self):
        if self.player_sprite.get_pos() in self.corner_list and self.player_sprite.get_pos()!=self.player_start_pos:
            if not self.check_move:
                pygame.event.post(pygame.event.Event(siren_play))
                background_music.stop()
                self.time_start = pygame.time.get_ticks()
            self.check_move=True

    def cherry_display(self):
        if self.check_move:
            self.cherry_timer -= 1
            if self.cherry_timer <= 0:
                self.cherry_kill_timer = 300
                self.cherry.add(Cherry(choice(self.corner_list)))
                self.cherry_timer = randint(500, 700)

    def cherry_counter(self):
        for cherry in range(self.cherry_amount):
            x=150+(cherry*(self.cherry_surface.get_size()[0]+10))
            screen .blit(self.cherry_surface,(x,3))

    def cherry_kill(self):
        self.cherry_kill_timer-=1
        if self.cherry_kill_timer<=0 and self.cherry:
            self.cherry.sprite.kill()

    def cherry_collect(self):
        if self.cherry:
            if pygame.sprite.spritecollide(self.player_sprite, self.cherry, True):
                self.score+=700
                self.cherry_amount+=1
                self.spacial_sound.play()
                if self.cherry_amount>=3:
                    self.cherry_amount=0
                    if self.lives<=3:
                        self.extra_life.play()
                        self.lives+=1

    def check_high_score(self):
        if int(self.score) > int(self.high_score):
            t = open("pacman highscore.txt", "w")
            t.write(str(self.score))
            t.close()
            self.high_score=self.score

    def display_time(self):
        if self.check_move:
            self.time_end=pygame.time.get_ticks()
            time_massage = self.font.render('time:' + str(int((self.time_end-self.time_start)/1000)+self.sum_time)+ '   sec', False, (255, 255, 255))
        else:time_massage = self.font.render('time:' + str(int(self.sum_time)) + '   sec', False,(255, 255, 255))
        time_rect = time_massage.get_rect(topleft=(width - 220, 0))
        screen.blit(time_massage, time_rect)

    def play_siren(self):
        self.siren1_sound.stop()
        self.siren2_sound.stop()
        if 0<len(self.points)<=self.rush_points:
            self.siren2_sound.play(-1)
        else:
            self.siren1_sound.play(-1)

    def run(self):
        self.walls.draw(screen)
        self.spacial_wall.draw(screen)
        self.points.draw(screen)
        self.spacial.draw(screen)
        self.player.draw(screen)
        self.aliens.draw(screen)
        self.cherry.draw(screen)
        self.collect_points()
        self.buff()
        self.display_score()
        self.display_lives()
        self.death()
        self.buff_active()
        self.check_if_move()
        self.cherry_kill()
        self.cherry_collect()
        self.cherry_counter()
        self.cherry_display()
        self.flasing_special()
        if not self.check_move:
            screen.blit(self.ready_surface, (width / 2 - self.ready_surface.get_width() / 2, height / 2 + 35))
        if self.check_game:
            if self.check_time:
                self.display_time()
            self.player_sprite.get_input(self.walls,width,self.corner_list,self.spacial_wall,self.road_list)
            for alien in self.aliens:
                alien.haunt(self.player_sprite.get_pos(),[alien.rect.x,alien.rect.y],self.corner_list,self.walls,self.road_list,width,self.check_move,self.rush_mode)
            if self.check_move:
                self.check_time = True
        self.victory()
        self.game_over()


def main():
    clock = pygame.time.Clock()
    game = Game()
    run=True

    while run:
        clock.tick(ticks)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==buff_mod:
                game.normal()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.stop()
                    background_music.play(-1)
                    run=False

            if event.type==siren_play:
                game.play_siren()

        screen.fill((30,30,30))
        game.run()
        pygame.display.flip()

    main()


if __name__ == '__main__':
    main()
