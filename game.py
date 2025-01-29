import pygame
from pygame.locals import *
import sys
import random
 
pygame.init()
vec = pygame.math.Vector2 
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.1
FPS = 60

score = 0
isDead = False

restartMenu = [[], []]

 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

pygame.font.init()
my_font = pygame.font.SysFont("Comic Sans MS", 30)

bg = pygame.image.load("backGround1.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.image.load("pogoman.png")
        self.surf = pygame.transform.scale(self.surf, (22, 50))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.isJumping = False
        self.isFallingVal = False

    def isFalling(self):
        if self.vel.y > 1:
            isFallingVal = True
            print("Is falling True")
        elif self.vel.y < -1:
            isFallingVal = False
            print("Is falling False")

    def move(self):
        self.acc = vec(0,0.15)
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH         
        self.rect.midbottom = self.pos

    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.isJumping:
           self.isJumping = True
           self.vel.y = -12
 
    def cancelJump(self):
        if self.isJumping:
            if self.vel.y < -3:
                self.vel.y = -5

    def update(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                lowest = min(hits, key=lambda platform: platform.rect.top)
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.isJumping = False
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        kumpi = random.randint(1, 2)
        if kumpi == 1:
            self.surf = pygame.image.load("platformThin.png").convert_alpha()
        else:
            self.surf = pygame.image.load("platformWide.png").convert_alpha()

        self.rect = self.surf.get_rect(topleft = (random.randint(0,WIDTH-10),random.randint(0, HEIGHT-30)))

    def move(self):
        pass
 
 
def plat_gen():
    count = 0
    while len(platforms) < 7:
        x = random.randint(0, WIDTH)
        y = random.randint(-50, 0)
        temp_platform = platform()
        temp_platform.rect.center = (x, y)

        if any(temp_platform.rect.colliderect(existing.rect) for existing in platforms):
            continue
        else:
            platforms.add(temp_platform)
            all_sprites.add(temp_platform)

def plat_gen_restart():
    for i in platforms:
        i.kill()
    PT1 = platform()

    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((255,0,0))
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

    platforms.add(PT1)
    all_sprites.add(PT1)
    while len(platforms) < 7:
        width = random.randrange(50,100)
        p  = platform()             
        p.rect.center = (random.randrange(0, WIDTH - width),random.randrange(-50, 400))
        platforms.add(p)
        all_sprites.add(p)

def death():
    plat_gen_restart()
    

PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
all_sprites = pygame.sprite.Group()

 
platforms = pygame.sprite.Group()
platforms.add(PT1)

respawnMainText = my_font.render(f"Press any button to restart!", False, (0,0,0))
 
for x in range(random.randint(5, 6)):
    pl = platform()
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
            if isDead == True:
                P1 = Player()
                all_sprites.add(P1)
                isDead = False
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancelJump()

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        score += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    
    if P1.rect.bottom > HEIGHT + 40 and isDead == False:      
        isDead = True
        restartMenu[0] = [scoreText, (WIDTH/2 - scoreText.get_width()/2, 150)]
        restartMenu[1] = [respawnMainText, (WIDTH/2 - respawnMainText.get_width()/2, 250)]
        score = 0
        death()

    

    scoreText = my_font.render(f"score: {round(score / 100)} m", False, (0,0,0))


    displaysurface.blit(bg, (0, 0))

    if isDead == False:
        displaysurface.blit(scoreText, (0,0))
        P1.isFalling()
        P1.update()
        plat_gen()

    elif isDead == True:
        for kuva in restartMenu:
            displaysurface.blit(kuva[0], kuva[1])
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

 
    pygame.display.update()
    FramePerSec.tick(FPS)