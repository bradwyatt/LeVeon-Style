"""
Created as a GIF meme mocking NBC's Frogger depiction of Le'Veon Bell
Game was originally Chiefs versus Steelers on Jan 15th, 2017
"""
import os
import sys
import pygame
from genmenu import *

(SCREEN_WIDTH, SCREEN_HEIGHT) = 728, 900
IMAGES = {}
SOUNDS = {}
SPAWN_POSITION = (SCREEN_WIDTH/2-30, SCREEN_HEIGHT-145)
PLAY_SCREEN, START_SCREEN, GAMEOVER_SCREEN, WINNER_SCREEN = 0, 1, 2, 3
TIME_LEFT = 31

def adjust_to_correct_appdir():
    try:
        appdir = sys.argv[0] #feel free to use __file__
        if not appdir:
            raise ValueError
        appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
        os.chdir(appdir)
        if not appdir in sys.path:
            sys.path.insert(0, appdir)
    except:
        #placeholder for feedback, adjust to your app.
        #remember to use only python and python standard libraries
        #not any resource or module into the appdir 
        #a window in Tkinter can be adequate for apps without console
        #a simple print with a timeout can be enough for console apps
        print('Please run from an OS console.')
        import time
        time.sleep(10)
        sys.exit(1)
adjust_to_correct_appdir()

def load_sound(file, name):
    sound = pygame.mixer.Sound(file)
    SOUNDS[name] = sound

def load_image(file, name, transparent, alpha):
    new_image = pygame.image.load(file)
    if alpha:
        new_image = new_image.convert_alpha()
    else:
        new_image = new_image.convert()
    if transparent:
        colorkey = new_image.get_at((0, 0))
        new_image.set_colorkey(colorkey, RLEACCEL)
    IMAGES[name] = new_image

def display_caption():
    pygame.display.set_caption("Le'Veon Style")

def startplaceholder(screen):
    global MENU_SELECTION
    MENU_SELECTION = PLAY_SCREEN

class Menu():
    def __init__(self, screen, start_menu):
        self.screen = screen
        self.title = start_menu
        self.menu = genmenu(['START', lambda: startplaceholder(screen)])
        self.menu.position(900, 190)
        self.menu.defaultColor((0, 0, 0))
        self.menu.choiceColor((0, 0, 0))
        self.clock = pygame.time.Clock()
        event = pygame.event.get()
        self.menu.create(self.screen)
        self.menu.choose(event)
        self.main_loop()

    def main_loop(self):
        global MENU_SELECTION
        while MENU_SELECTION == START_SCREEN:
            self.clock.tick(60)
            events = pygame.event.get()
            self.menu.choose(events)
            self.screen.blit(self.title, (0, 0))
            self.menu.create(self.screen)
            pygame.display.flip()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

class GameOver():
    def __init__(self, screen, gameover, arial_font, score):
        self.screen = screen
        self.title = gameover
        self.clock = pygame.time.Clock()
        self.main_loop(arial_font, score)

    def main_loop(self, arial_font, score):
        global MENU_SELECTION
        while MENU_SELECTION == GAMEOVER_SCREEN:
            self.clock.tick(60)
            events = pygame.event.get()
            self.screen.blit(self.title, (0, 0))
            score_gameover_text = arial_font.render("Score: " + str(score), 1, (0, 0, 0))
            self.screen.blit(score_gameover_text, (50, 175))
            pygame.display.flip()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        MENU_SELECTION = START_SCREEN

class Winner():
    def __init__(self, screen, winner):
        self.screen = screen
        self.title = winner
        self.clock = pygame.time.Clock()
        self.main_loop()

    def main_loop(self):
        global MENU_SELECTION
        while MENU_SELECTION == WINNER_SCREEN:
            self.clock.tick(60)
            events = pygame.event.get()
            self.screen.blit(self.title, (0, 0))
            pygame.display.flip()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        MENU_SELECTION = START_SCREEN

def mainmenuplaceholder(screen):
    global MENU_SELECTION
    MENU_SELECTION = START_SCREEN

class Enemy(pygame.sprite.Sprite):
    enemies = []
    def __init__(self, allsprites, pos, tier):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_enemy"]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        allsprites.add(self)
        self.tier = tier
        Enemy.enemies.append(self)
    def update(self):
        self.difficulty_movement()
        newpos = (self.rect.topleft[0] + self.direction[0], self.rect.topleft[1])
        self.rect.topleft = newpos
        if(self.rect.topleft[0] < -100 and self.tier == 3):
            self.rect.topleft = (SCREEN_WIDTH, self.rect.topleft[1])
        if(self.rect.topleft[0] > SCREEN_WIDTH and (self.tier == 1 or self.tier == 2)):
            self.rect.topleft = (-68, self.rect.topleft[1])
    def difficulty_movement(self):
        # Tier 1 moves right, Tier 2 moves right, Tier 3 (bottom) moves left
        if self.tier == 1:
            self.direction = (2, 0)
        elif self.tier == 2:
            self.direction = (1, 0)
        elif self.tier == 3:
            self.direction = (-1, 0)
    def destroy(self):
        Enemy.enemies.remove(self)
        self.kill()

