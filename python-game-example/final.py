# Importing libraries that we'll be using
import pygame
import sys
import random
import math

# Initializing pygame
pygame.init()

# These set us up to be able to use text and timers later
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Defining the window we will display our game on (in terms of pixels)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hungry Monkey Hunting Season')

#GLOBAL VARIABLES
platform_width = 128
platform_height = 10
platform_list = []
#Here's where we import the pixel art for our leafy platforms.
#You can also import any image from your computer by instead typing in
#your computer's path to that file, e.g. (f"/path/to/file_name.png)
platform_img = pygame.image.load(f"hungry_monkey_sprites/7tree_top_sprite.png")
num_platforms = 8

#We can use pygame.Rect to make a invisible rectangular object 
#to detect things like collisions
#It follows the format: pygame.Rect(<topleft_x>,<topleft_y>,<width>,<height>)
floor = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)


monkey_x = int(SCREEN_WIDTH / 2)
monkey_y = SCREEN_HEIGHT - 100
gravity = 1
ogOrb = pygame.image.load(f"game_sprites/magicOrb.png")
velocity_y = 0
monkey_size = 50
jump_power = -14
monkey = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)
is_jumping = False
monkey_img = pygame.image.load(f"hungry_monkey_sprites/2monkey_f1.png")
orb_x = random.randint(-300, 200)
orb_y = random.randint(-300, 200)
orb_img = pygame.transform.scale(ogOrb, (0.0001, 0.0001))
velocity_y = 0
monkey_size = 50
jump_power = -14
monkey = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)
is_jumping = False
monkey_img = pygame.image.load(f"hungry_monkey_sprites/2monkey_f1.png")
opp_x=0
opp_y=0
opp_dx=0
opp_dy=0
distance = 0
scoreT = 0

frame = 0
frames_left = 1000 #How many frames are left before game over

score = 0
top_score = 0
#The banana will be our player's goal
banana_x, banana_y = int(SCREEN_WIDTH / 2), 50
banana = pygame.Rect(banana_x,banana_y, 50, 50)

orb = pygame.Rect(orb_x, orb_y, 20, 20)
attempt_shoot_index = 0

#Some RGB values we might want to use
DARK_GREEN = (0, 150, 0)
SKY_BLUE = (105, 186, 255)
WHITE = (255,255,255)

