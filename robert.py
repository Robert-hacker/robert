import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Rex Tina Run')

pygame.mixer.music.load('Sounds/background.mp3')
pygame.mixer.music.set_volume(0.3)

jump_sound = pygame.mixer.Sound('Sounds/Rrr.wav')
fall_sound = pygame.mixer.Sound('Sounds/Bdish.wav')
loss_sound = pygame.mixer.Sound('Sounds/loss.wav')
heart_plus_sound = pygame.mixer.Sound('Sounds/hp+.wav')
button_sound = pygame.mixer.Sound('Sounds/button.wav')

cactus_img = [pygame.image.load('Objects/Cactus0.png'), pygame.image.load('Objects/Cactus1.png'), pygame.image.load('Objects/Cactus2.png')]
cactus_options = [69, 449, 37, 410, 40, 420]

stone_img = [pygame.image.load('Objects/Stone0.png'), pygame.image.load('Objects/Stone1.png')]
cloud_img = [pygame.image.load('Objects/Cloud0.png'), pygame.image.load('Objects/Cloud1.png')]

dino_img = [pygame.image.load('Dino/Dino0.png'), pygame.image.load('Dino/Dino1.png'), pygame.image.load('Dino/Dino2.png'),
			pygame.image.load('Dino/Dino3.png'), pygame.image.load('Dino/Dino4.png')]

