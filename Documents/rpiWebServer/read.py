import RPi.GPIO as GPIO
import picamera
from mfrc522 import SimpleMFRC522
from time import sleep
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart #having multiple listing and i you have an attachment
from email.mime.text import MIMEText  #sending text emails
from email.mime.base import MIMEBase #base class so you dont have to create an instanes of mimebase
from email import encoders #extract the payload and encodes it for a new encoded value
import os
from flask import Flask
from flask import render_template







#setting GPIO pins to each value
greenLed = 19
redLed = 16
buzzer = 21
#setting each GPIO and depending on if its output or input i can be used as GPIO.OUT or GPIO.IN)
GPIO.setmode(GPIO.BCM) #when its BCM you have to use the GPIO number. If its GPIO.BOARD you have to use the pin number.
GPIO.setup(2, GPIO.OUT) 
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(greenLed, GPIO.OUT)
GPIO.setup(redLed, GPIO.OUT)
pwm=GPIO.PWM(2, 50)
pwm.start(0)
reader = SimpleMFRC522()



#only listed array have access
id_list =[619323204106]
# 140469410606
#We used Try and Finally method to make this into one code
try:
    while True:
        #Read the Keyfob and see if its ID number is the same
        #If its the same show the name of the keyfob owner name and Access granted and taking picture
        id, text = reader.read()
        if (id in id_list):
            print( id,"\n" + text + "\n" + "Access Granted" + "\n")
            print("taking picture")
            
            #Taking picture with picamera with the resolution of 1280 by 720 and capture it and save it as Family.jpg
            with picamera.PiCamera() as camera:
                camera.resolution = (1280, 720)
                camera.capture("/home/pi/Desktop/Family.jpg")
            print("Alerting your family you are here")
            
            #Buzzes and shows Green LED light to notify the User that the Keyfob worked.
            GPIO.output(greenLed, GPIO.HIGH)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW)
            sleep(False)
            GPIO.output(greenLed, GPIO.LOW)
            sleep(False)
            
            
            #The servo movment by setting the angle
            def SetAngle(angle):
                    duty=angle / 18+2
                    GPIO.output(2, True)
                    pwm.ChangeDutyCycle(duty)
                   
                    sleep(0.5)
                    GPIO.output(2, False)
                    pwm.ChangeDutyCycle(0)
            SetAngle(90)
            sleep(5)
            SetAngle(0)
            sleep(2)

            #Mail code
            mail_content = 'Your family member\n'+text + '\nhas entered your home'
            #The mail addresses and the gmail encrypted password
            sender_address = 'leafgreen714@gmail.com'
            sender_pass = 'oeotjzyjchjhssey'
            receiver_address = 'polyolly8099@gmail.com'
             #Setup the MIME
             #Set the From and To  and Subject
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = text+'Access Granted'
            
            #The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            for imageName in os.listdir('/home/pi/Desktop'):
                if imageName.endswith('jifif'):
                    print(imageName)

    
            attachName='/home/pi/Desktop/Family.jpg'
            attach_file_name = attachName

            # Open the file as binary mode
            attach_file = open(attach_file_name, "rb") 
            payload = MIMEBase('image', 'jpg')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) #encode the attachment
            #add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            message.attach(payload)
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print('Mail Sent')
          
          
#------------------------------------------------------------            
       
        elif (id not in id_list):
            print( id,"\n" + text + "\n" + "Access Denided" + "\n")
            print("taking picture")
            with picamera.PiCamera() as camera:
                camera.resolution = (1280, 720)
                camera.capture("/home/pi/Desktop/Unknown.jpg")
            print("Unknown Person has been notified")
            sleep(2)
           #Buzzes 3 times and shows Red LED to indicate the unknown person
            GPIO.output(redLed, GPIO.HIGH)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.2)
            GPIO.output(buzzer,GPIO.LOW)
            sleep(0.2)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.2)
            GPIO.output(buzzer,GPIO.LOW)
            sleep(0.2)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.2)
            GPIO.output(buzzer,GPIO.LOW)
            sleep(False)
            GPIO.output(redLed,GPIO.LOW)
            sleep(False)
            
            def SetAngle(angle):
                    duty=angle / 18+2
                    GPIO.output(2, True)
                    pwm.ChangeDutyCycle(duty)
                   
                    sleep(0.5)
                    GPIO.output(2, False)
                    pwm.ChangeDutyCycle(0)
            SetAngle(0)
            sleep(2)
            #Mail code
            mail_content = 'Unknown person\n'+text + '\ntried entering your home'
            #The mail addresses and the gmail encrypted password
            sender_address = 'leafgreen714@gmail.com'
            sender_pass = 'oeotjzyjchjhssey'
            receiver_address = 'polyolly8099@gmail.com'
            #Setup the MIME
             #Set the From and To  and Subject
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = text+'Access Denied'
            #The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            for imageName in os.listdir('/home/pi/Desktop'):
                if imageName.endswith('jifif'):
                    print(imageName)


            attachName='/home/pi/Desktop/Unknown.jpg'
            attach_file_name = attachName

            # Open the file as binary mode
            attach_file = open(attach_file_name, "rb") 
            payload = MIMEBase('image', 'jpg')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) #encode the attachment
            #add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            message.attach(payload)
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print('Mail Sent')
finally:GPIO.cleanup()            

