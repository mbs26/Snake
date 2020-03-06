import pygame
import sys
import random
from pygame.locals import *

screen_x=14
screen_y=14

def load_image(dir,ALPHA):
    try:
        image=pygame.image.load(dir)
    except:
        print('No se ha podido cargar el fichero')
        sys.exit(1)
    if ALPHA:
        image=image.convert_alpha()
    else:
        image=image.convert()
    return image

coord=lambda x: (x[0]*20+1,x[1]*20+1)

class serpiente:
    def __init__(self,pos_i):
        self.cabeza=load_image('cabeza.png',0)
        self.cuerpo=load_image('cuerpo.png',0)
        #sprites de 39x39 pixeles
        self.pos=pos_i
        self.dir=1 #direccion: 0 izquierda, 1 derecha, 2 arriba, 3 abajo
        self.cola=[bloque((pos_i[0]-1,pos_i[1]),self.pos)]
    def paso(self):
        if self.dir==0:
            self.pos=(self.pos[0]-1,self.pos[1])
        elif self.dir==1:
            self.pos=(self.pos[0]+1,self.pos[1])
        elif self.dir==2:
            self.pos=(self.pos[0],self.pos[1]-1)
        elif self.dir==3:
            self.pos=(self.pos[0],self.pos[1]+1)
        buff=self.pos
        for bloque in self.cola:
            bloque.pos=bloque.anterior
            bloque.anterior=buff
            buff=bloque.pos
    def game_over(self):
        if self.pos[0]>screen_x or self.pos[1]>screen_y:
            return True
        if self.pos[0]<0 or self.pos[1]<0:
            return True
        for bloque in self.cola:
            if bloque.pos[0]>screen_x or bloque.pos[1]>screen_y or bloque.pos==self.pos:
                return True
        return False
    def comer(self,pos):
        if self.pos==pos:
            return 1
        else:
            return 0
    def nuevo_bloque(self):
        pos_ultimo=self.cola[-1].pos
        self.cola.append(bloque(pos_ultimo,pos_ultimo))

class bloque:
    def __init__(self,posicion_b,posicion_ant):
        self.pos=posicion_b
        self.anterior=posicion_ant

class fruta:
    def __init__(self,pos):
        self.cerezas=load_image('fruta.png',0)
        self.pos=pos
    def spawn(self,serpiente):
        ocupados=[serpiente.pos]+[bloque.pos for bloque in serpiente.cola]
        libres=[]
        for x in range(0,screen_x+1):
            for y in range(0,screen_y+1):
                if (x,y) not in ocupados:
                    libres.append((x,y))
        pos=random.choice(libres)
        self.pos=pos

def main():
    pygame.init()
    pygame.font.init()

    screen=pygame.display.set_mode((20*screen_x+20,20*screen_y+20))
    pygame.display.set_caption('Snake Game')
    pygame.display.set_icon(load_image('icon.png',1))

    snake=serpiente((4,2))
    cerezas=fruta((8,2))

    screen.fill((0,0,0))
    screen.blit(snake.cabeza,coord(snake.pos))
    for parte in snake.cola:
        screen.blit(snake.cuerpo,coord(parte.pos))
    pygame.display.flip()

    while True:
        event=pygame.event.poll()
        while event.type==pygame.KEYUP or (event.type==pygame.KEYDOWN and event.key not in [K_UP,K_DOWN,K_LEFT,K_RIGHT]):
            event=pygame.event.poll()
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:#direccion: 0 izquierda, 1 derecha, 2 arriba, 3 abajo
            if event.key==K_UP and snake.dir not in [2,3]:
                snake.dir=2
            elif event.key==K_DOWN and snake.dir not in [2,3]:
                snake.dir=3
            elif event.key==K_RIGHT and snake.dir not in [0,1]:
                snake.dir=1
            elif event.key==K_LEFT and snake.dir not in [0,1]:
                snake.dir=0

        snake.paso()
        if snake.comer(cerezas.pos):
            cerezas.spawn(snake)
            snake.nuevo_bloque()

        screen.fill((0,0,0))
        screen.blit(cerezas.cerezas,coord(cerezas.pos))
        screen.blit(snake.cabeza,coord(snake.pos))
        for parte in snake.cola:
            screen.blit(snake.cuerpo,coord(parte.pos))
        pygame.display.flip()

        if snake.game_over():
            myfont=pygame.font.SysFont('Comic Sans MS',30)
            screen.blit(myfont.render('Has muerto, Puntuacion: {0}'.format(len(snake.cola)) ,False,(0,255,0)),(10,0))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        sys.exit()
                pygame.time.delay(100)

        pygame.time.delay(150)

if __name__=='__main__':
    main()
