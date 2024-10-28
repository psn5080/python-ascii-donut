from math import cos, sin
import pygame
import random

# Constants
PIXEL_WIDTH, PIXEL_HEIGHT = 15, 15
SCREEN_WIDTH = 800 // PIXEL_WIDTH
SCREEN_HEIGHT = 800 // PIXEL_HEIGHT
SCREEN_SIZE = SCREEN_WIDTH * SCREEN_HEIGHT
CHARS = ".,-~:;=!*#$@"
DEFAULT_DONUT_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
FONT_SIZE = 20
THETA_SPACING = 10
PHI_SPACING = 3
R1 = 10
R2 = 20
K1 = SCREEN_HEIGHT * 100 * 3 / (8 * (R1 + R2))

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode(size=(800, 800))
font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)

def text_display(char, x, y, color):
    text = font.render(str(char), True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def main():
    A, B = 0, 0
    donut_frozen = False
    donut_spinning = True
    donut_color = DEFAULT_DONUT_COLOR

    while donut_spinning:
        screen.fill(BACKGROUND_COLOR)
        output = [' '] * SCREEN_SIZE
        zbuffer = [0] * SCREEN_SIZE

        for theta in range(0, 628, THETA_SPACING):
            for phi in range(0, 628, PHI_SPACING):
                cosA, sinA = cos(A), sin(A)
                cosB, sinB = cos(B), sin(B)
                costheta, sintheta = cos(theta), sin(theta)
                cosphi, sinphi = cos(phi), sin(phi)

                circlex = R2 + R1 * costheta
                circley = R1 * sintheta

                x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
                y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
                z = 100 + cosA * circlex * sinphi + circley * sinA
                z_inverse = 1 / z

                xp = int(SCREEN_WIDTH / 2 + K1 * z_inverse * x)
                yp = int(SCREEN_HEIGHT / 2 - K1 * z_inverse * y)
                position = xp + SCREEN_WIDTH * yp

                L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (
                            cosA * sintheta - costheta * sinA * sinphi)

                if z_inverse > zbuffer[position]:
                    zbuffer[position] = z_inverse
                    luminance_index = int(L * 8)
                    output[position] = CHARS[luminance_index if luminance_index > 0 else 0]

        y_pixel = 0
        print_count = 0
        for i in range(SCREEN_HEIGHT):
            y_pixel += PIXEL_HEIGHT
            x_pixel = 0
            for j in range(SCREEN_WIDTH):
                x_pixel += PIXEL_WIDTH
                text_display(output[print_count], x_pixel, y_pixel, donut_color)
                print_count += 1

        A += 0.15
        B += 0.035

        if not donut_frozen:
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                donut_spinning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    donut_frozen = not donut_frozen
                elif event.key == pygame.K_c:  # Change color
                    donut_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                elif event.key == pygame.K_ESCAPE:  # Exit with ESC
                    donut_spinning = False

if __name__ == "__main__":
    main()
