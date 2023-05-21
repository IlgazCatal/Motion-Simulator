import subprocess
import sys
try:
  import pygame
  from pygame.locals import *
except ImportError:
  subprocess.Popen("python -m pip install pygame",shell=True)

# constants
FPS = 60
CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 1500, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')
#BACKGROUND = pygame.image.load('background.jpg').convert()
PLAYER_WEIGHT = 1
FORCE_MULTIPLIER = 20

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, posx, posy, force):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.posx = posx
        self.posy = posy
        self.rect.center = [posx, posy]
        self.force = force
        self.acceleration = 0

    def update(self):
        self.posx += self.acceleration / FPS
        if self.posx > WIDTH:
            self.posx -= WIDTH
        self.rect.centerx = self.posx

    def apply_force(self):
        self.acceleration = self.force / PLAYER_WEIGHT * FORCE_MULTIPLIER

    def remove_force(self):
        self.force = 0

#Second player class
class Player2(pygame.sprite.Sprite):
    def __init__(self, width, height, posx, posy, force):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 0, 0))  # Change color to distinguish from Player 1
        self.rect = self.image.get_rect()
        self.posx = posx
        self.posy = posy
        self.rect.center = [posx, posy]
        self.force = force
        self.acceleration = 0

    def update(self):
        self.posx += self.acceleration * (1 / FPS)
        if self.posx > WIDTH:
            self.posx -= WIDTH
        self.rect.centerx = self.posx

    def apply_force(self):
        self.acceleration = self.force / PLAYER_WEIGHT * FORCE_MULTIPLIER

    def remove_force(self):
        self.force = 0
       
#Border class
class Borders(pygame.sprite.Sprite):
  def __init__(self,posx,posy,width,height):
    super().__init__()
    self.image = pygame.Surface([width,height])
    self.image.fill((255,255,255))
    self.rect = self.image.get_rect()
    self.rect.center = [posx,posy]
  
#Slider class
class Slider(pygame.sprite.Sprite):
    def __init__(self, posx, posy, width, height, color, value):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.color = color
        self.value = value
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(posx, posy))
        self.handle = pygame.Rect(posx,posy,height,height)

    def draw_slider(self):
        pygame.draw.rect(SCREEN,(127.5,127.5,127.5),self.rect)
        pygame.draw.rect(SCREEN,(255,255,255), self.handle)

    def update_cube_weight(self):
        global PLAYER_WEIGHT
        PLAYER_WEIGHT = int(slider.handle.centerx) - 1309

pygame.init()
pygame.font.init()
 
#player group shenanigans
player = Player(75,75,75,HEIGHT / 2,0)
player_group = pygame.sprite.Group()
player_group.add(player)
player2 = Player2(75, 75, WIDTH - 75, HEIGHT / 2, 0)
player_group.add(player2)

#Border group 
borders = Borders(WIDTH,HEIGHT, 1, HEIGHT * 2)
borders_copy = Borders(0,0,1,HEIGHT * 2)
border_group = pygame.sprite.Group()
border_group.add(borders,borders_copy)
player_group.add(borders,borders_copy)

#Slider group
slider = Slider(WIDTH - 200,128,200,20,(150, 150, 150),50)
slider_group = pygame.sprite.Group()
slider_group.add(slider)


#collision handler function
def handle_collision():
    border_collisions = pygame.sprite.spritecollide(player, border_group, False)
    if border_collisions:
        player2.rect.center = [150, 400]


    border_collisions2 = pygame.sprite.spritecollide(player2, border_group, False)
    if border_collisions2:
        player.rect.center = [WIDTH - 75, 400]

    player_collisions = pygame.sprite.collide_rect(player, player2)
    if player_collisions:
        player.posx -= player.force 
        player.force = 0
        player2.posx += player2.force 
        player2.force = 0 
       
# Game loop.
def main():
  dragging = False
  while True:
    #Event loops
    player.update()
    player2.update()
    for event in pygame.event.get():  
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      # Player 2 controls
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            player.force += 20
        if event.key == pygame.K_e:
            player.force -= 10

    # Player 2 controls
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player2.force -= 20
        if event.key == pygame.K_DOWN:
            player2.force += 10
      # Slider events
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if slider.handle.collidepoint(mouse_x,mouse_y):
          dragging = True
      elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False
      elif event.type == pygame.MOUSEMOTION:
        if dragging:
          mouse_x, mouse_y = pygame.mouse.get_pos()
          slider.handle.centerx = mouse_x
          if slider.handle.left < slider.rect.left:
            slider.handle.left = slider.rect.left
          if slider.handle.right > slider.rect.right:
            slider.handle.right = slider.rect.right
          slider.value = int((slider.handle.centerx - slider.rect.left) / slider.width)
          slider.update_cube_weight()
      

    #weight display
    font = pygame.font.Font(None,64)
    text = font.render(f'Weight: {PLAYER_WEIGHT}',True,(255,255,255))
    force_text = font.render(f'Force (Red): {-player2.force}',True,(255,255,255))
    force_text1 = font.render(f'Force (White): {player.force}',True,(255,255,255))
     
    #Update position of player
    player.apply_force()
    player2.apply_force()
    
    player.update()
    player2.update()

    handle_collision()
    # update
    #SCREEN.blit(background, (0, 0))
    SCREEN.fill((0,0,0))
    player_group.update()
    player_group.draw(SCREEN)
    SCREEN.blit(text,(WIDTH - 400,0))
    SCREEN.blit(force_text,(0,64))
    SCREEN.blit(force_text1,(0,0))
    slider.update()
    slider.draw_slider()
    pygame.display.flip()
    CLOCK.tick(FPS)

if __name__ == "__main__":
  main()
