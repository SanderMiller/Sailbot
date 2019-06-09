import math
import pygame, random
import numpy
import time
from pygame.math import Vector2



#Colors
GREEN = (20, 255, 140)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WATER = (68, 183, 255)
YELLOW = (255, 255, 63)
BLACK = (0, 0, 0)


realwindangle = random.randint(255, 295)

#Create Boat class as a sprite
class Boat(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((80,202), pygame.SRCALPHA)

        #Set and scale the sprite image
        picture = pygame.image.load("images/yellow_boat.png")
        boat_image = pygame.transform.scale(picture, (40, 100))
        self.image = boat_image
        self.rotated_image = self.image

        #Define properties of the Boat sprite
        self.rect = self.image.get_rect(center=(pos))
        self.pos = Vector2(pos)
        self.offset = Vector2(0, 0)
        self.angle = 270
        self.rotate()


    #rotate the sprite and equalize pos, image and rect
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.rotated_image, -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)

    def rotate_right(self):
        #Keep angle between 0 and 360
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        #Rotate Right
        self.angle += 1
        self.rotate()

    def rotate_left(self):
        #Keep angle between 0 and 360
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        #Rotate Left
        self.angle -= 1
        self.rotate()

    #respawn the boat
    def reset_boat(self):
        self.pos.x = 1700
        self.pos.y = 500
        self.angle = 270
        self.rotate()

    #Go forward
    def moveUp(self, pixels):
        #Don't move if pointed towards wind
        if realwindangle >=25 and realwindangle  <= 335:
            if self.angle > realwindangle - 25 and self.angle < realwindangle + 25:
                self.pos.y = self.pos.y
                self.pos.x = self.pos.x
                self.rect.y = self.rect.y
                self.rect.x = self.rect.x
                self.rect = self.image.get_rect(center=self.pos)
        #Move otherwise
            else:
                self.pos.y -= math.cos(math.radians(self.angle))*pixels
                self.pos.x += math.sin(math.radians(self.angle))*pixels
                self.rect.y -= math.cos(math.radians(self.angle))*pixels
                self.rect.x += math.sin(math.radians(self.angle))*pixels
                self.rect = self.image.get_rect(center=self.pos)
        elif realwindangle >=0 and realwindangle <= 25:
            if self.angle > 365 - abs(realwindangle - 25) or self.angle < realwindangle + 25:
                self.pos.y = self.pos.y
                self.pos.x = self.pos.x
                self.rect.y = self.rect.y
                self.rect.x = self.rect.x
                self.rect = self.image.get_rect(center=self.pos)
        #Move otherwise
            else:
                self.pos.y -= math.cos(math.radians(self.angle))*pixels
                self.pos.x += math.sin(math.radians(self.angle))*pixels
                self.rect.y -= math.cos(math.radians(self.angle))*pixels
                self.rect.x += math.sin(math.radians(self.angle))*pixels
                self.rect = self.image.get_rect(center=self.pos)

        elif realwindangle >=335:
            if self.angle > realwindangle - 25 or self.angle < realwindangle + 25- 365:
                self.pos.y = self.pos.y
                self.pos.x = self.pos.x
                self.rect.y = self.rect.y
                self.rect.x = self.rect.x
                self.rect = self.image.get_rect(center=self.pos)
        #Move otherwise
            else:
                self.pos.y -= math.cos(math.radians(self.angle))*pixels
                self.pos.x += math.sin(math.radians(self.angle))*pixels
                self.rect.y -= math.cos(math.radians(self.angle))*pixels
                self.rect.x += math.sin(math.radians(self.angle))*pixels
                self.rect = self.image.get_rect(center=self.pos)


pygame.init()



#Screen Properties
SCREENWIDTH=1850
SCREENHEIGHT=1000
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sailing Simulation")

#Make a sprites list and add Boat1
all_sprites_list = pygame.sprite.Group()
Boat1 = Boat((1700, 500))
all_sprites_list.add(Boat1)

#Initialize HUD: Text - Image on Screen
font = pygame.font.Font(None, 52)
small_font = pygame.font.Font(None, 42)
wind_direction = font.render("Wind Direction", 1, WHITE)
#Attribution for image below: http://www.pngall.com/?p=16293
compass = pygame.image.load("images/Compass_Image.png")
compass_scaled = pygame.transform.scale(compass, (250, 250))
wind_arrow = pygame.image.load("images/WindArrow.png")
rotated_wind_arrow = pygame.transform.rotozoom(wind_arrow, -realwindangle- 90 , 1)
buoy_warning = font.render("Don't hit the buoys!", 1, WHITE)
off_screen_warning = font.render("Don't go off screen", 1, WHITE)


#initialize global variables
currentBuoy = 0
speech_speed = 0.9
carryOn = True
testtime = 0
oldangle = realwindangle
deltaangle = 0
clock=pygame.time.Clock()
rudderStatus = 'Straight'

