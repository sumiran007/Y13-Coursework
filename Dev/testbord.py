import pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Bouncing")

# Colors
background_color = (0, 0, 0)  # Black
ball_color = (255, 0, 0)  # Red

# Ball settings
ball_radius = 20
ball_x, ball_y = screen_width // 2, screen_height // 2
ball_speed_x, ball_speed_y = 5, 3  # Ball movement speed

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collision with screen boundaries
    if ball_x - ball_radius < 0:  # Left boundary
        ball_x = ball_radius  # Reset position
        ball_speed_x = -ball_speed_x  # Reverse direction

    if ball_x + ball_radius > screen_width:  # Right boundary
        ball_x = screen_width - ball_radius
        ball_speed_x = -ball_speed_x

    if ball_y - ball_radius < 0:  # Top boundary
        ball_y = ball_radius
        ball_speed_y = -ball_speed_y

    if ball_y + ball_radius > screen_height:  # Bottom boundary
        ball_y = screen_height - ball_radius
        ball_speed_y = -ball_speed_y

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
