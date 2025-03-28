import pygame

pygame.init() #Initialize pygame
screen = pygame.display.set_mode((400, 400), pygame.RESIZABLE|pygame.HWSURFACE | pygame.DOUBLEBUF) #Set resolution
clock =  pygame.time.Clock() #Clock it runs off
running = True #checks if game is running
dt = 0 #Delta time
game_state = "menu"

#Name of window
pygame.display.set_caption("Python Game") 

#Player position
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) 

is_crocuhing = False

#Camera Offset
camera_offset_x = 0
camera_offset_y = 0

#Gravity and Velocity
player_velocity_y = 0
gravity = 200
on_ground = False

ground_width = 800
ground_height = 50
ground_x = 0
ground_y = screen.get_height() - 50 
ground_rect = pygame.Rect(ground_x, ground_y, ground_width, ground_height)

lower_ground_width = 800
lower_ground_height = 20
lower_ground_x = 0
lower_ground_y = 380
lower_ground_rect = pygame.Rect(lower_ground_x, lower_ground_y, lower_ground_width, lower_ground_height)

floating_platform_width = 30
floating_platform_height = 30
floating_platform_x = 200
floating_platform_y = 350
floating_platform_rect = pygame.Rect(floating_platform_x, floating_platform_y, floating_platform_width, floating_platform_height)

wall_width = 10
wall_height = 400
wall_x = -10
wall_y = 0
wall_rect = pygame.Rect(wall_x, wall_y, wall_width, wall_height)

floating_platforms = [
    pygame.Rect(300, 350, 30, 30),
    pygame.Rect(500, 350, 30, 30),
    pygame.Rect(600, 350, 30, 30),
    pygame.Rect(700, 350, 30, 30),
    pygame.Rect(770, 350, 30, 30),
]

