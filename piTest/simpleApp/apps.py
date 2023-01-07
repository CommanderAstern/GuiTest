from django.apps import AppConfig
import RPi.GPIO as GPIO
import time

class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleApp'
    def ready(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        pass # startup code here