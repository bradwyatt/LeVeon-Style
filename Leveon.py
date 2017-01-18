"""
Created as a GIF meme mocking NBC's Frogger depiction of Le'Veon Bell
Game was originally Chiefs versus Steelers on Jan 15th, 2017
"""
import pygame, random, sys
from pygame.locals import *
from genmenu import *
running = True #Flags game as on
menuOn = 1
firstMessage = 1
Rooms = []
(screenWidth, screenHeight) = 728, 900
SCORE = 0
player = None
screen = None
keys = [False, False, False, False]
images = {}
sounds = {}
(x1, y1) = (0, 0)
allsprites = pygame.sprite.Group()
clock = pygame.time.Clock()

def adjust_to_correct_appdir():
    try:
        appdir = sys.argv[0] #feel free to use __file__
        if not appdir:
            raise ValueError
        appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
        os.chdir(appdir)
        if not appdir in sys.path:
            sys.path.insert(0,appdir)
    except:
        #placeholder for feedback, adjust to your app.
        #remember to use only python and python standard libraries
        #not any resource or module into the appdir 
        #a window in Tkinter can be adequate for apps without console
        #a simple print with a timeout can be enough for console apps
        print 'Please run from an OS console.'
        import time
        time.sleep(10)
        sys.exit(1)
adjust_to_correct_appdir()

def load_sound(file, name):
    sound = pygame.mixer.Sound(file)
    sounds[name] = sound
    
def load_image(file, name, transparent, alpha):
    new_image = pygame.image.load(file)
    if alpha == True:
        new_image = new_image.convert_alpha()
    else:
        new_image = new_image.convert()
    if transparent:
        colorkey = new_image.get_at((0,0))
        new_image.set_colorkey(colorkey, RLEACCEL)
    images[name] = new_image
    
def displayCaption():
    pygame.display.set_caption("Le'Veon Style")

def quit():
    print 'Thanks for playing'
    sys.exit()

def startplaceholder(screen):
    global menuOn, keys
    Rooms = []
    Rooms.append(Room())
    SCORE = 0
    menuOn = 0
    keys = [False, False, False, False]
    pass

class Menu(object):
    def __init__(self,screen):
        self.screen = screen
        self.title = startMenu
        self.menu = genmenu(['START', lambda: startplaceholder(screen)])
        self.menu.position(900,190)
        self.menu.defaultColor((0,0,0))
        self.menu.choiceColor((0,0,0))
        self.clock = pygame.time.Clock()
        event = pygame.event.get()
        self.menu.create(self.screen)
        self.menu.choose(event)
        self.main_loop()

    def main_loop(self):
        global menuOn
        while menuOn == 1:
            self.clock.tick(60)
            events = pygame.event.get()
            self.menu.choose(events)
            self.screen.blit(self.title, (0, 0))
            self.menu.create(self.screen)
            pygame.display.flip()
            for event in events:
                if event.type == QUIT:
                    sys.exit()

class GameOver(object):
    def __init__(self,screen):
        self.screen = screen
        self.title = gameOver
        self.clock = pygame.time.Clock()
        event = pygame.event.get()
        self.main_loop()

    def main_loop(self):
        global menuOn
        while menuOn == 2:
            self.clock.tick(60)
            events = pygame.event.get()
            self.screen.blit(self.title, (0, 0))
            scoreGameOverText = arialFont.render("Score: "+str(SCORE), 1, (0,0,0))
            self.screen.blit(scoreGameOverText, (50, 175))
            pygame.display.flip()
            for event in events:
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        reset()
                        menuOn = 1
                        
class Winner(object):
    def __init__(self,screen):
        self.screen = screen
        self.title = winner
        self.clock = pygame.time.Clock()
        event = pygame.event.get()
        self.main_loop()

    def main_loop(self):
        global menuOn
        while menuOn == 3:
            self.clock.tick(60)
            events = pygame.event.get()
            self.screen.blit(self.title, (0, 0))
            pygame.display.flip()
            for event in events:
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        reset()
                        menuOn = 1

