import pygame


pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Fuzzy Chess")

size = 50
white = (255,255,255)
black = (0,0,0)

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    boardLength = 8
    screen.fill(white)

    cnt = 0
    for i in range(1, boardLength + 1):
        for z in range(1, boardLength + 1):
            # check if current loop value is even
            if cnt % 2 == 0:
                pygame.draw.rect(screen, white, [size * z, size * i, size, size])
            else:
                pygame.draw.rect(screen, black, [size * z, size * i, size, size])
            cnt += 1
        # since theres an even number of squares go back one value
        cnt -= 1
    # Add a nice boarder
    pygame.draw.rect(screen, black, [size, size, boardLength * size, boardLength * size], 1)
    pygame.display.update()