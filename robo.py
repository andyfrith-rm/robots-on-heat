import explorerhat as eh
import time
from gpiozero import LineSensor
import signal

left_sensor = LineSensor(22)
right_sensor= LineSensor(16)

left_motor = eh.motor.one
right_motor = eh.motor.two

left_on_line = True
right_on_line = True

dry_run = True

low_speed = 0
turning_speed = 15
high_speed = 15

def go_left():
    global dry_run, low_speed, turning_speed, high_speed
    print('going left')
    if not dry_run:
        left_motor.forwards(turning_speed)
        right_motor.forwards(low_speed)
    
def go_right():
    global dry_run, low_speed, turning_speed, high_speed
    print('going right')
    if not dry_run:
        left_motor.forwards(low_speed)
        right_motor.forwards(turning_speed)
    
def go_onwards():
    global dry_run, high_speed
    print('going onwards')
    if not dry_run:
        left_motor.forwards(high_speed)
        right_motor.forwards(high_speed)

def stop():
    global dry_run
    print('stop')
    if not dry_run:
        left_motor.stop()
        right_motor.stop()

def update_states():
    global left_on_line
    global right_on_line
#    print('update_states()')
    if left_on_line and right_on_line:
#        print('left on line' + str(left_on_line))
#        print('right on line' + str(right_on_line))
        go_onwards()
    elif left_on_line:
        go_left()
    elif right_on_line:
        go_right()
    else:
        stop()

def left_update(state):
    global left_on_line
#    print('left update: ' + str(state))
    left_on_line = state
    #update_states()
        
def right_update(state):
    global right_on_line
#    print('right update: ' + str(state))
    right_on_line = state
    #update_states()

left_sensor.when_line = lambda: left_update(True)
left_sensor.when_no_line = lambda: left_update(False)

right_sensor.when_line = lambda: right_update(True)
right_sensor.when_no_line = lambda: right_update(False)

signal.signal(signal.SIGINT, lambda x: stop())

while 1:
    update_states()
    time.sleep(0.1)