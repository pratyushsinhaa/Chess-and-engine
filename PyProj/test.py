import pygame
pygame.init()

screen = pygame.display.set_mode((800,600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill((255,0,0))
    pygame.display.update()

pygame.quit()