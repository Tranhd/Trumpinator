import pygame
from PIL import Image
import time 
import random
import os
import imageio


pygame.init()

display_width = 800
display_height = 600

black = (0,0,0) # RGB color for black.
white = (255,255,255) # RGB color for white. 
red = (255,0,0) # RGB color for red
gameDisplay = pygame.display.set_mode((display_width,display_height)) # set the width and height of the game.
pygame.display.set_caption('Trumpinator2000') # Set the title of the window (the game).

clock = pygame.time.Clock() # Initiate the clock.

# To display score
def score(count):
    font = pygame.font.SysFont(None, 25) # Set font and size.
    text = font.render("#Trumps Dodged " + str(count), True, black) # Text
    gameDisplay.blit(text, [3,3]) # Display in left top corner

# Draw car
def car(x,y):
    gameDisplay.blit(carImage, (x,y)) # Draws the carImage to the display.


def crash(): # Crash handler
    message_display('You got TRUMPINATED', sleep = 0) # Show text
    trumpinator = loadimage('Trumpinator.png', 400) # Load trumpinator image
    gameDisplay.blit(trumpinator, (300,50)) # Draw trumpintor
    for _ in range(1,50):
        updatedisplay(screen = False) # Update display.
    time.sleep(5) # Sleep 5 seconds
    gameDisplay.blit(trumpinator, (-800,-800)) # Remove trumpinator
    
def message_display(text, sleep = 2): # To display text
    largeText = pygame.font.Font('freesansbold.ttf', 40) # Set font and size.
    textSurf, textRect = text_objects(text, largeText) # Create text- surface and rectangel.
    textRect.center = ((display_width/2), (display_height/2)) # Where to put text.
    gameDisplay.blit(textSurf, textRect) # Draw message.
    updatedisplay(screen = False) # Update display.
    time.sleep(sleep) # Wait sleep seconds.
    
def text_objects(text, font):
    textSurf = font.render(text, True, red)
    return textSurf, textSurf.get_rect()

def things(thingx, thingy, thingw, thingh, color): # Obstacles
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh]) # Draw box to screen.

def updatedisplay(screen = False): # Update display
    pygame.display.update()
    if screen:
        if not hasattr(updatedisplay, "counter"):
            updatedisplay.counter = 0 
        pygame.image.save(gameDisplay, "screenshots/screenshot" + str(updatedisplay.counter) + ".jpeg")
        updatedisplay.counter +=1

# Draw trump at x,y
def trump(x,y):
    gameDisplay.blit(trumpImage, (x,y))
    
# Initiate the game
def game_init():
    x = (display_width * 0.45) # x coordinate for car image, referenced from top-left so use 0.45 to get middle.
    y = (display_height * 0.8) # y coordinate for car image, referenced from top left so use 0.8 to get bottom.
    x_change = 0 # Initial offset of car.
    gameExit = False # Game is not done.
    dodged = 0 # No obstacles have been dodged.
    return x, y, x_change, gameExit, dodged

def obstacle_init(startgame):
    thing_startx = random.randrange(0, display_width) # Start x-coordinate    
    thing_starty = -600 if startgame else -100 # Initialy of the screen
    thing_speed = 7 # How fast the obstacles will be
    thing_width = 100
    thing_height = 100
    return thing_startx, thing_starty, thing_speed, thing_width, thing_height

# Initiate the trump.
def trump_init(startgame, speed = 15):
    thing_startx = random.randrange(0, display_width) # Start x-coordinate    
    thing_starty = -600 if startgame else -70 # Initialy of the screen, closer if in-game.
    thing_speed = speed # How fast the obstacles will be, standard is 10 pixels per frame.
    return thing_startx, thing_starty, thing_speed

# Function to load an image.
def loadimage(path, basewidth):
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pygame.image.fromstring(data, size, mode)

def writegif():
    filenames = ['screenshots/screenshot' + str(i) +'.jpeg'  for i in range(200, len(os.listdir('screenshots/'))-1)]
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('demo.gif', images)
    print(filename)
    
carImage = loadimage('Car.png', 50) # Load the car image.
trumpImage = loadimage('Trump.png', 100) # Load the trump image.

trumpwidth = trumpImage.get_width()
trumpheight = trumpImage.get_height() - 30
carWidth = carImage.get_width()

# Main game loop.
def game_loop():

    x, y, x_change, gameExit, dodged = game_init() # Initial game-state
    thing_startx, thing_starty, thing_speed = trump_init(True) # Initiate trump
    
    while not gameExit: # While user have not exited.
        for event in pygame.event.get(): # Get all events.
            if event.type == pygame.QUIT: # Does the user want to quit?
                gameExit = True # Break loop
                break
            if event.type == pygame.MOUSEBUTTONDOWN: # Did a key get pressed?
                if event.button == 1: # Left mouse -> Change location of car to left.
                    x_change = -15
                elif event.button == 3: # Right mouse -> Change location of car to left.
                    x_change = 15
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3: # Stop moving when button released.
                    x_change = 0

        x += x_change # Change location of car.
        gameDisplay.fill(white) # Set background color. 
        
        trump(thing_startx, thing_starty) # Draw the trump
        thing_starty += thing_speed # Move obstacle
        car(x,y) # Show car. 
        score(dodged)
        
        if x + carWidth  > display_width or x < 0: # We have crashed into the sides.
            crash() # We have crashed.
            x, y, x_change, gameExit, dodged = game_init() # Reset game state.
        
        if thing_starty > display_height: # The trump has been dodged.
            if dodged % 3 == 0: # increase speed of trumps once in a while.
                speed = thing_speed + dodged
                
            thing_startx, thing_starty, thing_speed = trump_init(False, speed = speed) # Create new trump.
            dodged += 1 # Increase score.
    
        # If we crashed into an trump.            
        if y < thing_starty + trumpheight and y + carWidth/2 < thing_starty + trumpheight: 
            if abs((x + carWidth/2) - (thing_startx + trumpwidth/2)) < trumpwidth-50:
                crash() 
                thing_startx, thing_starty, thing_speed = trump_init(True) # Create ner trump, new game version.
                x, y, x_change, gameExit, dodged = game_init()  # Initiate new game
        
        updatedisplay(screen = False) # Update the display.
        clock.tick(60) # The frames per second.

game_loop() # Call main game loop
pygame.quit()
#writegif()
quit()

