import mediapipe
import cv2
from math import sqrt
import pygame
import sys
import numpy
import time

pygame.init()
clock=pygame.time.Clock()

window_size = (1080, 720)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('shitty ass keyboard')


running = True
counter = 0
total_blinks = 0

displayfont = cv2.FONT_HERSHEY_SIMPLEX


left_eye = [ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
right_eye = [ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]

mediapipe_face_mesh = mediapipe.solutions.face_mesh
face_mesh = mediapipe_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence =0.6, min_tracking_confidence=0.7)

video_capture = cv2.VideoCapture(0)

def landmarksDetection(image, results, draw=False):
    image_height, image_width= image.shape[:2]
    mesh_coordinates = [(int(point.x * image_width), int(point.y * image_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw :
        [cv2.circle(image, i, 2, (0, 255, 0), -1) for i in mesh_coordinates]
    return mesh_coordinates

# Euclaidean distance to calculate the distance between the two points
def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

# Blinking Ratio
def blinkRatio(image, landmarks, right_indices, left_indices):

    right_eye_landmark1 = landmarks[right_indices[0]]
    right_eye_landmark2 = landmarks[right_indices[8]]

    right_eye_landmark3 = landmarks[right_indices[12]]
    right_eye_landmark4 = landmarks[right_indices[4]]

    left_eye_landmark1 = landmarks[left_indices[0]]
    left_eye_landmark2 = landmarks[left_indices[8]]

    left_eye_landmark3 = landmarks[left_indices[12]]
    left_eye_landmark4 = landmarks[left_indices[4]]

    right_eye_horizontal_distance = euclaideanDistance(right_eye_landmark1, right_eye_landmark2)
    right_eye_vertical_distance = euclaideanDistance(right_eye_landmark3, right_eye_landmark4)

    left_eye_vertical_distance = euclaideanDistance(left_eye_landmark3, left_eye_landmark4)
    left_eye_horizobtal_distance = euclaideanDistance(left_eye_landmark1, left_eye_landmark2)

    right_eye_ratio = right_eye_horizontal_distance/right_eye_vertical_distance
    left_eye_ratio = left_eye_horizobtal_distance/left_eye_vertical_distance

    eyes_ratio = (right_eye_ratio+left_eye_ratio)/2

    return eyes_ratio







fontsize = 40
font = pygame.font.Font("PermanentMarker-Regular.ttf", fontsize)
keysize = (80,80)


boxshadow = pygame.Surface((window_size[0]-20,200))
boxshadow.fill((100,100,100,255))


boxsurface = pygame.Surface((window_size[0]-20, 200))
boxsurface.fill("white")


boxrect = boxsurface.get_rect()
boxrect.topleft = (10,5)

finaltext=""
outtext = font.render(finaltext, True, (0,0,0))
outrect = outtext.get_rect(topleft=(20,20))


class Button():
	def __init__(self, pos, key,size):
		self.key=key
		self.surface = pygame.image.load("key.png")
		self.rect = self.surface.get_rect()
		self.rect.topleft = pos
		self.text = font.render(key, True, (0, 0, 0))
		self.text_rect = self.text.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

		self.shadow = pygame.image.load("key.png")
		self.shadow = pygame.transform.scale_by(self.shadow, 1.3)
		self.shadow.fill(pygame.Color(100,100,100,255))

	def check_click(self, mpos):
		if self.rect.collidepoint(event.pos):
			return True

	def update(self):
		screen.blit(self.shadow, (self.rect.x, self.rect.y))
		self.surface.blit(self.text, self.text_rect)
		screen.blit(self.surface,self.rect.topleft)
		'''
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.surface.fill("grey")
		else:
			self.surface.fill("white")'''

class Blinker():
	def __init__(self):
		self.surface = pygame.Surface((3,fontsize))
		self.color1 = "black"
		self.color2 = "white"
		self.surface.fill(self.color1)

	def passed(self):
		self.surface.fill(self.color2)

	def draw(self, surf, pos):
		surf.blit(self.surface, pos)


Alphabet = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"," "]

r1 = []
r2 = []
r3 = []
space = None
backspace = None


blinker = Blinker()

e=7

for index, key in enumerate(Alphabet):
	if index<=9:
		ky = window_size[1]-4*keysize[0]-e*4
		kx = keysize[0] + (keysize[0]+e)*index

		backspace = Button((keysize[0] + (keysize[0]+e)*10, ky), "<-", keysize)
		r1.append(Button((kx,ky),key,keysize))

	elif index <=18:
		ky = window_size[1]-3*keysize[0]-e*3
		kx = keysize[0]*1.5 + (keysize[0]+e)*(index%10)
		r2.append(Button((kx,ky),key,keysize))

	elif index <=25:
		ky = window_size[1]-2*keysize[0]-e*2
		kx = keysize[0]*2.5+e+ (keysize[0]+e)*(index%19)
		r3.append(Button((kx,ky),key,keysize))

	elif index == 26:
		kx = 11*(keysize[0]+e)/3
		ky = window_size[1]-keysize[0]-e

		space = Button((kx,ky),key,(keysize[0]*6,keysize[0]))
		space.shadow = pygame.image.load("spacekey.png")
		space.shadow = pygame.transform.scale_by(space.shadow, 1.1)
		space.shadow.fill(pygame.Color(100,100,100,255))
		screen.blit(space.shadow, (space.rect.x, space.rect.y))

		space.surface = pygame.image.load("spacekey.png")
		space.rect = space.surface.get_rect()
		space.rect.topleft=(kx,ky)

keys = r1
keys.append(backspace)
keys = keys + r2 + r3
keys.append(space)

currentkey = keys[0]

fps =0
count=0
while running:
	ret, frame = video_capture.read()
	#frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
	frame_height, frame_width= frame.shape[:2]
	#rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
	results  = face_mesh.process(frame)


	clock.tick(60)
	screen.fill((169, 221, 232))
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for key in keys:
				if key.check_click(event.pos):
					if key.key == "<-":
						finaltext = finaltext[:-1]
					else:
						finaltext += key.key


	for key in keys:
		key.update()
	
	currentkey = keys[count]
	currentkey.shadow.fill("black")
	fps+=1
	
	
	if fps==60*0.2:
		blinker.surface.fill(blinker.color2)
		
	if fps==60*0.5:
		blinker.surface.fill("black")
		currentkey.shadow.fill((100,100,100))
		fps=0
		count+=1
		if count==len(Alphabet)+1:
			count=0
	if results.multi_face_landmarks:
		mesh_coordinatess = landmarksDetection(frame, results, True)

		eyes_ratio = blinkRatio(frame, mesh_coordinatess, right_eye, left_eye)

		#cv2.putText(frame, "Please blink your eyes",(int(frame_height/2), 100), displayfont, 1, (0, 255, 0), 2)

		if eyes_ratio > 3.8:
			counter +=1
		elif counter > 11:
			total_blinks +=1
			if currentkey.key == "<-":
				finaltext = finaltext[:-1]
			else:
				finaltext += currentkey.key
			counter =0
		#cv2.rectangle(frame, (20, 120), (290, 160), (0,0,0), -1)
		#cv2.putText(frame, f'Total Blinks: {total_blinks}',(30, 150), displayfont, 1, (0, 255, 0), 2)



	

	
	boxsurface.fill("white")
	
	outtext= font.render(finaltext, True, (0,0,0))
	outrect= outtext.get_rect(topleft=(20,20))

	blinker.draw(boxsurface,(outrect.right+2, outrect.y+outrect.height/4))


	boxsurface.blit(outtext, outrect)
	screen.blit(boxshadow, (boxrect.x, boxrect.y+30))
	screen.blit(boxsurface,boxrect.topleft)

	pygame.display.update()
	#cv2.imshow('Liveness Detection', frame)
	if cv2.waitKey(2) == 27:
		break



pygame.quit()
sys.exit()
cv2.destroyAllWindows()
video_capture.release()