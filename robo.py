import explorerhat as eh
import time
from gpiozero import LineSensor
import signal
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import requests

DHTPin = 10   #define the pin of DHT11

left_sensor = LineSensor(24)
right_sensor= LineSensor(25)

left_motor = eh.motor.one
right_motor = eh.motor.two

left_on_line = False
right_on_line = False

dry_run = False

low_speed = 0
turning_speed = 10
backwards_speed = -turning_speed
high_speed = 10

API_ENDPOINT = 'http://192.168.43.183:3000/temperatures'

def go_left():
    global dry_run, low_speed, turning_speed, high_speed, left_motor, right_motor
    print('going left')
    if not dry_run:
        left_motor.forwards(turning_speed)
        right_motor.forwards(low_speed)
    
def go_right():
    global dry_run, low_speed, turning_speed, high_speed, left_motor, right_motor
    print('going right')
    if not dry_run:
        left_motor.forwards(low_speed)
        right_motor.forwards(turning_speed)
    
def go_onwards():
    global dry_run, high_speed, left_motor, right_motor
    print('going onwards')
    if not dry_run:
        left_motor.forwards(high_speed)
        right_motor.forwards(high_speed)

def stop():
    global dry_run, left_motor, right_motor
    print('stop')
    if not dry_run:
        left_motor.stop()
        right_motor.stop()

def update_states():
    global left_on_line
    global right_on_line
#    print('update_states()')
  #  print('left on line: ' + str(left_on_line))
  #  print('right on line: ' + str(right_on_line))
    if left_on_line and right_on_line:
#        print('left on line' + str(left_on_line))
#        print('right on line' + str(right_on_line))
        print ('Should not get here, both sensors on line!')
        stop()
    elif left_on_line:
        go_left()
    elif right_on_line:
        go_right()
    else:
        go_onwards()

def left_update(state):
    global left_on_line
    #print('left update: ' + str(state))
    left_on_line = state
    #update_states()
        
def right_update(state):
    global right_on_line
    #print('right update: ' + str(state))
    right_on_line = state
    #update_states()

def temperature_update():
   stop()
   dht = DHT.DHT(DHTPin)
   chk = dht.readDHT11()
   if (chk is dht.DHTLIB_OK):
       temp_now = dht.temperature
       print('Temperature:' + str(temp_now))
       return temp_now
   else: #error state
       print("Error from temperature sensor!")
       time.sleep(0.5)
       return temperature_update()

def push_data_to_api(temperature):
    data = {
        'temp': str(temperature), 'floor_level':'5', 'longitude':'52.542793', 'latitude':'-0.134542'
    }
    #need a timeout
    response = requests.post(url = API_ENDPOINT, data = data)
    json_response = response.json()
    print(json_response)
    if response:
        print('Pushed data to API')
    else:
        print('Failed to push data to API')

def turn_light_on():
    eh.output.one.on()

def turn_light_off():
    eh.output.one.off()

left_sensor.when_line = lambda: left_update(True)
left_sensor.when_no_line = lambda: left_update(False)

right_sensor.when_line = lambda: right_update(True)
right_sensor.when_no_line = lambda: right_update(False)

#signal.signal(signal.SIGINT, lambda x: stop())

count=0

while 1:
    update_states()
    time.sleep(0.1)
    count=count+1
    if(count%100 == 0):
        stop()
        turn_light_on()
        current_temperature = temperature_update()
        push_data_to_api(current_temperature)
       # turn_light_off()