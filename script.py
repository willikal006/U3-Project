# ============================================================
#  MONSTER WRANGLER — Build Day 1
#  Principles of Computing | Unit 3 — OOP + Game Projects
#  March 5, 2025
# ============================================================

import pygame, random

# ---- Initialize pygame ----
pygame.init()

# ---- Display Window ----
WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

# ---- FPS and Clock ----
FPS   = 60
clock = pygame.time.Clock()


# ==============================================================
#  TODO 1 — Game.__init__
# ==============================================================

class Game():
    """A class to control gameplay"""

    def __init__(self, player, monster_group):
        """Initialize the game object"""

        # -- Game tracking values --
        self.score        = 0
        self.round_number = 0
        self.round_time   = 0
        self.frame_count  = 0

        # -- References to other objects --
        self.player        = player
        self.monster_group = monster_group

        # -- Sound --
        self.next_level_sound = pygame.mixer.Sound("next_level.wav")

        # -- Font --
        self.font = pygame.font.Font("Abrushow.ttf", 24)

        # -- Monster target images --
        blue_image   = pygame.image.load("blue_monster.png").convert_alpha()
        green_image  = pygame.image.load("green_monster.png").convert_alpha()
        purple_image = pygame.image.load("purple_monster.png").convert_alpha()
        yellow_image = pygame.image.load("yellow_monster.png").convert_alpha()
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]

        # -- Choose a random starting target type --
        self.target_monster_type  = random.randint(0, 3)

        # Use target_monster_type as an index into self.target_monster_images
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        # -- Target monster display rect --
        self.target_monster_rect          = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx  = WINDOW_WIDTH // 2
        self.target_monster_rect.top      = 30


    # ==============================================================
    #  TODO 2 — Game.update
    # ==============================================================

    def update(self):
        """Update the game object"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time  += 1
            self.frame_count  = 0

        self.check_collisions()


    # ==============================================================
    #  TODO 3 — Game.draw
    # ==============================================================

    def draw(self):
        """Draw the HUD to the display"""

        # -- Colors --
        WHITE  = (255, 255, 255)
        BLUE   = (20,  176, 235)
        GREEN  = (87,  201,  47)
        PURPLE = (226,  73, 243)
        YELLOW = (243, 157,  20)

        # List: index matches monster type
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # -- Build text surfaces --
        catch_text  = self.font.render("Current Catch", True, WHITE)
        catch_rect  = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH // 2
        catch_rect.top      = 5

        score_text  = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect  = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text  = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect  = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text  = self.font.render("Current Round: " + str(self.round_number), True, WHITE)
        round_rect  = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text   = self.font.render("Round Time: " + str(self.round_time), True, WHITE)
        time_rect   = time_text.get_rect()
        time_rect.topright  = (WINDOW_WIDTH - 10, 5)

        warp_text   = self.font.render("Warps: " + str(self.player.warps), True, WHITE)
        warp_rect   = warp_text.get_rect()
        warp_rect.topright  = (WINDOW_WIDTH - 10, 35)

        # blit all six text surfaces
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)

        # blit target monster image
        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        # colored outline box around the target monster image
        pygame.draw.rect(
            display_surface,
            colors[self.target_monster_type],
            (WINDOW_WIDTH // 2 - 32, 30, 64, 64),
            2
        )

        # colored play area border
        pygame.draw.rect(
            display_surface,
            colors[self.target_monster_type],
            (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200),
            4
        )


    # ---- These methods are stubs — you'll build them on Days 2 & 3 ----

    def check_collisions(self):
        """Check for collisions between player and monsters — Day 2"""
        pass

    def start_new_round(self):
        """Start a new round — Day 2"""
        self.round_number += 1
        self.round_time    = 0
        self.frame_count   = 0

    def choose_new_target(self):
        """Choose a new target monster — Day 2"""
        pass

    def pause_game(self, main_text, sub_text):
        """Pause the game and show message — Day 3"""
        global running
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        if self.font:
            main_surface = self.font.render(main_text, True, WHITE)
            main_rect    = main_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            sub_surface  = self.font.render(sub_text,  True, WHITE)
            sub_rect     = sub_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64))
            display_surface.fill(BLACK)
            display_surface.blit(main_surface, main_rect)
            display_surface.blit(sub_surface,  sub_rect)
        else:
            display_surface.fill(BLACK)

        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running   = False

    def reset_game(self):
        """Reset the game — Day 3"""
        pass


# ==============================================================
#  TODO 4 — Player.__init__
# ==============================================================

class Player(pygame.sprite.Sprite):
    """A player class that the user can control"""

    def __init__(self):
        """Initialize the player"""
        super().__init__()

        # load knight.png into self.image
        self.image = pygame.image.load("knight.png").convert_alpha()

        # place player bottom-center
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom  = WINDOW_HEIGHT - 10

        # basic player stats (used by HUD)
        self.lives = 3
        self.warps = 3
