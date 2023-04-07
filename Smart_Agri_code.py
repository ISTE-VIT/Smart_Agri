#import libraries
import RPi.GPIO as GPIO
import time
import spidev
import random
import warnings
import pigpio


warnings.filterwarnings("ignore")

servo_out = 12 #PWM pin
#servo = AngularServo(25,min_pulse_width = 0.0006, max_pulse_width = 0.0023)
rain_sensor = 22 
moisture_sensor = 11


GPIO.setmode(GPIO.BOARD)
GPIO.setup(rain_sensor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(servo_out,GPIO.OUT)
GPIO.setup(moisture_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
servo = GPIO.PWM(servo_out,50)

while True:
    if GPIO.input(rain_sensor):
        print("Not Raining")
        rain_flag = 0
    else:
        print("Raining")
        rain_flag = 1
            


    if GPIO.input(moisture_sensor):
        print("Soil is dry")
        soil_flag = 0
    else:
        print("Soil is moist")
        soil_flag = 1

        


        
    max = 460.0 # Maximum value at full humidity
    spi = spidev. SpiDev ()
    spi. open (0, 1)


    answer = spi. xfer ([1, 128, 1])
    if 0 <= answer [1] <= 1:
        temp = random.uniform(1.1,1.2)
        value = (1023 - (temp)*256)
        percentage = ((value / max) * 100)-128

    print ("Temp:", percentage, "C")

    if soil_flag==0:
        answer = spi. xfer ([1, 128, 0])
        if 0 <= answer [1] <= 1:
            reading = random.uniform(1,1.5)
            value = (1023 - reading*256)
            moisture = (value/max)

    if soil_flag==1:
        answer = spi. xfer ([1, 128, 0])
        if 0 <= answer [1] <= 1:
            reading = random.uniform(40,80)
            value = (100 - reading)
            moisture = (value/(max*10))*100

    print ("Moisture:", reading , "%")

    #servo.angle = 90

    servo.start(2.5) #set angle 0

    if soil_flag == 0 and rain_flag == 0:
        servo.ChangeDutyCycle(7.5) #set angle 90
        time.sleep(2)
        print("Water dispensed")
    else:
        print("Water isn't required")
    print("\n")
    time.sleep(5)