def draw_setting():
    """Draws background, platforms, floor, and banana onto our screen"""
    # For each new frame, we want to redraw our background over the previous frame
    pygame.draw.rect(screen, SKY_BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    for platform in platform_list:
        # screen.blit is how you draw one surface (like images) onto another (like our window)
        screen.blit(platform_img, platform)

    # Drawing the floor
    pygame.draw.rect(screen, DARK_GREEN, floor)

    # Drawing banana        
    if len(platform_list) == num_platforms:
        banana_img = pygame.image.load(f"hungry_monkey_sprites/1banana_sprite.png")
        screen.blit(banana_img, (banana_x,banana_y))
        orb_img = pygame.image.load(f"game_sprites/magicOrb.png")
        screen.blit(orb_img, (orb_x, orb_y))

    # Drawing score
    score_txt = font.render(f"Banana Score: {score}", True, (255,255,255))
    screen.blit(score_txt, (10, 10))
	
def update_monkey():
	"""Control monkey's movement and image, and detect collisions with platforms and banana"""
	#Globals allow us to edit variable that exist outside of this function
	global monkey_x, monkey_y, velocity_y, monkey, monkey_img, platform_list,score, attempt_shoot_index, opp_x, opp_y, opp_dx, opp_dy, distance, bullet, scoreT

	

	#Constantly applying gravity to monkey
	velocity_y += gravity
	monkey_y += velocity_y

	#Here's how you detect keystrokes:
	key_pressed = pygame.key.get_pressed()
	if key_pressed[pygame.K_a]:
		monkey_x -= 5
	elif key_pressed[pygame.K_d]:
		monkey_x += 5
	#Update monkey's x and y coordinates
	monkey = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)

	#Check if monkey is on a platform
	for platform in platform_list:
		if monkey.colliderect(platform) and velocity_y > 0:
			monkey_y = platform[1] - monkey_size #platform[1] stores the platform's y coordinate
			velocity_y = 0
			if (key_pressed[pygame.K_SPACE] or key_pressed[pygame.K_w]): #Monkey can only jump when standing on something
				velocity_y = jump_power
	if monkey.colliderect(floor):
		monkey_y = floor[1] - monkey_size
		velocity_y = 0
		if (key_pressed[pygame.K_SPACE] or key_pressed[pygame.K_w]):
			velocity_y = jump_power
		#Generate new platforms every time the ground is touched (won't generate if there are enough platforms)
		generate_platforms()

	#Animate the monkey
	global frame
	sprite_frame = int((frame / 5) % 4) + 1
	if len(platform_list) == num_platforms:  # Whenever platforms are all generated, play the animation
		if sprite_frame == 1:
			current_sprite = f"hungry_monkey_sprites/2monkey_f1.png"
		elif sprite_frame == 2:
			current_sprite = f"hungry_monkey_sprites/0monkey_f2.png"
		elif sprite_frame == 3:
			current_sprite = f"hungry_monkey_sprites/3monkey_f3.png"
		else:
			current_sprite = f"hungry_monkey_sprites/4monkey_f4.png"
		monkey_img = pygame.image.load(current_sprite)
	if velocity_y < 0 and len(platform_list) == num_platforms: #Jumping sprite
		monkey_img = pygame.image.load(f"hungry_monkey_sprites/6monkey_jump_sprite.png")
	# Detect banana collision
	if monkey.colliderect(banana) and len(platform_list) == num_platforms:
		global top_score, frames_left, score
		platform_list = []
		monkey_img = pygame.image.load(f"hungry_monkey_sprites/5monkey_happy.png")
		score += 1
		frames_left += 50

	#Draw monkey onto screen
	screen.blit(monkey_img, (monkey_x, monkey_y))    

