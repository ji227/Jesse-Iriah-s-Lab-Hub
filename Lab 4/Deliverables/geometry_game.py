# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont # Use Pillow for image manipulation
import pygame
import random
import busio
import sys
import time

# --- Attempt to import all hardware libraries ---
try:
    import qwiic_joystick
    joystick_connected = True
except (ImportError, ModuleNotFoundError):
    joystick_connected = False

try:
    from adafruit_seesaw.seesaw import Seesaw
    from adafruit_seesaw.rotaryio import IncrementalEncoder
    encoder_connected = True
except (ImportError, ModuleNotFoundError):
    encoder_connected = False

# --- Qwiic Button LED Setup (Green LED control) ---
try:
    import qwiic_button
    button = qwiic_button.QwiicButton()
    if button.is_connected():
        print("Qwiic Button detected.")
        button.LED_off()  # start with LED off
        qwiic_button_connected = True
    else:
        print("Qwiic Button not connected.")
        qwiic_button_connected = False
except (ImportError, AttributeError, OSError) as e:
    print(f"Qwiic Button module not found or initialization failed: {e}")
    qwiic_button_connected = False

# --- MODIFIED: Import new display driver ---
from adafruit_ssd1305 import SSD1305_SPI

# --- Hardware Setup ---
i2c = busio.I2C(board.SCL, board.SDA)

# Joystick Setup
if joystick_connected:
    myJoystick = qwiic_joystick.QwiicJoystick(i2c)
    if not myJoystick.connected:
        print("Joystick not connected, falling back to keyboard.", file=sys.stderr)
        joystick_connected = False
    else:
        myJoystick.begin()
        print(f"Joystick Initialized. Firmware: {myJoystick.version}")

# Rotary Encoder Setup
if encoder_connected:
    try:
        seesaw = Seesaw(i2c, addr=0x36)
        seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
        encoder = IncrementalEncoder(seesaw)
        last_encoder_pos = encoder.position
    except ValueError:
        print("Rotary Encoder not found. Use L/R Arrow Keys in menu.", file=sys.stderr)
        encoder_connected = False

def set_qwiic_led(on: bool):
    """
    Turns the Qwiic Button LED on (green) or off.
    """
    if not qwiic_button_connected:
        return
    try:
        if on:
            button.LED_on(100)   # RGB(0,255,0) = green
        else:
            button.LED_off()
    except Exception:
        pass

# --- MODIFIED: Display Setup for Waveshare 128x32 OLED ---
spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.D17)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)
disp = SSD1305_SPI(128, 32, spi, dc_pin, reset_pin, cs_pin)

# Clear display.
disp.fill(0)
disp.show()

# --- MODIFIED: Global Pygame & Game Setup for new resolution ---
SCREEN_WIDTH, SCREEN_HEIGHT = 128, 32
pygame.init()
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
WHITE, BLACK, GREEN = (255, 255, 255), (0, 0, 0), (0, 255, 0)
# Use smaller fonts for the tiny screen
font = pygame.font.Font(None, 12)
title_font = pygame.font.Font(None, 16)
clock = pygame.time.Clock()
FPS = 30



# --- NEW: Function to update the monochrome display ---
def update_display(pygame_surface):
    """Converts a Pygame surface to a 1-bit PIL Image and displays it."""
    # Convert pygame surface to a PIL image
    pil_string_image = pygame.image.tostring(pygame_surface, "RGB")
    pil_image = Image.frombytes("RGB", pygame_surface.get_size(), pil_string_image)

    # Convert the PIL image to black and white
    mono_image = pil_image.convert("1")

    # Display the monochrome image
    disp.image(mono_image)
    disp.show()


player_sprite_raw = pygame.Surface((10, 10))  # create a 10x10 pixel surface
player_sprite_raw.fill((0, 0, 0))  # black square
# ##########################################################################
# DINO GAME CODE (Rescaled for 128x32)
# ##########################################################################

DINO_GROUND_LEVEL = SCREEN_HEIGHT - 5

class DinoPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.normal_height = 10
        self.duck_height = 5
        self.sprite_width = 9

        self.image = pygame.transform.scale(player_sprite_raw, (self.sprite_width, self.normal_height))
        self.rect = self.image.get_rect(bottomleft=(10, DINO_GROUND_LEVEL))
        
        self.velocity_y = 0
        self.gravity = 0.4  # Scaled down gravity
        self.jump_strength = -5 # Scaled down jump
        self.is_jumping = False
        self.is_ducking = False

    def update(self):
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
        if self.rect.bottom >= DINO_GROUND_LEVEL:
            self.rect.bottom = DINO_GROUND_LEVEL
            self.is_jumping = False
            self.velocity_y = 0

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.is_jumping = True
            self.velocity_y = self.jump_strength

    def duck(self, is_pressed):
        if self.is_jumping: return
        
        current_bottom = self.rect.bottom
        if is_pressed and not self.is_ducking:
            self.is_ducking = True
            self.image = pygame.transform.scale(player_sprite_raw, (self.sprite_width, self.duck_height))
            self.rect = self.image.get_rect(bottomleft=(10, current_bottom))

        elif not is_pressed and self.is_ducking:
            self.is_ducking = False
            self.image = pygame.transform.scale(player_sprite_raw, (self.sprite_width, self.normal_height))
            self.rect = self.image.get_rect(bottomleft=(10, current_bottom))

class DinoObstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # Scaled down obstacles
        if random.choice([True, False]):
            self.image = pygame.Surface([5, 10])
            self.rect = self.image.get_rect(bottomleft=(SCREEN_WIDTH, DINO_GROUND_LEVEL))
        else:
            self.image = pygame.Surface([8, 8])
            self.rect = self.image.get_rect(bottomleft=(SCREEN_WIDTH, DINO_GROUND_LEVEL - 8))
        self.image.fill(BLACK)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

def dino_game_loop():
    player = DinoPlayer()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    game_over = False
    score, game_speed = 0, 4
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 2500)

    while True:
        if encoder_connected and not seesaw.digital_read(24):
            time.sleep(0.1); return "MENU"

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if not game_over and event.type == obstacle_timer:
                new_obstacle = DinoObstacle(game_speed)
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)

        if game_over:
            if joystick_connected and myJoystick.button == 0: return "MENU"
        else:
            if joystick_connected:
                y = myJoystick.vertical
                if y > 700: player.jump()
                player.duck(y < 300)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]: player.jump()
                player.duck(keys[pygame.K_DOWN])

            all_sprites.update()
            score += 1
            if pygame.sprite.spritecollide(player, obstacles, False): game_over = True
            if score % 200 == 0: game_speed = min(8, game_speed + 1)

        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, (0, DINO_GROUND_LEVEL), (SCREEN_WIDTH, DINO_GROUND_LEVEL), 1)
        all_sprites.draw(screen)
        score_text = font.render(f"{score // 10}", True, BLACK)
        screen.blit(score_text, (5, 5))

        if game_over:
            msg = title_font.render("GAME OVER", True, BLACK)
            screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))

        update_display(screen) # Use the new display function
        clock.tick(FPS)

# ##########################################################################
# MAZE GAME CODE (Rescaled for 128x32)
# ##########################################################################

# --- MODIFIED: Maze dimensions for new screen size ---
CELL_SIZE = 4
MAZE_COLS = SCREEN_WIDTH // CELL_SIZE
MAZE_ROWS = SCREEN_HEIGHT // CELL_SIZE
MAZE_OFFSET_X, MAZE_OFFSET_Y = 0, 0 # No offset needed if it fills screen

class MazePlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_size = CELL_SIZE - 1 # Player is almost as big as a cell
        self.image = pygame.transform.scale(player_sprite_raw, (player_size, player_size))
        self.x, self.y = 0, 0
        self.rect = self.image.get_rect(topleft=(MAZE_OFFSET_X, MAZE_OFFSET_Y))

    def move(self, dx, dy, walls):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < MAZE_COLS and 0 <= new_y < MAZE_ROWS:
            current_cell_walls = walls[self.y][self.x]
            if dx == -1 and not current_cell_walls[0]: self._update_pos(new_x, new_y)
            elif dx == 1 and not current_cell_walls[1]: self._update_pos(new_x, new_y)
            elif dy == -1 and not current_cell_walls[2]: self._update_pos(new_x, new_y)
            elif dy == 1 and not current_cell_walls[3]: self._update_pos(new_x, new_y)

    def _update_pos(self, new_x, new_y):
        self.x, self.y = new_x, new_y
        self.rect.x = MAZE_OFFSET_X + self.x * CELL_SIZE
        self.rect.y = MAZE_OFFSET_Y + self.y * CELL_SIZE

def generate_maze():
    walls = [[[True, True, True, True] for _ in range(MAZE_COLS)] for _ in range(MAZE_ROWS)] # L,R,U,D
    stack, visited = [(0, 0)], {(0, 0)}
    while stack:
        x, y = stack[-1]
        neighbors = []
        if x > 0 and (x-1, y) not in visited: neighbors.append((x-1, y, 0, 1))
        if x < MAZE_COLS-1 and (x+1, y) not in visited: neighbors.append((x+1, y, 1, 0))
        if y > 0 and (x, y-1) not in visited: neighbors.append((x, y-1, 2, 3))
        if y < MAZE_ROWS-1 and (x, y+1) not in visited: neighbors.append((x, y+1, 3, 2))
        if neighbors:
            nx, ny, wall, opp_wall = random.choice(neighbors)
            walls[y][x][wall] = False
            walls[ny][nx][opp_wall] = False
            visited.add((nx, ny)); stack.append((nx, ny))
        else: stack.pop()
    return walls

