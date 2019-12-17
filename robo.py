import explorerhat as eh
import time
from gpiozero import LineSensor
import signal

left_sensor = LineSensor(22)
right_sensor= LineSensor(24)

left_on_line = True
right_on_line = True

dry_run = False

low_speed = 0
turning_speed = 15
high_speed = 15

#andy was here

def go_left():
    global dry_run, low_speed, turning_speed, high_speed
    print('going left')
    if not dry_run:
        eh.motor.one.forwards(turning_speed)
        eh.motor.two.forwards(low_speed)
    
def go_right():
    global dry_run, low_speed, turning_speed, high_speed
    print('going right')
    if not dry_run:
        eh.motor.one.forwards(low_speed)
        eh.motor.two.forwards(turning_speed)
    
def go_onwards():
    global dry_run, high_speed
    print('going onwards')
    if not dry_run:
        eh.motor.one.forwards(high_speed)
        eh.motor.two.forwards(high_speed)

def stop():
    global dry_run
    print('stop')
    if not dry_run:
        eh.motor.one.stop()
        eh.motor.two.stop()

def update_states():
    global left_on_line
    global right_on_line
#    print('update_states()')
    if left_on_line and right_on_line:
        print('left on line' + str(left_on_line))
        print('right on line' + str(right_on_line))
        go_onwards()
    elif left_on_line:
        go_left()
    elif right_on_line:
        go_right()
    else:
        stop()

def left_update(state):
    global left_on_line
    print('left update: ' + str(state))
    left_on_line = state
    update_states()
        
def right_update(state):
    global right_on_line
    print('right update: ' + str(state))
    right_on_line = state
    update_states()

left_sensor.when_line = lambda: left_update(True)
left_sensor.when_no_line = lambda: left_update(False)

right_sensor.when_line = lambda: right_update(True)
right_sensor.when_no_line = lambda: right_update(False)

signal.signal(signal.SIGINT, lambda x: stop())

update_states()
