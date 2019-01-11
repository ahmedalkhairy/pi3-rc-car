
import sys, tty, termios, time
from gpiozero import Motor
from gpiozero import LED
from gpiozero import DistanceSensor
from multiprocessing import Process
import threading

motorfb = Motor(forward=8, backward=7)
motorrl = Motor(forward=10, backward=9)
rled = LED(17)
lled = LED(27)
global speed
global exits
speed=0.4

#ultrasonic = DistanceSensor(echo=21, trigger=20, threshold_distance=0.2)

def getch():
    import sys, tty, termios, time

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def forward(speed0):
   print(speed0)
   motorfb.forward(speed0)
 


def backward(speed0):
    print(speed0)
    motorfb.backward(speed0)


def right():
  motorrl.forward()


def left():
    motorrl.backward()
  
    
def stopmv():
    motorfb.stop()

    
def stopmv_ultra():
    if(statuss !='stop'):
        satuss='stop'
        motorfb.stop()

    

def toggleLights():

    global lightStatus

    if(lightStatus == False):
        rled.on()
        lled.on()
        lightStatus = True
    else:
        rled.off()
        lled.off()
        lightStatus = False


def toggleSteering(direction):

    global wheelStatus

    if(direction == "right"):
        if(wheelStatus == "centre"):
            right()
            wheelStatus = "right"
        elif(wheelStatus == "left"):
            motorrl.stop()
            wheelStatus = "centre"

    if(direction == "left"):
        if(wheelStatus == "centre"):
            motorrl.stop()
            left()
       
            wheelStatus = "left"
        elif(wheelStatus == "right"):
            motorrl.stop()
            wheelStatus = "centre"
            
            
def move(direction,speed_in):

    global statuss

    if(direction == "forward"):
        if(statuss == "stop"):
            forward(speed_in)
            statuss = "forward"
        elif(statuss == "backward"):
            motorfb.stop()
            statuss = "stop"

    if(direction == "backward"):
        if(statuss == "stop"):
            backward(speed_in)
       
            statuss = "backward"
        elif(statuss == "forward"):
            motorfb.stop()
            statuss = "stop"


# Global variables for the status of the lights and steering
lightStatus = False
wheelStatus = "centre"
statuss="stop"
speed=0.5


exits=False

# Instructions for when the user has an interface
print("w/s: acceleration")
print("a/d: steering")
print("l: lights")
print("x: exit")

# Infinite loop that will not end until the user presses the
# exit key
def check_status():
    while True:
         toggleLights() 
         time.sleep(1)
      
        
#p1=  Process(target=check_status, args=()).start()
toggleLights() 
time.sleep(1)
toggleLights()

def check_distance():
    ultrasonic = DistanceSensor(echo=21, trigger=20)

    while True:

        dist=ultrasonic.distance
        
        #ultrasonic.when_in_range = toggleLights()
        if(dist <= 0.20 ):
            if(statuss=="forward"):
                stopmv()
                stopmv_ultra()
                print(dist)

        time.sleep(0.2)
        if(exits==True):
            break
#p2=  Process(target=check_distance,).start()
p2 = threading.Thread(target=check_distance, ).start()

while True:
    char = getch()
    if(char == "w"):
        move("forward",speed)

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
        move("backward",speed)

    # The "a" key will toggle the steering left
    if(char == "a"):
        toggleSteering("left")

    # The "d" key will toggle the steering right
    if(char == "d"):
        toggleSteering("right")

    # The "l" key will toggle the LEDs on/off
    if(char == "l"):
        toggleLights()
        
    # The "l" key will toggle the LEDs on/off
    if(char == "9"):
        if(speed < 1):
            speed=speed + 0.1
            if(speed > 1):
                speed=1
            if(statuss == "forward"):
                forward(speed)
            else:
                backward(speed)
          
            print(statuss)
            print(speed)

            print("speed increaded")
        else:
            print("speed max")  
             
        
    if(char == "6"):
        if(speed > 0.3):
            speed=speed - 0.1
            if(statuss == "backward"):
                backward(speed)
                print(statuss)
                print(speed)
            else:
                forward(speed)

            print("speed decreased")
        else:
            print("speed min")  

  #  ultrasonic.when_in_range = stopmv_ultra


    # The "x" key will break the loop and exit the program
    if(char == "x"):
        print("Program Ended")
        exits=True
        break
    

    # At the end of each loop the acceleration motor will stop
    # and wait for its next command
   #motorrl.stop()
#motorfb.stop()
    # The keyboard character variable will be set to blank, ready
    # to save the next key that is pressed
    char = ""

# Program will cease all GPIO activity before terminating


        
 
