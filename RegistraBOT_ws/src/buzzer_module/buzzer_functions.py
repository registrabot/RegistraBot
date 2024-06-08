import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the buzzer
BUZZER_PIN = 16

# Set up the GPIO pin as an output
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Function to play a sound at 600 Hz
def register_sound():
    pwm = GPIO.PWM(BUZZER_PIN, 980)  # Set frequency to 980 Hz
    pwm.start(50)  # Start PWM with 50% duty cycle
    time.sleep(0.2)  # Keep the sound on for 1 second
    pwm.stop()  # Stop the PWM

# Function to play a sound at 980 Hz
def finish_sound():
    pwm = GPIO.PWM(BUZZER_PIN, 600)  # Set initial frequency to 600 Hz
    pwm.start(50)  # Start PWM with 50% duty cycle
    time.sleep(.1)  # Keep the sound on for 1 second
    pwm.ChangeFrequency(980)  # Change frequency to 980 Hz
    time.sleep(.2)  # Keep the sound on for 1 second
    pwm.stop() # Stop the PWM

def cancel_sound():
    pwm = GPIO.PWM(BUZZER_PIN, 980)  # Set initial frequency to 980 Hz
    pwm.start(50)  # Start PWM with 50% duty cycle
    time.sleep(.1)  # Keep the sound on for 1 second
    pwm.ChangeFrequency(600)  # Change frequency to 600 Hz
    time.sleep(.2)  # Keep the sound on for 1 second
    pwm.stop()  # Stop the PWM


