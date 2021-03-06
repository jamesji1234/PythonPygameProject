import pygame as pg
import random

WIDTH = 980 # Screen width
HEIGHT = 800 # Screen HeightWS
FPS = 60 # Fps to run   
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pg.init() # Start
pg.mixer.init() # Sound Start  
screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("My Game 6001855")
clock = pg.time.Clock()



class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT / 2
        self.rect.left = 10
        self.speedY = 0
    def update(self):
        self.speedY = 0
        keystate = pg.key.get_pressed()
        if  keystate[pg.K_UP]:
            self.speedY = -8
        if keystate[pg.K_DOWN ]:
            self.speedY = 8 
        self.rect.y += self.speedY    

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.rect.x = random.randrange(WIDTH + 40, WIDTH + 100)
        self.speedx = random.randrange(-8 , -1)
        self.speedy = random.randrange(-3 , 3)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = random.randrange(WIDTH + 40, WIDTH + 100)
            self.speedx = random.randrange(-8 , -1)
        if  self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy *= -1   


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((20,10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 10
    def update(self):
        self.rect.x += self.speedx
        #Destroy when passed screen
        if self.rect.left > WIDTH:
            self.kill

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
player = Player()
bullets = pg.sprite.Group()
all_sprites.add(player)
for i in range(10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

running = True

while running:
    clock.tick(FPS)
    #Input
    for event in pg.event.get():
        #Check Closing
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
    #Update
    all_sprites.update()

    hits = pg.sprite.groupcollide(mobs , bullets , True , True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pg.sprite.spritecollide(player,mobs,False)
    if hits:
        running = False
    #Drawing
    screen.fill(BLACK)
    all_sprites.draw(screen)
    #EndofDrawing
    pg.display.flip()

pg.quit()