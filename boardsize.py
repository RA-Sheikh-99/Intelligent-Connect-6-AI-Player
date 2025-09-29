
import pygame
import sys

# Prompt user for board size >=6
def get_user_number():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Intelligent Connect 6 player")
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()
    input_text = ''
    running = True
    user_number = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit() and int(input_text) >= 6:
                        user_number = int(input_text)
                        running = False
                    else:
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isdigit():
                        input_text += event.unicode
        screen.fill((255, 255, 255))
        input_box = pygame.Rect(250, 250, 300, 60)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
        text_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        prompt_surface = font.render("Enter boardsize", True, (0, 0, 0))
        screen.blit(prompt_surface, (300, 180))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    return user_number