def maze_game_loop():
    player = MazePlayer()
    all_sprites = pygame.sprite.Group(player)
    walls = generate_maze()
    goal_rect = pygame.Rect(MAZE_OFFSET_X + (MAZE_COLS-1)*CELL_SIZE, MAZE_OFFSET_Y + (MAZE_ROWS-1)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    last_move_time, move_cooldown = 0, 200

    while True:
        if encoder_connected and not seesaw.digital_read(24):
            time.sleep(0.1); return "MENU"

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"

        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > move_cooldown:
            dx, dy = 0, 0
            # --- SYNTAX FIX HERE ---
            if joystick_connected:
                x, y = myJoystick.horizontal, myJoystick.vertical
                if x < 300:
                    dx = -1
                elif x > 700:
                    dx = 1
                elif y < 300:
                    dy = -1
                elif y > 700:
                    dy = 1
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    dx = -1
                elif keys[pygame.K_RIGHT]:
                    dx = 1
                elif keys[pygame.K_UP]:
                    dy = -1
                elif keys[pygame.K_DOWN]:
                    dy = 1
            
            if dx != 0 or dy != 0:
                player.move(dx, dy, walls)
                last_move_time = current_time

        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, goal_rect)
        for r in range(MAZE_ROWS):
            for c in range(MAZE_COLS):
                x, y = MAZE_OFFSET_X + c * CELL_SIZE, MAZE_OFFSET_Y + r * CELL_SIZE
                if walls[r][c][0]: pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE))
                if walls[r][c][1]: pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
                if walls[r][c][2]: pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y))
                if walls[r][c][3]: pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE))
        all_sprites.draw(screen)

        if player.x == MAZE_COLS-1 and player.y == MAZE_ROWS-1:
            win_text = title_font.render("YOU WIN!", True, BLACK)
            screen.blit(win_text, win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
            update_display(screen); time.sleep(2); return "MENU"

        update_display(screen) # Use the new display function
        clock.tick(FPS)

# ##########################################################################
# MENU AND MAIN APP LOOP
# ##########################################################################

def menu_loop():
    global last_encoder_pos
    games = ["DINO GAME", "MAZE GAME"]
    selected_game_idx = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if not joystick_connected and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: selected_game_idx = (selected_game_idx - 1) % len(games)
                if event.key == pygame.K_RIGHT: selected_game_idx = (selected_game_idx + 1) % len(games)
                if event.key == pygame.K_RETURN: return games[selected_game_idx].replace(" ", "_")
        
        # --- SYNTAX FIX HERE ---
        if encoder_connected:
            pos = encoder.position
            if pos > last_encoder_pos:
                selected_game_idx = (selected_game_idx + 1) % len(games)
            elif pos < last_encoder_pos:
                selected_game_idx = (selected_game_idx - 1) % len(games)
            last_encoder_pos = pos

        if joystick_connected and myJoystick.button == 0:
            time.sleep(0.2); return games[selected_game_idx].replace(" ", "_")

        screen.fill(WHITE)
        title_text = title_font.render("Pi Game Console", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH/2, 8)))

        for i, game in enumerate(games):
            # We only have space to show one game at a time now
            if i == selected_game_idx:
                game_text = font.render(game, True, BLACK)
                screen.blit(game_text, game_text.get_rect(center=(SCREEN_WIDTH/2, 24)))

        # Simple indicator for selected game
        if selected_game_idx == 0:
            pygame.draw.line(screen, BLACK, (35, 30), (85, 30), 1)
        else:
            pygame.draw.line(screen, BLACK, (35, 30), (85, 30), 1)


        update_display(screen) # Use the new display function
        clock.tick(FPS)
if __name__ == "__main__":
    game_state = "MENU"
    while game_state != "QUIT":
        # Control Qwiic LED based on game state
        set_qwiic_led(on=(game_state != "MENU"))

        if game_state == "MENU":
            game_state = menu_loop()
        elif game_state == "DINO_GAME":
            game_state = dino_game_loop()
        elif game_state == "MAZE_GAME":
            game_state = maze_game_loop()

    # Turn LED off on exit
    set_qwiic_led(False)
    pygame.quit()
    sys.exit()

