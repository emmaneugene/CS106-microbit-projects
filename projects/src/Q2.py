from microbit import *
import math

def update_x(x):
    x_accel = accelerometer.get_x()
    
    if x_accel - get_x_anchor(x) > 325 and x < 4:
        return x + 1
    if x_accel - get_x_anchor(x) < -325 and x > 0:
        return x - 1

    return x
    
def update_y(y):
    y_accel = accelerometer.get_y()

    if y_accel - get_y_anchor(y) > 325 and y < 4:
        return y + 1
    if y_accel - get_y_anchor(y) < -325 and y > 0:
        return y - 1

    return y

def get_x_anchor(x):
    # returns the reference x-acceleration value given the position of x
    return (x - 2) * 325

def get_y_anchor(y):
    # returns the reference y-acceleration value given the position of y
    return (y - 2) * 325

def is_vertical():
    return accelerometer.current_gesture() in ('up', 'down', 'left', 'right')

def update_image(rotation):
    # mapping for pixels based on rotation
    if rotation < 22.5:
        return Image("90000:00000:00000:00000:00000")
    elif rotation < 45:
        return Image("90000:90000:00000:00000:00000")
    elif rotation < 67.5:
        return Image("90000:90000:90000:00000:00000")
    elif rotation < 90:
        return Image("90000:90000:90000:90000:00000")
    elif rotation < 112.5:
        return Image("90000:90000:90000:90000:90000")
    elif rotation < 135:
        return Image("90000:90000:90000:90000:99000")
    elif rotation < 157.5:
        return Image("90000:90000:90000:90000:99900")
    elif rotation < 180:
        return Image("90000:90000:90000:90000:99990")
    elif rotation < 202.5:
        return Image("90000:90000:90000:90000:99999")
    elif rotation < 225:
        return Image("90000:90000:90000:90009:99999")
    elif rotation < 247.5:
        return Image("90000:90000:90009:90009:99999")
    elif rotation < 270:
        return Image("90000:90009:90009:90009:99999")
    elif rotation < 292.5:
        return Image("90009:90009:90009:90009:99999")
    elif rotation < 315:
        return Image("90099:90009:90009:90009:99999")
    elif rotation < 337.5:
        return Image("90999:90009:90009:90009:99999")
    else: 
        return Image("99999:90009:90009:90009:99999")

def get_rotation(deg, anchor):
    if deg - anchor < 0:
        return deg - anchor + 360
    
    return deg - anchor

def get_degree():
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    # returns a degree based on x-pos and y-pos (arctan)
    # x > 0, y > 0, angle is 0 to 90
    # x > 0, y < 0, angle is 90 to 180 
    # x < 0, y < 0, angle is 180 to 270
    # x < 0, y > 0, angle is 270 to 360

    # take into account zero division
    if y == 0 and x > 0:
        return 0
    if y == 0 and x < 0:
        return 180

    angle = math.atan(math.fabs(x) / math.fabs(y))

    degree = (angle / math.pi) * 180

    if x >= 0 and y > 0:
        return degree

    if x >= 0 and y < 0:
        return 180 - degree    

    if x <= 0 and y < 0:
        return 180 + degree    

    if x <= 0 and y > 0:
        return 360 - degree    

compass.calibrate()

while True:
    # Face up mode
    value = 0
    x = 2
    y = 2
    
    while accelerometer.current_gesture() == 'face up':
        # base image is current count (0-9)
        i =  Image(str(value))
        # flicker our point over the base image
        i.set_pixel(x, y, 9)
        display.show(i)
        sleep(500)

        i.set_pixel(x, y, 0)
        display.show(i)
        sleep(500)
        x = update_x(x)
        y = update_y(y)

        # count will reset if point hits the edges
        if x % 4 == 0 or y % 4 == 0:
            value = 0
            display.clear()
            sleep(1000)

    # Vertical mode
    anchored = False
    rotated_backwards = False
    anchor = 0
    previous_rotation = 0
    current_rotation = 0

    while is_vertical():

        if not anchored:
            anchor = get_degree()
            previous_rotation = anchor
            anchored = True
        
        current_rotation = get_rotation(get_degree(), anchor)

        # check if user rotated backwards
        if previous_rotation < 22.5 and current_rotation > 315:
            rotated_backwards = True

        while rotated_backwards and is_vertical:
            display.show(Image("90000:00000:00000:00000:00000"))

            # check if user reset
            current_rotation = get_rotation(get_degree(), anchor)
            if  current_rotation < 22.5:
                rotated_backwards = False
            
        if not rotated_backwards:
            display.show(update_image(current_rotation))
            sleep(200)
        
        previous_rotation = current_rotation