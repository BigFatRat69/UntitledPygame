import pygame
from pygame.locals import *
import sys
import random
import json
 
pygame.init()
vec = pygame.math.Vector2 
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.1
FPS = 60

highScore = 0
score = 0
isDead = False
gameStart = False
userName = ""

restartMenu = [[], []]

 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

pygame.font.init()
my_font = pygame.font.SysFont("Comic Sans MS", 30)

bg = pygame.image.load("backGround1.png")

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_leaderboard(scores):
    with open("leaderboard.json", "w") as file:
        json.dump(scores, file, indent=4)

leaderboard = load_leaderboard()

def input_name():
    global userName, gameStart
    input_active = True
    input_text = ""

    while input_active:
        displaysurface.fill((255, 255, 255))
        prompt = my_font.render("Syötä nimesi: ", True, (0, 0, 0))
        name_display = my_font.render(input_text, True, (0, 0, 255))

        displaysurface.blit(prompt, (WIDTH//4, HEIGHT//3))
        displaysurface.blit(name_display, (WIDTH//4, HEIGHT//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and input_text.strip():
                    userName = input_text.strip()
                    gameStart = True
                    input_active = False
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.image.load("assets/pogoman.png")
        self.surf = pygame.transform.scale(self.surf, (22, 50))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.isJumping = False
        self.jump_cooldown = 0

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
        if self.jump_cooldown == 0:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits and not self.isJumping:
                self.isJumping = True
                self.vel.y = -12
                self.jump_cooldown = 15
 
    def cancelJump(self):
        if self.jump_cooldown > 0 and self.isJumping and self.vel.y < -3:
            self.vel.y = -5

    def update(self):
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if self.vel.y > 0 and hits:        
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
            self.surf = pygame.image.load("assets/platformThin.png").convert_alpha()
        else:
            self.surf = pygame.image.load("assets/platformWide.png").convert_alpha()

        self.rect = self.surf.get_rect(topleft = (random.randint(0,WIDTH-10),random.randint(0, HEIGHT-30)))

    def move(self):
        pass
 
 
def plat_gen():
    while len(platforms) < 7:
        x = random.randint(0, WIDTH)
        y = random.randint(-70, 0)
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
    global isDead, score, highScore
    isDead = True
    if score > highScore:
        highScore = score

    leaderboard.append({"name": userName, "score": round(score / 100)})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard[:] = leaderboard[:5]
    save_leaderboard(leaderboard)
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

input_name()
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if isDead:
                P1 = Player()
                all_sprites.add(P1)
                isDead = False
                score = 0
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                P1.cancelJump()

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        score += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    
    if P1.rect.bottom > HEIGHT + 40 and not isDead:      
        death()

    scoreText = my_font.render(f"Score: {round(score / 100)} m", False, (0,0,0))

    displaysurface.blit(bg, (0, 0))
    if not isDead:
        displaysurface.blit(scoreText, (10,10))
        P1.update()
        plat_gen()
    else:
        displaysurface.blit(my_font.render("Game Over!", True, (255, 0, 0)), (WIDTH // 4, HEIGHT // 4))
        displaysurface.blit(my_font.render("Press any key to restart", True, (0, 0, 0)), (WIDTH // 8, HEIGHT // 3))

        y_offset = HEIGHT // 2
        for idx, entry in enumerate(leaderboard):
            leaderboard_text = my_font.render(f"{idx+1}. {entry['name']} - {entry['score']} m", True, (0, 0, 0))
            displaysurface.blit(leaderboard_text, (WIDTH // 6, y_offset + idx * 30))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

 
    pygame.display.update()
    FramePerSec.tick(FPS)