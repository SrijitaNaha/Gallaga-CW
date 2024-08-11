import pgzrun
import random

# Screen dimensions
WIDTH = 1200
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize score
score = 0
lives = 3

# Create a ship
ship = Actor('galaga')
ship.pos = (WIDTH // 2, HEIGHT - 60)

# Initialize bullets
bullets = []

# Initialize enemies
enemies = []
for _ in range(8):
    enemy = Actor('bug')
    enemy.x = random.randint(0, WIDTH - 80)
    enemy.y = random.randint(-100, 0)
    enemies.append(enemy)

# Set enemy movement direction
direction = 1

# Set enemy movement speed
speed = 5

# Function to display score
def display_score():
    screen.draw.text(f'Score: {score}', (50, 30))
    screen.draw.text(f'Lives: {lives}', (50, 60))

# Function to handle key down events
def on_key_down(key):
    if key == keys.SPACE:
        # Create a new bullet
        bullet = Actor('bullet')
        bullet.x = ship.x
        bullet.y = ship.y - 50
        bullets.append(bullet)

# Function to update game state
def update():
    global score
    global direction
    global lives

    # Move ship left or right
    if keyboard.left:
        ship.x -= speed
        if ship.x <= 0:
            ship.x = 0
    elif keyboard.right:
        ship.x += speed
        if ship.x >= WIDTH:
            ship.x = WIDTH

    # Move bullets
    for bullet in bullets:
        if bullet.y <= 0:
            bullets.remove(bullet)
        else:
            bullet.y -= 10

    # Move enemies
    move_down = False
    for enemy in enemies:
        enemy.y += 5
        if enemy.y > HEIGHT:
            enemy.x = random.randint(0, WIDTH - 80)
            enemy.y = random.randint(-100, 0)

        # Check for collisions with bullets
        for bullet in bullets:
            if enemy.colliderect(bullet):
                sounds.eep.play()
                score += 100
                bullets.remove(bullet)
                enemies.remove(enemy)

        # Check for collisions with ship
        if enemy.colliderect(ship):
            lives -= 1
            enemies.remove(enemy)
            if lives == 0:
                game_over()

# Function to draw game state
def draw():
    if lives > 0:
        screen.clear()
        screen.fill(BLUE)
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        ship.draw()
        display_score()
    else:
        game_over_screen()

# Function to handle game over
def game_over():
    pass  # Do nothing, just let the game over screen handle it

# Function to draw game over screen
def game_over_screen():
    screen.clear()
    screen.fill(BLUE)
    screen.draw.text('GAME OVER', (WIDTH // 2 - 150, HEIGHT // 2 - 50), fontsize=60, color=WHITE)
    screen.draw.text(f'Final Score: {score}', (WIDTH // 2 - 100, HEIGHT // 2 + 20), fontsize=40, color=WHITE)
    screen.draw.text('Press SPACE to play again', (WIDTH // 2 - 150, HEIGHT // 2 + 60), fontsize=30, color=WHITE)

    # Wait for SPACE key press to restart the game
    if keyboard.SPACE:
        restart_game()

# Function to restart the game
def restart_game():
    global score
    global lives
    global bullets
    global enemies

    score = 0
    lives = 3
    bullets = []
    enemies = []
    for _ in range(8):
        enemy = Actor('bug')
        enemy.x = random.randint(0, WIDTH - 80)
        enemy.y = random.randint(-100, 0)
        enemies.append(enemy)

pgzrun.go()