def mainmenuplaceholder(screen):
    global menuOn
    menuOn = 1
    pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["spr_enemy"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.tier = 0
    def update(self):
        self.difficultyMovement()
        newpos = (self.rect.topleft[0]+self.direction[0],self.rect.topleft[1])
        self.rect.topleft = newpos
        if(self.rect.topleft[0] < -100 and self.tier == 3):
            self.rect.topleft = (screenWidth, self.rect.topleft[1])
        if(self.rect.topleft[0] > screenWidth and (self.tier == 1 or self.tier == 2)):
            self.rect.topleft = (-68, self.rect.topleft[1])
    def difficultyMovement(self):
        # Tier 1 moves right, Tier 2 moves right, Tier 3 (bottom) moves left
        if(self.tier == 1):
            self.direction = (2,0)
        elif(self.tier == 2):
            self.direction = (1,0)
        elif(self.tier == 3):
            self.direction = (-1,0)
            
class Steelers(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["spr_steelers"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.tier = 0
    def update(self):
        self.difficultyMovement()
        newpos = (self.rect.topleft[0]+self.direction[0],self.rect.topleft[1])
        self.rect.topleft = newpos
        if(self.rect.topright[0] < 0 and self.tier == 2):
            self.rect.topleft = (screenWidth, self.rect.topleft[1])
        if(self.rect.topleft[0] > screenWidth and self.tier == 1):
            self.rect.topleft = (-100, self.rect.topleft[1])
    def difficultyMovement(self):
        if(self.tier == 1):
            self.direction = (1,0)
        elif(self.tier == 2):
            self.direction = (-1,0)
            
class Goal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["spr_goal"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
    def update(self):
        if(SCORE == 0):
            self.image = images["spr_goal"]
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["spr_player"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.playerWidth, self.playerHeight = (65, 80)
        self.speedX, self.speedY = 50, 40
        self.pos = [screenWidth/2, screenHeight/2]
        self.timeLeft = 31
    def update(self):
        self.image = pygame.transform.smoothscale(self.image, (self.playerWidth, self.playerHeight))
        self.rect = self.image.get_rect()
        newpos = (self.pos[0], self.pos[1])
        self.rect.topleft = newpos
        self.speedX, self.speedY = 40, 50
        self.timeLeft -= .028
class Room():
    def __init__(self):
        reset()

def reset():
    global SCORE
    SCORE = 0
    player.pos = [screenWidth/2-30, screenHeight-145]
    player.rect.topleft = (player.pos[0], player.pos[1])
    keys = [False, False, False, False]
    enemies[0].rect.topleft = (0, 120)
    enemies[1].rect.topleft = (300, 120)
    enemies[2].rect.topleft = (600, 120)
    enemies[0].tier, enemies[1].tier, enemies[2].tier = 1, 1, 1
    enemies[3].rect.topleft = (0, 300)
    enemies[4].rect.topleft = (200, 300)
    enemies[5].rect.topleft = (400, 300)
    enemies[6].rect.topleft = (600, 300)
    enemies[3].tier, enemies[4].tier, enemies[5].tier, enemies[6].tier = 2, 2, 2, 2
    enemies[7].rect.topleft = (0, 520)
    enemies[8].rect.topleft = (200, 520)
    enemies[9].rect.topleft = (400, 520)
    enemies[10].rect.topleft = (600, 520)
    enemies[7].tier, enemies[8].tier, enemies[9].tier, enemies[10].tier = 3, 3, 3, 3
    steelers[0].rect.topleft = (350, 675) #Quarterback
    steelers[0].tier = 2
    steelers[1].rect.topleft = (50, 600)
    steelers[2].rect.topleft = (200, 600)
    steelers[3].rect.topleft = (350, 600)
    steelers[4].rect.topleft = (500, 600)
    steelers[5].rect.topleft = (650, 600)
    steelers[1].tier, steelers[2].tier, steelers[3].tier, steelers[4].tier, steelers[5].tier = 1, 1, 1, 1, 1
    goals[0].rect.topleft = (25, 10)
    goals[1].rect.topleft = (175, 10)
    goals[2].rect.topleft = (325, 10)
    goals[3].rect.topleft = (475, 10)
    goals[4].rect.topleft = (625, 10)
    player.timeLeft = 31
    
#Init
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Le'Veon Style")
spr_goal = load_image("sprites/goal.png", "spr_goal", True, True)
spr_touchdown = load_image("sprites/touchdown.png", "spr_touchdown", True, True)
goals = [ Goal() for i in range(5)]
#other sprites
spr_enemy = load_image("sprites/patriots.png", "spr_enemy", False, True)
enemies = [ Enemy() for i in range(11)]
spr_steelers = load_image("sprites/steelers.png", "spr_steelers", True, True)
steelers = [ Steelers() for i in range(6)]
spr_player = load_image("sprites/leveonbell.png", "spr_player", True, True)
player = Player()
#font and texts
arcadeFont = pygame.font.Font("fonts/ARCADE.ttf", 16)
arcadeFontMain = pygame.font.Font("fonts/ARCADE.ttf", 48)
arcadeFontGameOver = pygame.font.Font("fonts/ARCADE.ttf", 76)
arialFont = pygame.font.SysFont('Arial', 32)
#backgrounds
startMenu = pygame.image.load("sprites/startmenu.png").convert()
startMenu = pygame.transform.scale(startMenu, (screenWidth, screenHeight))
gameOver = pygame.image.load("sprites/gameover.png").convert()
gameOver = pygame.transform.scale(gameOver, (screenWidth, screenHeight))
winner = pygame.image.load("sprites/winner.png").convert()
winner = pygame.transform.scale(winner, (screenWidth, screenHeight))
bgwater = pygame.image.load("sprites/footballfield.jpg").convert()
bgwater = pygame.transform.scale(bgwater, (screenWidth, screenHeight))
#window
gameicon = pygame.image.load("sprites/bellico.png")
pygame.display.set_icon(gameicon)
pygame.display.set_caption('Le\'Veon Style')
pygame.mouse.set_visible(0)
#sounds
snd_leap = load_sound("sounds/snd_leap.wav", "snd_leap")
sounds["snd_leap"].set_volume(.5)
snd_playerdie = load_sound("sounds/playerdie.wav", "snd_playerdie")
sounds["snd_playerdie"].set_volume(.3)
#music loop
pygame.mixer.music.load("sounds/froggertheme.mp3")
pygame.mixer.music.set_volume(.2)
pygame.mixer.music.play(-1)
#Main
while running:
    if(firstMessage == 1):
        print "Please ignore the errors."
        firstMessage = 0
    clock.tick(35)
    displayCaption()
    if menuOn == 1: #Menu Screen
        Menu(screen)
        SCORE = 0
    elif menuOn == 2: #Gameover Screen
        sounds["snd_playerdie"].play()
        GameOver(screen)
    elif menuOn == 3:
        Winner(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                for i in range(0, len(sounds)):
                    soundslist = sounds.keys() #returns list of keys in sounds
                    sounds[soundslist[i]].stop() #stops all sounds when go to menu
                menuOn = 1
            elif event.key==K_UP:
                keys[0]=True
            elif event.key==K_LEFT:
                keys[1]=True
            elif event.key==K_DOWN:
                keys[2]=True
            elif event.key==K_RIGHT:
                keys[3]=True
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_UP:
                keys[0]=False
            elif event.key==pygame.K_LEFT:
                keys[1]=False
            elif event.key==pygame.K_DOWN:
                keys[2]=False
            elif event.key==pygame.K_RIGHT:
                keys[3]=False
    if keys[0]:#up
        sounds["snd_leap"].play()
        if player.pos[1] > 50: #boundary, 32 is block, added a few extra pixels to make it look nicer
            player.pos[1] -= player.speedY
        keys[0]=False
    if keys[2]:#down
        sounds["snd_leap"].play()
        if player.pos[1] < screenHeight-95: 
            player.pos[1] += player.speedY
        keys[2]=False
    if keys[1]:#left
        sounds["snd_leap"].play()
        if player.pos[0] > 32:
            player.pos[0] -= player.speedX
        keys[1]=False
    if keys[3]:#right
        sounds["snd_leap"].play()
        if player.pos[0] < screenWidth-75:
            player.pos[0] += player.speedX
        keys[3] = False
    allsprites.update()
    #water background movement
    screen.blit(bgwater, (x1,y1))
    allsprites.draw(screen)
    #Menu Design
    for enemy in enemies:
        if pygame.sprite.collide_mask(enemy, player):
            menuOn = 2
    for goal in goals:
        if pygame.sprite.collide_mask(goal, player):
            goal.image = images["spr_touchdown"]
            player.pos = [screenWidth/2-30, screenHeight-145]
            SCORE += 1
    if player.timeLeft < 1:
        menuOn = 2
    if SCORE == 5:
        menuOn = 3
    #Test Print Code: FOR DEBUGGING PURPOSES BELOW:
    timerText = arcadeFontMain.render("TIME:", 1, (0,0,0))
    screen.blit(timerText, (screenWidth/2+170, screenHeight-45))
    timerCountdownText = arcadeFontMain.render(str(int(player.timeLeft)), 1, (0,0,0))
    screen.blit(timerCountdownText, (screenWidth-70, screenHeight-45))
    #Top Screen Design
    pygame.display.flip()
    pygame.display.update()