health_img = pygame.image.load('Effects/heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

light_img =  [pygame.image.load('Effects/Light0.png'), pygame.image.load('Effects/Light1.png'), pygame.image.load('Effects/Light2.png'),
			  pygame.image.load('Effects/Light3.png'), pygame.image.load('Effects/Light4.png'), pygame.image.load('Effects/Light5.png'),
			  pygame.image.load('Effects/Light6.png'), pygame.image.load('Effects/Light7.png'), pygame.image.load('Effects/Light8.png'),
			  pygame.image.load('Effects/Light9.png'), pygame.image.load('Effects/Light10.png')]


img_counter = 0
health = 1



class Object:
	def __init__(self, x, y, width, image, speed):
		self.x = x
		self.y = y
		self.width = width
		self.image = image
		self.speed = speed

	def move(self):
		if self.x >= -self.width:
			display.blit(self.image, (self.x, self.y))
			#pygame.draw.rect(display, (224, 121, 31), (self.x, self.y, self.width, self.height))
			self.x -= self.speed
			return True
		else:
			#self.x = display_width + 100 + random.randrange(-80, 60)
			return False

	def return_self(self, radius, y, width, image):
		self.x = radius
		self.y = y
		self.width = width
		self.image = image
		display.blit(self.image, (self.x, self.y))

class Button:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.inactive_clr = (13, 162, 58)
		self.active_clr = (23, 204, 58)
		self.draw_effects = False
		self.rect_h = 10
		self.rect_w = width
		self.clear_effects = False

	def draw(self, x, y, message, action=None, font_size=30):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:

			if click[0] == 1:
				pygame.mixer.Sound.play(button_sound)
				pygame.time.delay(300)
				if action is not None:
					if action == quit:
						pygame.quit()
						quit()
					else:
						action()



		self.draw_beautiful_rect(mouse[0], mouse[1], x, y,)

		print_text(message=message, x=x+10, y=y+10, font_size=font_size)

	def draw_beautiful_rect(self, ms_x, ms_y, x, y):
		if x <= ms_x <= x + self.width and y <= ms_y <= y + self.height:
			self.draw_effects = True

		if self.draw_effects:
			if ms_x < x or ms_x > x + self.width or ms_y < y or ms_y > y + self.height:
					self.clear_effects = True
					self.draw_effects = False


			if self.rect_h < self.height:
				self.rect_h += (self.height - 10) / 40

		if self.clear_effects and not self.draw_effects:
			if self.rect_h > 10:
				self.rect_h -= (self.height - 10) / 40
			else:
				self.clear_effects = False


		draw_y = y + self.height - self.rect_h
		pygame.draw.rect(display, self.active_clr, (x, draw_y, self.rect_w, self.rect_h))


usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

cactus_width = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y =display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0

mouse_counter = 0
need_draw_click = False

def show_menu():
	menu_bckgr = pygame.image.load('Background/Menu.jpg')

	start_btn = Button(288, 90)
	quit_btn = Button(120, 90)

	show = True
	while show:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		display.blit(menu_bckgr, (0, 0))
		start_btn.draw(270, 200, 'Start game', start_game, 50)
		quit_btn.draw(358, 300, 'Quit', quit, 50)

		draw_mouse()

		pygame.display.update()
		clock.tick(60)

def start_game():
		global scores, make_jump, jump_counter, usr_y, health

		while game_cycle():
			scores = 0
			make_jump = False
			jump_counter = 30
			usr_y = display_height - usr_height - 100
			health = 1



def game_cycle():
	global make_jump

	pygame.mixer.music.play(-1)


	game = True
	cactus_arr = []
	create_cactus_arr(cactus_arr)
	land = pygame.image.load(r'Background/Land.jpg')

	stone, cloud = open_random_objects()
	heart = Object(display_width, 280, 30, health_img, 4)

	button = Button(100, 50)


	while game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()


		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			make_jump = True

		count_scores(cactus_arr)

		display.blit(land, (0, 0))
		print_text('Scores: ' + str(scores), 600, 10)

		button.draw(20, 100, 'wow')

		draw_array(cactus_arr)
		move_objects(stone, cloud)

		draw_dino()

		if keys[pygame.K_ESCAPE]:
			pause()

		if make_jump:
			jump()


		heart.move()
		hearts_plus(heart)

		if check_collision(cactus_arr):
			#pygame.mixer.music.stop()
			#pygame.mixer.Sound.play(fall_sound)
			#if not check_health():
			game = False

		show_health()

		draw_mouse()
		pygame.display.update()
		clock.tick(90)
	return game_over()


def jump():
	global usr_y, jump_counter, make_jump
	if jump_counter >= -30:
		if jump_counter == 30:
			pygame.mixer.Sound.play(jump_sound)
		if jump_counter == -10:
			pygame.mixer.Sound.play(fall_sound)

		usr_y -= jump_counter / 2.0
		jump_counter -= 1
	else:
		jump_counter = 30
		make_jump = False


def create_cactus_arr(array):
	choise = random.randrange(0, 3)
	img = cactus_img[choise]
	width = cactus_options[choise * 2]
	height = cactus_options[choise * 2 + 1]
	array.append(Object(display_width + 20, height, width, img, 4))

	choise = random.randrange(0, 3)
	img = cactus_img[choise]
	width = cactus_options[choise * 2]
	height = cactus_options[choise * 2 + 1]
	array.append(Object(display_width + 300, height, width, img, 4))

	choise = random.randrange(0, 3)
	img = cactus_img[choise]
	width = cactus_options[choise * 2]
	height = cactus_options[choise * 2 + 1]
	array.append(Object(display_width + 600,  height, width, img, 4))

def find_radius(array):
		maximum = max(array[0].x, array[1].x, array[2].x)

		if maximum < display_width:
			radius = display_width
			if radius - maximum < 50:
				radius += 280
		else:
			radius = maximum

		choise = random.randrange(0, 5)
		if choise == 0:
			radius += random.randrange(10, 15)
		else:
			radius += random.randrange(250, 400)

		return radius



def draw_array(array):
	for cactus in array:
		check = cactus.move()
		if not check:
			object_return(array, cactus)


def object_return(objects, obj):
	radius = find_radius(objects)

	choise = random.randrange(0, 3)
	img = cactus_img[choise]
	width = cactus_options[choise * 2]
	height = cactus_options[choise * 2 + 1]

	obj.return_self(radius, height, width, img)



def open_random_objects():
	choise = random.randrange(0, 2)
	img_of_stone = stone_img[choise]

	choise = random.randrange(0, 2)
	img_of_cloud = cloud_img[choise]

	stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
	cloud = Object(display_width,  80, 70, img_of_cloud, 2)

	return stone, cloud


def move_objects(stone, cloud):
	check = stone.move()
	if not check:
		choise = random.randrange(0, 2)
		img_of_stone = stone_img[choise]
		stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

	check = cloud.move()
	if not check:
		choise = random.randrange(0, 2)
		img_of_cloud = cloud_img[choise]
		cloud.return_self(display_width, random.randrange(10, 200), cloud.width, img_of_cloud)

def draw_dino():
	global img_counter
	if img_counter == 25:
		img_counter = 0

	display.blit(dino_img[img_counter // 5], (usr_x, usr_y))
	img_counter += 1

def print_text(message, x, y, font_color = (0, 0, 0), font_type='Effects/PingPong.ttf', font_size=30):
	font_type = pygame.font.Font(font_type, font_size)
	text = font_type.render(message, True, font_color)
	display.blit(text, (x, y))

def pause():
	paused = True

	pygame.mixer.music.pause()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		print_text('Pause. Press Enter to continue', 90, 180)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			paused = False

		pygame.display.update()
		clock.tick(15)

	pygame.mixer.music.unpause()

def check_collision(barriers):
	for barrier in barriers:
		if barrier.y == 449: # Маленький кактус
			if not make_jump:
				if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
					if check_health():
						object_return(barriers, barrier)
						return False
					else:
						return True

			elif jump_counter >= 0:
				if usr_y + usr_height - 5 >= barrier.y:
					if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
						if check_health():
							object_return(barriers, barrier)
							return False
						else:
							return True

			else:
				if usr_y + usr_height - 10 >= barrier.y:
					if barrier.x <= usr_x <= barrier.x + barrier.width:
						if check_health():
							object_return(barriers, barrier)
							return False
						else:
							return True

		else:
			if not make_jump:
				if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
					if check_health():
						object_return(barriers, barrier)
						return False
					else:
						return True

				elif jump_counter == 10:
					if usr_y + usr_height - 5 >= barrier.y:
						if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
							if check_health():
								object_return(barriers, barrier)
								return False
							else:
								return True
				elif jump_counter >= -1:
					if usr_y + usr_height - 5 >= barrier.y:
						if barrier.x <= usr_x + usr_width - 25 <= barrier.x + barrier.width:
							if check_health():
								object_return(barriers, barrier)
								return False
							else:
								return True
					else:
						if usr_y + usr_height - 10 >= barrier.y:
							if barrier.x <= usr_x + 5 <= barrier.x + barrier.width:
								if check_health():
									object_return(barriers, barrier)
									return False
								else:
									return True
	return False

def count_scores(barriers):
	global scores, max_above
	above_cactus = 0

	if -20 <= jump_counter < 25:
		for barrier in barriers:
			if usr_y + usr_height - 5 <= barrier.y:
				if barrier.x <= usr_x <= barrier.x + barrier.width:
					above_cactus += 1
				elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
					above_cactus += 1

		max_above = max(max_above, above_cactus)
	else:
		if jump_counter == -30:
			scores += max_above
			max_above = 0



def game_over():
	global scores, max_scores
	if scores > max_scores:
		max_scores = scores

	stopped = True
	while stopped:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		print_text('Game Over', 350, 200)
		print_text('Max scores: ' + str(max_scores), 540, 35)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			return True
		if keys[pygame.K_ESCAPE]:
			return False


		pygame.display.update()
		clock.tick(15)


def show_health():
	global health
	show = 0
	x = 20
	while show != health:
		display.blit(health_img, (x, 20))
		x += 40
		show += 1

def check_health():
	global health
	health -= 1
	if health == 0:
		pygame.mixer.Sound.play(loss_sound)
		return False
	else:
		pygame.mixer.Sound.play(fall_sound)
		return True

def hearts_plus(heart):
	global health, usr_x, usr_y, usr_width, usr_height

	if heart.x <= -heart.width:
		radius = display_width + random.randrange(3000, 9000)
		heart.return_self(radius, heart.y, heart.width, heart.image)



	if usr_x <= heart.x <= usr_x + usr_width:
		if usr_y <= heart.y <= usr_y + usr_height:
			pygame.mixer.Sound.play(heart_plus_sound)
			if health < 3:
				health += 1

			radius = display_width + random.randrange(3000, 9000)
			heart.return_self(radius, heart.y, heart.width, heart.image)

def draw_mouse():
	global mouse_counter, need_draw_click
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	mouse_size = [10, 12, 16, 20, 28, 34, 40, 45, 48, 54, 58]

	if click[0] or click [1]:
		need_draw_click = True

	if need_draw_click:
		draw_x = mouse[0] - mouse_size[mouse_counter] // 2
		draw_y = mouse[1] - mouse_size[mouse_counter] // 2

		display.blit(light_img[mouse_counter], (draw_x, draw_y))
		mouse_counter += 1


		if mouse_counter == 10:
			mouse_counter = 0
			need_draw_click = False



show_menu()
pygame.quit()
quit()
