from flask import Flask
from flask import render_template
import RPi.GPIO as GPIO
from time import sleep

greenLed = 19
redLed = 16
buzzer = 21
servo = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(greenLed, GPIO.OUT)
GPIO.setup(redLed, GPIO.OUT)
pwm=GPIO.PWM(servo, 50)
pwm.start(0)


app= Flask(__name__)            
@app.route('/')
def index():
    return render_template('smartbox.html')
@app.route('/A')
def Unlock():
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(90/18+2)    
    sleep(2)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
    
    sleep(2)
    return render_template('smartbox.html')
@app.route('/a')
def Lock():
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(0/18+2)     
    sleep(2)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)          
    
    sleep(2)
    return render_template('smartbox.html')
if __name__=="__main__":
    print("Start")
    app.run(port=7777)