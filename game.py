import pygame
from pygame.locals import *
import sys
import random
 
pygame.init()
vec = pygame.math.Vector2 
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
 
    def move(self):
        self.acc = vec(0,0.5)
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH         
        self.rect.midbottom = self.pos
 
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
           self.vel.y = -15
 
    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, width=None, x=None, y=None):
        super().__init__()
        self.width = width if width else random.randint(50, 100)
        self.surf = pygame.Surface((self.width, 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(x if x else random.randint(0, WIDTH - self.width), 
                                               y if y else random.randint(0, HEIGHT - 30)))

    def move(self):
        pass

#TODO fix platforms spawning on screen instead of outside the screen
def plat_gen():
    while len(platforms) < 7:
        width = random.randint(50, 100)
        x = random.randint(0, WIDTH - width)
        y = random.randint(-50, 0)
        
        temp_platform = Platform(width, x, y)
        
        if any(temp_platform.rect.colliderect(existing.rect) for existing in platforms):
            continue 
        else:
            platforms.add(temp_platform)
            all_sprites.add(temp_platform)

        
 
PT1 = Platform()
P1 = Player()
 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
all_sprites = pygame.sprite.Group()

 
platforms = pygame.sprite.Group()
platforms.add(PT1)
 
for x in range(random.randint(5, 6)):
    pl = Platform()
    platforms.add(pl)
    all_sprites.add(pl)
all_sprites.add(P1)
all_sprites.add(PT1)
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
 
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
         
    displaysurface.fill((0,0,0))
    P1.update()
    plat_gen()
 

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
 
    pygame.display.update()
    FramePerSec.tick(FPS)