def game_over_display():
    """Displays game stats whenever time runs out"""
    global score

    screen.fill(SKY_BLUE)
    game_over_txt = font.render("Game Over", True, WHITE)
    score_txt = font.render(f"Your score was: {score}", True, WHITE)
    top_score_txt = font.render(f"The high score is: {top_score}",True,WHITE)
    restart_txt = font.render("Press R to restart, or Q to quit",True, WHITE)
    theme_txt = font.render("the enemey is envy. Envy is within us...our own enemy", True, WHITE)

    #Draw the above text onto the screen
    screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(top_score_txt, (SCREEN_WIDTH // 2 - top_score_txt.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(theme_txt, (SCREEN_WIDTH // 2 - theme_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.display.update()

	# Wait for restart or quit input
    input_waiting = True
    while input_waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Press R to restart
                    input_waiting = False
                    game_loop() # Restart the game
                elif event.key == pygame.K_q: # Press Q to quit
                    pygame.quit()
                    sys.exit()

def advance_timer():
	"""Every frame, reduce the time left for the game and display this change"""
	global top_score, frames_left, scoreT

	frames_left -= 1

	if score - scoreT ==1:
		frames_left += 100
		scoreT = score
	timer_txt = font.render(f"Time left: {frames_left}", True, (255, 255, 255))
	screen.blit(timer_txt, (10, 60))

	#Check if the timer has run out, meaning the game is over
	if frames_left <= 0:
		if score > top_score:
			top_score = score
		game_over_display()

def generate_platforms():
	"""Whenever there are fewer platforms than desired num_platforms, generate new random ones"""
	current_platform_count = len(platform_list)
	while current_platform_count < num_platforms:
		platform_x = (random.randint(0, SCREEN_WIDTH - platform_width)) #random.randint(a,b) generate a random integer between a and b
		platform_y = (random.randint(80 + (current_platform_count * (SCREEN_HEIGHT - 80) // num_platforms),(80 + (current_platform_count + 1) * (SCREEN_HEIGHT - 80) // num_platforms)))
		#Create new rectangles for these platforms, and store them in platform_list
		platform_list.append(pygame.Rect(platform_x, platform_y, platform_width, platform_height))

		current_platform_count += 1

def reset_variables():
	"""Every time the game_loop is rerun, reset relevant variables"""
	global frames_left, score, platform_list, monkey_x, monkey_y

	frames_left = 1000
	score = 0
	platform_list = []
	generate_platforms()
	monkey_x = int(SCREEN_WIDTH / 2)
	monkey_y = SCREEN_HEIGHT - 100

class Envy(pygame.sprite.Sprite):
	def __init__(self, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('game_sprites/enemy.png')
		self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self):
		screen.blit(self.image, self.rect)

def game_loop():
	"""This function runs our main game loop, yippie!"""
	global frame
  
	reset_variables()
	running = True
	while running:
		#Here is an instance of event handling, checking if the user wants to exit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()

		draw_setting() #Drawing floor, platforms, and banana
		update_monkey() #Let's allow our monkey to move and collide with things
		advance_timer() #Progress the game timer and check if it's run out
		try_shoot()
		bullet_check()
		envy = Envy(enem_x, enem_y, 4)
		envy.draw()

		# Now that we've made our changes to the frame, let's update the screen to reflect those changes:
		pygame.display.update()
		clock.tick(30) #This functions helps us cap the FPS (Frames per Second)
		frame += 1 #We use this frame variable to animate our monkey


# Global variables to track the red square's position and status
red_square_active = False
red_square_position = (0, 0)
red_square_timer = 0

def try_shoot():  # Try to shoot from a random position
    global attempt_shoot_index, red_square_active, red_square_position, red_square_timer, enemy_rect
    global opp_x, opp_y, opp_dx, opp_dy, distance, enem_x, enem_y

    # Check if we need to generate a new red square
    if not red_square_active:
        attempt_shoot_index += 1
        if attempt_shoot_index % 10 == 1:
            # Load the image and scale it to larger dimensions
            opp_img = pygame.image.load(f"game_sprites/bullet.png")
            larger_opp_img = pygame.transform.scale(opp_img, (50, 30))  # Larger size (50x30)

            # Generate a random position and activate the red square
            opp_x = random.randint(0, SCREEN_WIDTH - 50)  # Ensure it fits within the screen
            opp_y = random.randint(0, SCREEN_HEIGHT - 30)
            enem_x = opp_x
            enem_y = opp_y
            enemy_rect = pygame.Rect(opp_x, opp_y, 50, 30)
            red_square_position = (opp_x, opp_y)
            red_square_active = True
            red_square_timer = 100  # Red square stays active for 100 frames

            # Calculate the difference in positions
            opp_dx = monkey_x - opp_x
            opp_dy = monkey_y - opp_y
            distance = math.sqrt(opp_dx**2 + opp_dy**2)  # Calculate distance once
    else:
        # Move the red square towards the monkey at a constant speed
        if distance != 0:
            speed = 10  # Adjust speed as needed
            opp_x += opp_dx / distance * speed
            opp_y += opp_dy / distance * speed

        # Draw the larger red square (bullet)
        opp_img = pygame.image.load(f"game_sprites/bullet.png")
        larger_opp_img = pygame.transform.scale(opp_img, (50, 30))  # Larger size
        red_square_position = (opp_x, opp_y)
        screen.blit(larger_opp_img, red_square_position)

        # Decrement the timer and deactivate the square if time runs out
        red_square_timer -= 1
        if red_square_timer <= 0:
            red_square_active = False


def bullet_check():
    # Larger bullet dimensions
    bullet_width, bullet_height = 50, 30  # Bigger size
    bullet = pygame.Rect(opp_x, opp_y, bullet_width, bullet_height)

    # Check collision between the monkey and the bullet
    if monkey.colliderect(bullet):
        game_over_display()

def bullet_check():
    # Larger and faster bullet
    bullet_width, bullet_height = 20, 10  # Increased size
    bullet = pygame.Rect(opp_x, opp_y, bullet_width, bullet_height)

    # Check collision between the monkey and the bullet
    if monkey.colliderect(bullet):
        game_over_display()

def bullet_check():
	bullet = pygame.Rect(opp_x, opp_y, 14, 7)
	if monkey.colliderect(bullet):
		game_over_display()

game_loop()