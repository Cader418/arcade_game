import pygame
import os
import math
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 500
YELLOW_WIDTH, YELLOW_HEIGHT = 55, 55
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#BOARDER = pygame.Rect(700, 0, 10, HEIGHT)
BUL_RAD = (0,0)
pygame.display.set_caption("Game")

FONT = pygame.font.SysFont('comicsans', 100)
FONT2 = pygame.font.SysFont('comicsans', 80)

WHITE = (255, 255, 255)
green = (152, 228, 120)
blue = (47, 72, 88)
BLACK = (0,0,0)
YELLOW = (255,255,98)
FPS = 60
VEL = 5
BUL_VEL = 30
BAD_WIDTH, BAD_HEIGHT = 15, 15
YELLOW_GUY1 = pygame.image.load(os.path.join("circ.png"))
YELLOW_GUY = pygame.transform.scale(YELLOW_GUY1, (YELLOW_WIDTH, YELLOW_HEIGHT))

class bad():
    def __init__(self, x, y):
        self.bod = pygame.Rect(x,y,BAD_WIDTH, BAD_HEIGHT)
        self.color = blue
        self.attack_pos = ""

def draw_end(score, highScore):
    text = "SCORE: " + str(score)
    text2 = "HIGH SCORE: " + str(highScore)
    draw_text = FONT.render(text, 1, WHITE)
    draw_text_2 = FONT2.render(text2, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    WIN.blit(draw_text_2, (WIDTH/2 - draw_text_2.get_width()/2, HEIGHT/2 - 200))
    pygame.display.update()
    pygame.time.delay(3000)


def draw_window(yelPos, bullets, bads):
    WIN.fill(green)
    for i in bullets:
        pygame.draw.ellipse(WIN, YELLOW, i[0], 0)
    WIN.blit(YELLOW_GUY, (yelPos.x, yelPos.y))
    for i in bads:
        pygame.draw.rect(WIN,i.color, i.bod)
    pygame.display.update()

def yellow_movement(keys_pressed, yelPos):
    if keys_pressed[pygame.K_a] and not yelPos.x == 0:  # Left
        yelPos.x -= VEL
    if keys_pressed[pygame.K_d] and not yelPos.x ==  900 - YELLOW_HEIGHT:  # Right
        yelPos.x += VEL
    if keys_pressed[pygame.K_w] and not yelPos.y == 0:  # Up
        yelPos.y -= VEL
    if keys_pressed[pygame.K_s] and not yelPos.y == HEIGHT - YELLOW_HEIGHT:  # Down
        yelPos.y += VEL

def bullet_movement(bullets, bads, hit_count):
    for i in bullets:
        tempx, tempy = i[0].x, i[0].y
        i[0].x += BUL_VEL*i[1]
        i[0].y += BUL_VEL*i[2]
        if i[0].x <= 0 or i[0].x >= WIDTH or i[0].y <= 0 or i[0].y >= HEIGHT:
            bullets.remove(i)
        for j in bads:
            if j.bod.colliderect(i[0]):
                bads.remove(j)
                hit_count = hit_count+1;
    return hit_count

def bad_movement(bads, yelPos):
    runInd = True;
    for i in bads:
        if i.attack_pos == "from_left":
            i.bod.x += VEL
        elif i.attack_pos == "from_top":
            i.bod.y += VEL
        elif i.attack_pos == "from_right":
            i.bod.x -= VEL
        elif i.attack_pos == "from_bottom":
            i.bod.y -= VEL
        if i.bod.x <= 0 or i.bod.x >= WIDTH or i.bod.y <= 0 or i.bod.y >= HEIGHT:
            bads.remove(i)
        if yelPos.colliderect(i.bod):
            runInd = False
    return runInd

def main():
    tempx, tempy = BUL_VEL, BUL_VEL
    yelPos = pygame.Rect(450,250,YELLOW_WIDTH, YELLOW_HEIGHT)
    bullets = []
    bads = []
    bindex = 0
    clock = pygame.time.Clock()
    clock_count = 0;
    hit_count = 1;
    score = 0;
    run = True
    while run:
        clock.tick(FPS)
        clock_count = clock_count+1;
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bul = pygame.Rect(yelPos.x+YELLOW_HEIGHT//2-8, yelPos.y+YELLOW_HEIGHT//2-8, 30, 30)
                tempx, tempy = pygame.mouse.get_pos()
                angle = math.atan2(tempy-bul.y, tempx-bul.x)
                dx = math.cos(angle)
                dy = math.sin(angle)
                bullets.append([bul, dx, dy])
        b = "b" + str(bindex)
        bindex += 1
        b_attack_pos = random.randrange(0,50,1)
        if b_attack_pos == 0:
            b = bad(0, random.randrange(0,HEIGHT,1))
            b.attack_pos = "from_left"
            bads.append(b)
        elif b_attack_pos == 1:
            b = bad(random.randrange(0, WIDTH, 1), 0)
            b.attack_pos = "from_top"
            bads.append(b)
        elif b_attack_pos == 2:
            b = bad(WIDTH, random.randrange(0, HEIGHT, 1))
            b.attack_pos = "from_right"
            bads.append(b)
        elif b_attack_pos == 3:
            b = bad(random.randrange(0, WIDTH, 1), HEIGHT)
            b.attack_pos = "from_bottom"
            bads.append(b)
        if run:
            run = bad_movement(bads, yelPos)
            hit_count = bullet_movement(bullets, bads, hit_count)
            keys_pressed = pygame.key.get_pressed()
            yellow_movement(keys_pressed, yelPos)
            draw_window(yelPos, bullets, bads)

    score = hit_count * clock_count;
    with open ("high_score.txt", 'r') as file:
        highScore = file.read()
        if score > int(highScore):
            highScore = score
        file.close()
    with open ("high_score.txt", 'w') as file:
        file.write(str(highScore))
        file.close()
    draw_end(score, highScore)
    pygame.quit()

if __name__ == "__main__":
    main()