import RPi.GPIO as GPIO
from time import sleep

# set GPIO numbering mode
#GPIO.setmode(GPIO.BOARD)
# set pin 12 as GPIO out
#GPIO.setup(12, GPIO.OUT)

def release():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    servo = GPIO.PWM(12, 50)
    servo.start(0)
    for x in range(2,12):
        servo.ChangeDutyCycle(x)
        sleep(0.5)
    servo.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    release()