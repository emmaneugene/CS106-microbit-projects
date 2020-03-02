# Create a game that gives you a random integer from 0 to 255
# After the number is displayed, you must enter the bit representation of the number (8-bit)
# If entered correctly, show smiley face
from microbit import *
import random

def get_binary_representation():
    total = 0
    multiplier = 1
    count = 0
    
    while count < 4:
        if button_a.is_pressed():
            total += multiplier
            multiplier *= 2
            count += 1
            display.scroll(str(total))
            
        if button_b.is_pressed():
            multiplier *= 2
            count += 1
            display.scroll(str(total))

    return total

while True:
    gesture = accelerometer.current_gesture()
    
    if gesture == "shake":
        n = random.randint(0, 15)
        display.scroll(str(n))
    
        guess = get_binary_representation()
        
        if guess == n:
            display.show(Image.HAPPY)
        else:
            display.show(Image.SAD)
        
        sleep(5000)
    
    
    
