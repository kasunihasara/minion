import pygame
from tkinter import *
from tkinter import messagebox
pygame.init()

win = pygame.display.set_mode((1100,680))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'),pygame.image.load('R6.png'),pygame.image.load('R7.png'),pygame.image.load('R8.png'),pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),pygame.image.load('L7.png'),pygame.image.load('L8.png'),pygame.image.load('L9.png')]
bg = pygame.image.load('background.jpg')


speaker=pygame.image.load('speaker-filled-audio-tool.png')
speaker = pygame.transform.scale(speaker, (32, 32))
mute=pygame.image.load('mute.png')
mute = pygame.transform.scale(mute, (32, 32))

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("Game_bullet.mp3")
hitSound = pygame.mixer.Sound("Game_hit.mp3")
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

score = 0
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.isJump = False
        self.left = False
        self.right = True
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x - 5, self.y + 11, 80, 150)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)



    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 5 
        self.y = 410
        self.walkCount = 0
        man.right = True
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()



        
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

    


class enemy(object):
    walkRight = [pygame.image.load('ER1.png'), pygame.image.load('ER2.png'), pygame.image.load('ER3.png'), pygame.image.load('ER4.png'), pygame.image.load('ER5.png'), pygame.image.load('ER6.png'), pygame.image.load('ER7.png'), pygame.image.load('ER8.png'), pygame.image.load('ER9.png')]
    walkLeft = [pygame.image.load('EL1.png'), pygame.image.load('EL2.png'), pygame.image.load('EL3.png'), pygame.image.load('EL4.png'), pygame.image.load('EL5.png'), pygame.image.load('EL6.png'), pygame.image.load('EL7.png'), pygame.image.load('EL8.png'), pygame.image.load('EL9.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end=end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 6
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
        
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//4], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//4], (self.x,self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 70, 10)) 
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1]-20, 70 - (5 * (10 - self.health)), 10))

        self.hitbox = (self.x + 17, self.y + 2, 100, 130)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
       
            
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
    def hit(self):
        if self.health > -3:
            self.health -= 1
        else:
            self.visible = False
            pygame.mixer.music.stop()
            Tk().wm_withdraw() 
            messagebox.showinfo('Game Over','quite')
            pygame.quit()
        print('hit')


def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    win.blit(speaker, (15,10))
    win.blit(mute, (15,80))
    goblin.draw(win)
    text = font.render("Score: " + str(score), 1, (0,0,0)) 
    win.blit(text, (500, 10))
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()


#mainloop
font = pygame.font.SysFont("comicsans", 30, True)
man = player(500, 410, -490,64)
goblin = enemy(64,450, 64, 64, 910)
shootLoop = 0
bullets = []
run = True
while run:
    
    clock.tick(27)
    if goblin.visible == True:
        
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 1100 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //100+23), round(man.y + man.height//100+100), 6, (0,0,0), facing))
        shootLoop = 1



    if event.type == pygame.MOUSEBUTTONDOWN:
        x,y=pygame.mouse.get_pos()
       
        if y>=89 and y<=139:
            pygame.mixer.music.stop()
        elif y>=20 and y<=60:
            pygame.mixer.music.play(-1) 

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if man.right==True:
            
           if keys[pygame.K_UP]:
               man.isJump = True
               man.right = True
               man.left = False
               man.walkCount = 0

        elif man.left==True:
            
           if keys[pygame.K_UP]:
               man.isJump = True
               man.right = False
               man.left = True
               man.walkCount = 0
            
    
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()