#Closing window
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_SPACE:
                    game_state = "level_1"
                elif event.key == pygame.K_h:
                    game_state = "help"
            elif game_state == "level_1":
                pass

    dt = clock.tick(60) / 1000

    screen.fill(("blue"))

    if game_state == "menu":
        screen.fill((0, 0, 0)) # Fill screen with black
        font_large = pygame.font.Font(None, 75)
        font_small = pygame.font.Font(None, 36)
        title_font = font_large.render("Python Game", True, (255, 255, 255))
        title_rect = title_font.get_rect(center=(screen.get_width() / 2, screen.get_height() // 3))
        start_font = font_small.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_font.get_rect(center=(screen.get_width() / 2, screen.get_height() // 2))
        help_font = font_small.render("Press H for 'HOW TO PLAY'", True, (255, 255, 255))
        help_rect = help_font.get_rect(center=(screen.get_width() / 2, screen.get_height() * 2 // 3))
        quit_font = font_small.render("Press R to Quit", True, (255, 255, 255))
        quit_rect = quit_font.get_rect(center=(screen.get_width() / 2, screen.get_height() * 2 // 2.5))
        screen.blit(title_font, title_rect)
        screen.blit(start_font, start_rect)
        screen.blit(quit_font, quit_rect)
        screen.blit(help_font, help_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]: #Uses "r" to "reset" window
            pygame.quit()
            running = False

    elif game_state == "help":
        screen.fill((0, 0, 0))
        font_large = pygame.font.Font(None, 75)
        font_small = pygame.font.Font(None, 36)
        help_title = font_large.render("How to Play", True, (255, 255, 255))
        help_title_rect = help_title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(help_title, help_title_rect)

        controls_text = font_small.render("Controls:", True, (255, 255, 255))
        controls_rect = controls_text.get_rect(left=50, top=180)
        screen.blit(controls_text, controls_rect)

        move_text = font_small.render("W: Jump", True, (200, 200, 200))
        move_rect = move_text.get_rect(left=70, top=210)
        screen.blit(move_text, move_rect)

        crouch_text = font_small.render("S: Crouch", True, (200, 200, 200))
        crouch_rect = crouch_text.get_rect(left=70, top=240)
        screen.blit(crouch_text, crouch_rect)

        left_text = font_small.render("A: Move Left", True, (200, 200, 200))
        left_rect = left_text.get_rect(left=70, top=270)
        screen.blit(left_text, left_rect)

        right_text = font_small.render("D: Move Right", True, (200, 200, 200))
        right_rect = right_text.get_rect(left=70, top=300)
        screen.blit(right_text, right_rect)

        quit_help_text = font_small.render("Press M to return to Menu", True, (200, 200, 200))
        quit_help_rect = quit_help_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(quit_help_text, quit_help_rect)

    elif game_state == "level_1":
        player_velocity_y += gravity * dt
        player_pos.y += player_velocity_y * dt

        player_radius = 20
        player_rect = pygame.Rect(
            player_pos.x - player_radius,
            player_pos.y - player_radius,
            player_radius * 2,
            player_radius * 2
        )

        if player_rect.colliderect(ground_rect):
            player_pos.y = ground_rect.top - player_radius
            player_velocity_y = 0
            on_ground = True
        else:
            on_ground = False

        if player_rect.colliderect(wall_rect):
            if player_pos.x < wall_rect.right and player_pos.x > wall_rect.left:
                if player_pos.x < wall_rect.centerx:
                    player_pos.x = wall_rect.left - player_radius
            else:
                player_pos.x = wall_rect.right + player_radius

        for platform_rect in floating_platforms:
            if player_rect.colliderect(platform_rect):
                player_pos.x = screen.get_width() // 2
                player_pos.y = screen.get_height() //2  
                player_velocity_y = 0
                on_grounf = False 

        # Calculate camera offset
        camera_offset_x = player_pos.x - screen.get_width() // 2
        camera_offset_y = 0

        # Text
        font = pygame.font.Font(None, 36)
        text = font.render("Pygame Game", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = screen.get_width() // 2 - camera_offset_x # Adjusted text position with camera offset
        textpos.centery = 50
        second_text = font.render("Made by Mineman130", 1, (10, 10, 10))
        second_textpos = text.get_rect()
        second_textpos.centerx = screen.get_width() // 2.5 - camera_offset_x # Adjusted text position with camera offset
        second_textpos.centery = 80
        screen.blit(text, textpos)
        screen.blit(second_text, second_textpos)

        original_radius = 20
        crouch_radius = 10
        current_radius = original_radius
        if is_crocuhing:
            current_radius = crouch_radius
            player_pos.y += (original_radius - current_radius)

        # Draws a circle to screen (player)
        pygame.draw.circle(screen, "white", (player_pos.x - camera_offset_x, player_pos.y - camera_offset_y), player_radius)

        # Draw the ground
        pygame.draw.rect(screen, "green", (ground_rect.x - camera_offset_x, ground_rect.y - camera_offset_y, ground_rect.width, ground_rect.height))

        # Draw the wall
        pygame.draw.rect(screen, "brown", (wall_rect.x - camera_offset_x, wall_rect.y - camera_offset_y, wall_rect.width, wall_rect.height))

        # Draw the lower ground
        pygame.draw.rect(screen, "brown", (lower_ground_rect.x - camera_offset_x, lower_ground_rect.y - camera_offset_y, lower_ground_rect.width, lower_ground_rect.height))

        # Draw the bad spots
        for platform_rect in floating_platforms:
            pygame.draw.rect(screen, "red", (platform_rect.x - camera_offset_x, platform_rect.y - camera_offset_y, platform_rect.width, platform_rect.height))

        # Draws a circle to screen (again, this is redundant - remove this line)
        # pygame.draw.circle(screen, "white", player_pos, player_radius)

        # Get pressed keys
        keys = pygame.key.get_pressed() #Move player with WASD
        if keys[pygame.K_w]:
            player_pos.y -= 100 * dt
        if keys[pygame.K_s]:
            is_crocuhing = True
        else:
            is_crocuhing = False
        if keys[pygame.K_a]:
            player_pos.x -= 150 * dt
        if keys[pygame.K_d]:
            player_pos.x += 150 * dt


    keys = pygame.key.get_pressed() #Checks for keys pressed after everything is loaded
    if keys[pygame.K_r]: # Check for 'R' key here, outside the game state blocks, meaning this will work in any game_state
        pygame.quit()
        running = False

    if keys[pygame.K_m]: # Check for 'M' key here
        game_state = "menu"

    pygame.display.flip()