class Steelers(pygame.sprite.Sprite):
    steelers_list = []
    def __init__(self, allsprites, pos, tier):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_steelers"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.pos = pos
        self.rect.topleft = pos
        self.tier = tier
        Steelers.steelers_list.append(self)
    def update(self):
        self.difficulty_movement()
        newpos = (self.rect.topleft[0]+self.direction[0], self.rect.topleft[1])
        self.rect.topleft = newpos
        if(self.rect.topright[0] < 0 and self.tier == 2):
            self.rect.topleft = (SCREEN_WIDTH, self.rect.topleft[1])
        if(self.rect.topleft[0] > SCREEN_WIDTH and self.tier == 1):
            self.rect.topleft = (-100, self.rect.topleft[1])
    def difficulty_movement(self):
        if self.tier == 1:
            self.direction = (1, 0)
        elif self.tier == 2:
            self.direction = (-1, 0)
    def destroy(self):
        Steelers.steelers_list.remove(self)
        self.kill()

class Goal(pygame.sprite.Sprite):
    goals = []
    def __init__(self, allsprites, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_goal"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.rect.topleft = pos
        Goal.goals.append(self)
        self.filled = 0
    def update(self):
        pass
    def destroy(self):
        Goal.goals.remove(self)
        self.kill()
    def collision_with_player(self):
        self.image = IMAGES["spr_touchdown"]
        self.filled = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, allsprites, pos, time_left):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_player"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.player_width, self.player_height = (65, 80)
        self.speed_x, self.speed_y = 50, 40
        self.rect.topleft = (pos[0], pos[1])
        self.pos = [pos[0], pos[1]]
        self.time_left = time_left
        self.score = 0
    def update(self):
        self.image = pygame.transform.smoothscale(self.image, (self.player_width, self.player_height))
        self.rect.topleft = (self.pos[0], self.pos[1])
        self.speed_x, self.speed_y = 40, 50
        self.time_left -= .028
    def collision_with_goal(self):
        self.pos[0], self.pos[1] = SPAWN_POSITION
        self.rect.topleft = self.pos
    def destroy(self):
        self.kill()