#Refreshes Screen
def update_screen():
    all_sprites_list.draw(screen)
    pygame.display.flip()
    #Set the frames per second to desired number
    clock.tick(60)

#Define functions that restart the boat with the correct warnings
def restart_boat_with_delay_hitted_buoy():
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    pygame.display.flip()
    time.sleep(1)



#GLOBAL REFERENCE FRAME VARIABLES
#-----------------------------------------------------------------------------------------------------------------------------------------------------

def windAngle():
    actualwindangle = random.randint(245, 295)
    return actualwindangle

def CalculatedGlobalWindAngle():
    #Calculate wind direction with respect to the global reference frame based on wind direction with respect to the boat
    CalcGlobalWindAngle = BoatHeading() + AngletoWind()
    if CalcGlobalWindAngle  > 360:
        CalcGlobalWindAngle -= 360 
    return CalcGlobalWindAngle

#Get Heading of the boat (given by compass)
def BoatHeading():
    boat_angle = Boat1.angle
    return boat_angle

#Distance to current buoy
def distance():
    #200 pixels representsent a 4.2 meter boat
    pixels_to_meters_rate = .021
    distance = round(math.sqrt(((Boat1.pos.x-BuoyPos[currentBuoy])**2)+(Boat1.pos.y-BuoyPos[currentBuoy+1])**2)*pixels_to_meters_rate)
    return distance

def GlobalAngle2Buoy():
    GlobalAngle2Buoy = BoatHeading() + AngletoBuoy()
    if GlobalAngle2Buoy >= 360:
        GlobalAngle2Buoy -= 360
    return GlobalAngle2Buoy
#-----------------------------------------------------------------------------------------------------------------------------------------------------


