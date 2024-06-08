import RPi.GPIO as GPIO
import time

class BuzzerController:
    def __init__(self):
        self.BUZZER_PIN = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)

    def register_sound(self):
        pwm = GPIO.PWM(self.BUZZER_PIN, 980)  # Set frequency to 980 Hz
        pwm.start(50)  # Start PWM with 50% duty cycle
        time.sleep(0.2)  # Keep the sound on for 0.2 seconds
        pwm.stop()  # Stop the PWM

    def finish_sound(self):
        pwm = GPIO.PWM(self.BUZZER_PIN, 600)  # Set initial frequency to 600 Hz
        pwm.start(50)  # Start PWM with 50% duty cycle
        time.sleep(.1)  # Keep the sound on for 0.1 seconds
        pwm.ChangeFrequency(980)  # Change frequency to 980 Hz
        time.sleep(.2)  # Keep the sound on for 0.2 seconds
        pwm.stop()  # Stop the PWM

    def cancel_sound(self):
        pwm = GPIO.PWM(self.BUZZER_PIN, 980)  # Set initial frequency to 980 Hz
        pwm.start(50)  # Start PWM with 50% duty cycle
        time.sleep(.1)  # Keep the sound on for 0.1 seconds
        pwm.ChangeFrequency(600)  # Change frequency to 600 Hz
        time.sleep(.2)  # Keep the sound on for 0.2 seconds
        pwm.stop()  # Stop the PWM