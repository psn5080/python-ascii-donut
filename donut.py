
#!----Library Import----!#
from math import cos, sin
import pygame

#!----Variable Setup----!#
pixel_width, pixel_height = 15, 15 #higher pixel size results in lower donut resolution
screen_width = 800 // pixel_width
screen_height = 800 // pixel_height
screen_size = screen_width * screen_height #approx. 50x50 pygame window

chars = ".,-~:;=!*#$@" #symbols that make up the donut, in order of intensity (. has the lowest luminosity and @ has the highest)
donut_color = (0,255,0) #donut color in rgb format

A, B = 0, 0 #set trigonometric angles to 0 at start
theta_spacing = 10 #donut fluffiness
phi_spacing = 3 #donut cross-sectional rings
R1 = 10 #donut hole size
R2 = 20 #donut thickness
K1 = screen_height * 100 * 3 / (8 * (R1 + R2)) #overall donut size

#!----PyGame Setup----!#
pygame.init()

screen = pygame.display.set_mode(size=(800, 800))
font = pygame.font.SysFont('Arial', 20, bold=True)

#!----Screen Print Function---!#
def text_display(char, x, y):
    text = font.render(str(char), True, donut_color) #donut text print properties
    text_rect = text.get_rect(center=(x, y)) #find center of screen
    screen.blit(text, text_rect) #place donut text on center


#!----MAIN CODE----!#
print_count = 0
x_pixel, y_pixel = 0, 0
donut_frozen = False
donut_spinning = True

while donut_spinning:
    screen.fill((0,0,0)) #set backgruond to black

    output = [' '] * screen_size
    zbuffer = [0] * screen_size

    for theta in range(0, 628, theta_spacing):  # theta goes around the cross-sectional circle of a torus, from 0 to 2pi (6.28)
        for phi in range(0, 628, phi_spacing):  # phi goes around the center of revolution of a torus, from 0 to 2pi (6.28)

            #trigonometric setup
            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)
            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi = cos(phi)
            sinphi = sin(phi)

            # donut size and x, y coordinates before spinning
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D (x, y, z) coordinates after rotation
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = 100 + cosA * circlex * sinphi + circley * sinA
            z_inverse = 1 / z  # one over z

            # x, y projection
            xp = int(screen_width / 2 + K1 * z_inverse * x)
            yp = int(screen_height / 2 - K1 * z_inverse * y)

            position = xp + screen_width * yp

            # luminance (ranges from -sqrt(2) to sqrt(2))
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (
                        cosA * sintheta - costheta * sinA * sinphi)

            if z_inverse > zbuffer[position]:
                zbuffer[position] = z_inverse  # larger 1/z value means the pixel is closer to the viewer than what's already plotted
                luminance_index = int(L * 8)  #L times 8 gives luminance_index range 0..11 (8 * sqrt(2) = 11)
                output[position] = chars[luminance_index if luminance_index > 0 else 0]

    #print ascii donut
    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display(output[print_count], x_pixel, y_pixel)
            print_count += 1
        x_pixel = 0
    y_pixel = 0
    print_count = 0

    #increment trigonometric spin angles
    A += 0.15
    B += 0.035

#!----PyGame Update----!#
    if not donut_frozen:
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            donut_spinning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                donut_frozen = not donut_frozen