def main():
    global MENU_SELECTION
    MENU_SELECTION = START_SCREEN
    RUNNING, RESTART, DEBUG = 0, 1, 2
    state = RESTART
    debug_message = 0
    allsprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Le'Veon Style")
    load_image("sprites/goal.png", "spr_goal", True, True)
    load_image("sprites/touchdown.png", "spr_touchdown", True, True)
    load_image("sprites/patriots.png", "spr_enemy", False, True)
    load_image("sprites/steelers.png", "spr_steelers", True, True)
    load_image("sprites/leveonbell.png", "spr_player", True, True)

    # Font and texts
    arcade_font_main = pygame.font.Font("fonts/ARCADE.ttf", 48)
    arial_font = pygame.font.SysFont('Arial', 32)
    # Backgrounds
    start_menu = pygame.image.load("sprites/startmenu.png").convert()
    start_menu = pygame.transform.scale(start_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
    game_over = pygame.image.load("sprites/gameover.png").convert()
    game_over = pygame.transform.scale(game_over, (SCREEN_WIDTH, SCREEN_HEIGHT))
    winner = pygame.image.load("sprites/winner.png").convert()
    winner = pygame.transform.scale(winner, (SCREEN_WIDTH, SCREEN_HEIGHT))
    football_field = pygame.image.load("sprites/footballfield.jpg").convert()
    football_field = pygame.transform.scale(football_field, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Window
    gameicon = pygame.image.load("sprites/bellico.png")
    pygame.display.set_icon(gameicon)
    pygame.display.set_caption('Le\'Veon Style')
    pygame.mouse.set_visible(0)
    # Sounds
    load_sound("SOUNDS/snd_leap.wav", "snd_leap")
    SOUNDS["snd_leap"].set_volume(.01)
    load_sound("SOUNDS/playerdie.wav", "snd_playerdie")
    SOUNDS["snd_playerdie"].set_volume(.01)
    # Music loop
    pygame.mixer.music.load("SOUNDS/froggertheme.mp3")
    pygame.mixer.music.set_volume(.04)
    pygame.mixer.music.play(-1)
    # Main
    while True:
        clock.tick(35)
        display_caption()
        if MENU_SELECTION == START_SCREEN: # Menu Screen
            keys = [False, False, False, False]
            Menu(screen, start_menu)
        elif MENU_SELECTION == PLAY_SCREEN and state == RESTART:
            Enemy(allsprites, (0, 120), 1)
            Enemy(allsprites, (300, 120), 1)
            Enemy(allsprites, (600, 120), 1)
            Enemy(allsprites, (0, 300), 2)
            Enemy(allsprites, (200, 300), 2)
            Enemy(allsprites, (400, 300), 2)
            Enemy(allsprites, (600, 300), 2)
            Enemy(allsprites, (0, 520), 3)
            Enemy(allsprites, (200, 520), 3)
            Enemy(allsprites, (400, 520), 3)
            Enemy(allsprites, (600, 520), 3)

            Steelers(allsprites, (350, 675), 2) # Quarterback
            Steelers(allsprites, (50, 600), 1)
            Steelers(allsprites, (200, 600), 1)
            Steelers(allsprites, (350, 600), 1)
            Steelers(allsprites, (500, 600), 1)
            Steelers(allsprites, (650, 600), 1)

            player = Player(allsprites, SPAWN_POSITION, TIME_LEFT)

            Goal(allsprites, (25, 10))
            Goal(allsprites, (175, 10))
            Goal(allsprites, (325, 10))
            Goal(allsprites, (475, 10))
            Goal(allsprites, (625, 10))

            score = 0

            state = RUNNING

        elif MENU_SELECTION == PLAY_SCREEN and state == RUNNING:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        for i in range(0, len(SOUNDS)):
                            sounds_list = list(SOUNDS.keys()) # Returns list of keys in SOUNDS
                            SOUNDS[sounds_list[i]].stop() # Stops all SOUNDS when go to menu
                        MENU_SELECTION = START_SCREEN
                    elif event.key == K_UP:
                        keys[0] = True
                    elif event.key == K_LEFT:
                        keys[1] = True
                    elif event.key == K_DOWN:
                        keys[2] = True
                    elif event.key == K_RIGHT:
                        keys[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        keys[0] = False
                    elif event.key == pygame.K_LEFT:
                        keys[1] = False
                    elif event.key == pygame.K_DOWN:
                        keys[2] = False
                    elif event.key == pygame.K_RIGHT:
                        keys[3] = False
                    elif event.key == pygame.K_SPACE:
                        debug_message = 1
                        state = DEBUG
            if keys[0]: # Up
                SOUNDS["snd_leap"].play()
                # Boundary, 32 is block, added a few extra pixels to make it look nicer
                if player.pos[1] > 50: 
                    player.pos[1] -= player.speed_y
                keys[0] = False
            if keys[2]: # Down
                SOUNDS["snd_leap"].play()
                if player.pos[1] < SCREEN_HEIGHT-95: 
                    player.pos[1] += player.speed_y
                keys[2] = False
            if keys[1]: # Left
                SOUNDS["snd_leap"].play()
                if player.pos[0] > 32:
                    player.pos[0] -= player.speed_x
                keys[1] = False
            if keys[3]: # Right
                SOUNDS["snd_leap"].play()
                if player.pos[0] < SCREEN_WIDTH-75:
                    player.pos[0] += player.speed_x
                keys[3] = False

            # Draw and Update sprites on screen
            allsprites.update()
            screen.blit(football_field, (0, 0))
            allsprites.draw(screen)
            timer_text = arcade_font_main.render("TIME:", 1, (0, 0, 0))
            screen.blit(timer_text, (SCREEN_WIDTH/2+170, SCREEN_HEIGHT-45))
            timer_countdown_text = arcade_font_main.render(str(int(player.time_left)), 1, (0, 0, 0))
            screen.blit(timer_countdown_text, (SCREEN_WIDTH-70, SCREEN_HEIGHT-45))

            # Collisions
            for enemy in Enemy.enemies:
                if pygame.sprite.collide_mask(enemy, player):
                    for spr in allsprites:
                        spr.destroy()
                    state = RESTART
                    MENU_SELECTION = GAMEOVER_SCREEN
            for goal in Goal.goals:
                if pygame.sprite.collide_mask(goal, player) and goal.filled == 0:
                    goal.collision_with_player()
                    player.collision_with_goal()
                    score += 1
            if player.time_left < 1:
                MENU_SELECTION = GAMEOVER_SCREEN
                for spr in allsprites:
                    spr.destroy()
                state = RESTART
            if score == 5:
                MENU_SELECTION = WINNER_SCREEN
                for spr in allsprites:
                    spr.destroy()
                state = RESTART

            pygame.display.flip()
        elif MENU_SELECTION == GAMEOVER_SCREEN: # Gameover Screen
            keys = [False, False, False, False]
            SOUNDS["snd_playerdie"].play()
            GameOver(screen, game_over, arial_font, score)
        elif MENU_SELECTION == WINNER_SCREEN:
            keys = [False, False, False, False]
            Winner(screen, winner)
        elif state == DEBUG and MENU_SELECTION == PLAY_SCREEN:
            if debug_message == 1:
                debug_message = 0
                # USE BREAKPOINT HERE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        state = RUNNING
if __name__ == '__main__':
    main()
