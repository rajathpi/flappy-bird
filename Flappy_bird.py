import pygame
import neat
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

#BIRD_IMGS stores the 3 images of the bird
#transform.scale2x is used to scale the image so that it is easier to see
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird1.png")  )) ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

class Bird:
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25		#Angle we rotate the image to make it point the direction the bird is moving
	ROT_VEL = 20			#Rotation veloctiy
	ANIMATION_TIME = 5		#how long we show each bird animation

	def __init__(self, x, y):	#x and y gives us the starting position of the bird
		self.x = x
		self.y = y
		self.tilt = 0			
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0] #referencing the 1st bird image

	def jump(self):
		self.vel = -10.5	#-ve vel because pygame starts from the top left corner of the screen with (0,0), so -10.5 seems to put the bird at the center of the screen
		self.tick_count = 0 #keeps track of when we last jump
		self.height = self.y #keeps track of where we it jumped from or from where it started moving

	def move(self):
		self.tick_count += 1 #keeping count of the number of frames we passed by, number of seconds that we were there in the game

		d =  self.vel*self.tick_count + 1.5*self.tick_count**2 	#how many pixels we move up or down, this is what we actually change when we move the y position of the bird
		#as soon as we jump we setup the tick_count to 0
		#when tick becomes 1, we have 
		# 	-10.5+ 1.5 = -9  which  is where are moving 9 pixels upwards.

		if d >= 16: #if moving more than 16 pixels, just bring it back to 16 pixels
			d = 16

		if d < 0: #making it jump 
			d -= 2

		self.y = self.y + d #adding the position to out y dir so we move either up or down

		#every time we jump we keep track of where we jump from

		#we will write a function to tilt the bird
		#if the bird is above the starting point then we just make it look like its moving upwards
		#if the bird is below the starting point then we make the bird facing downwards so that it feels like it too
		if d < 0 or self.y < self.height + 50: #tilting the bird upwards
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION #immediately rotating the bird by 25 degrees
		else: # we tilt the bird downwards
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL

	def draw(self, win):
		self.img_count += 1

		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0

		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2

		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
		win.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

#blit is used to draw, it draws whatever is put on the window
def draw_window(win, bird):
	win.blit(BG_IMG, (0,0))
	bird.draw(win)
	pygame.display.update()


def main():
	bird = Bird(200,200)
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	#clock = pygame.time.Clock()

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run  = False

		#bird.move()
		draw_window(win, bird)

	pygame.quit()
	quit()

main()