#LOCAL REFERENCE FRAME VARIABLES
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Angle to current buoy
def AngletoBuoy():
    BoatCartx = Boat1.pos.x
    BoatCarty = -(Boat1.pos.y - SCREENHEIGHT)
    BuoyCartx = BuoyPos[currentBuoy]
    BuoyCarty = -(BuoyPos[currentBuoy+1] - SCREENHEIGHT)
    v = (BuoyCartx - BoatCartx, BuoyCarty - BoatCarty)
    u = (math.sin(math.radians(BoatHeading())), math.cos(math.radians(Boat1.angle)))
    if numpy.cross(u,v) <= 0:
        if (numpy.dot(u, v)/(numpy.linalg.norm(u))) >= 0:
            Angle2Buoy = round(math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
        else:
            Angle2Buoy = round(math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
    elif numpy.cross(u,v) > 0:
        if (numpy.dot(u, v)/(numpy.linalg.norm(u))) >= 0:
            Angle2Buoy = round(360 - math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
        else:
            Angle2Buoy = round(360 - math.degrees(math.acos(numpy.dot(u, v)/(numpy.linalg.norm(u)*numpy.linalg.norm(v)))))
    return Angle2Buoy
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def get_distance_sentence():
    str_distance = str(distance())
    dist_sentence = "Buoy " + str_distance + " meters away"
    return dist_sentence 


def AngletoWind():
    windangle = realwindangle 
    boatheading = Boat1.angle
    Angle2Wind = windangle-boatheading
    if Angle2Wind < 0:
        Angle2Wind += 360
    return Angle2Wind

def SailPos():
    if AngletoWind() < 45 or AngletoWind() > 315:
        sailpos = 'Close Haul'
    if AngletoWind() >= 45 and AngletoWind() <= 90  or AngletoWind() <= 315 and AngletoWind()>= 270:
        sailpos = 'Close Reach'
    if AngletoWind() > 90 and AngletoWind() <= 135  or AngletoWind() < 270 and AngletoWind()>= 225:
        sailpos = 'Broad Reach'
    if AngletoWind() > 135 and AngletoWind() < 225 :
        sailpos = 'Down Wind'
    return  sailpos


def get_clock_heading_sentence():
    str_clock_heading = str(AngletoBuoy())
    heading_sentence = "Angle to Buoy: " + str_clock_heading
    return heading_sentence





#Main Loop
while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False

            #Pressing the x Key will quit the game
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x:
                     carryOn=False

                #Pressing 5 advances the current buoy
                if event.key == pygame.K_5:
                    if currentBuoy == 0:
                        currentBuoy += 2
                    elif currentBuoy == 2:
                        currentBuoy += 2
                    elif currentBuoy == 4:
                        currentBuoy = 0



        #Update Sprites
        all_sprites_list.update()
        screen.fill(WATER)
        
        time = round(pygame.time.get_ticks()/1000)

        
        if testtime != time and time % 5 ==0:

            testtime = time
            realwindangle =  windAngle()
            deltaangle = realwindangle - oldangle
            oldangle = realwindangle
            rotated_wind_arrow = pygame.transform.rotozoom(wind_arrow, -realwindangle- 90 , 1)
        #Draw The Buoys
        BuoyPos = [200, 550, 1500, 300, 1500, 800]
        radius = 30
        pygame.draw.circle(screen, RED, [BuoyPos[0],BuoyPos[1]],radius, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[2],BuoyPos[3]],radius, 0)
        pygame.draw.circle(screen, RED, [BuoyPos[4],BuoyPos[5]],radius, 0)
        #Make Current Buoy Green
        pygame.draw.circle(screen, GREEN, [BuoyPos[currentBuoy],BuoyPos[currentBuoy+1]],30, 0)


        #Collision Detection with Buoys
        if (BuoyPos[currentBuoy]-radius*1.5 < Boat1.pos.x < BuoyPos[currentBuoy]+radius*1.5) and (BuoyPos[currentBuoy+1]-radius*1.5 < Boat1.pos.y < BuoyPos[currentBuoy+1]+radius*1.5):
            if currentBuoy == 0:
                currentBuoy += 2
            elif currentBuoy == 2:
                currentBuoy += 2
            elif currentBuoy == 4:
                currentBuoy = 0
       


        #Head Up Display Text and Images to Display
        #Display distance to buoy
        distance_to_buoy = get_distance_sentence()
        distance_to_buoy_render = small_font.render(distance_to_buoy, 1, BLACK)
        screen.blit(distance_to_buoy_render, (850,925))

        #Display clock heading to buoy
        buoy_clock_pos = get_clock_heading_sentence()
        buoy_clock_pos_render = small_font.render(buoy_clock_pos, 1, BLACK)
        screen.blit(buoy_clock_pos_render, (1200,925))

        #Display boat heading as cardinal direction
        boat_cardinal_heading = str(BoatHeading())
        boat_cardinal_heading_render = small_font.render('Boat Heading: '+boat_cardinal_heading, 1, BLACK)
        screen.blit(boat_cardinal_heading_render, (1500,925))

         #Display boat heading as cardinal direction
        ang2wind = str(AngletoWind())
        boat_cardinal_heading_render = small_font.render('Wind Vane Reading: '+ang2wind, 1, WHITE)
        screen.blit(boat_cardinal_heading_render, (100,925))

         #Display boat heading as cardinal direction
        ang2buoy = str(GlobalAngle2Buoy())
        boat_cardinal_heading_render = small_font.render('Global Angle to Buoy: '+ang2buoy, 2, BLACK)
        screen.blit(boat_cardinal_heading_render, (450,925))
        
         #Display boat heading as cardinal direction
        ang2buoy = str(SailPos())
        boat_cardinal_heading_render = small_font.render('Sail Position: '+ang2buoy, 1, WHITE)
        screen.blit(boat_cardinal_heading_render, (100,775))
        

          #Display boat heading as cardinal direction
        ang2buoy = str(CalculatedGlobalWindAngle())
        boat_cardinal_heading_render = small_font.render('Calculated Global Wind Angle: '+ang2buoy, 1, BLACK)
        screen.blit(boat_cardinal_heading_render, (100,875))

          #Display boat heading as cardinal direction
        boat_cardinal_heading_render = small_font.render('Rudder Status: ' + rudderStatus, 1, WHITE)
        screen.blit(boat_cardinal_heading_render, (100,825))

        #Display other images & text on screen
        screen.blit(wind_direction, (50,50))
        screen.blit(rotated_wind_arrow, (50,100))
        screen.blit(compass_scaled, (1575,25))

        rudderStatus = 'Straight'
        if abs(GlobalAngle2Buoy() - CalculatedGlobalWindAngle()) < 25:
            if AngletoWind() <= 24 and AngletoWind() >= 0:
                 Boat1.rotate_left()
                 rudderStatus = 'Turning Left'
            if AngletoWind() <= 180 and AngletoWind() >= 26:
                 Boat1.rotate_right()
                 rudderStatus = 'Turning Right'
            if AngletoWind() <= 360 and AngletoWind() >= 336:
                 Boat1.rotate_right()
                 rudderStatus = 'Turning Right'
            if AngletoWind() <= 334 and AngletoWind() > 180:
                 Boat1.rotate_left()
                 rudderStatus = 'Turning Left'

        else:
            if AngletoBuoy()>=1 and AngletoBuoy()<=180:
                Boat1.rotate_right()
                rudderStatus = 'Turning Right'
            if AngletoBuoy()>180 and AngletoBuoy()<=359:
                Boat1.rotate_left()
                rudderStatus = 'Turning Left'
        
        
        #Controls of Boat
        Boat1.moveUp(1)
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            Boat1.rotate_right()
        if keys[pygame.K_LEFT]:
            Boat1.rotate_left()
        
        if AngletoBuoy()>=1 and AngletoBuoy()<=180:
            Boat1.rotate_right()
        if AngletoBuoy()>180 and AngletoBuoy()<=359:
            Boat1.rotate_left()
        '''
        #Refresh Screen
        update_screen()


pygame.quit()