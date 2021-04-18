from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import random
import RPi.GPIO as GPIO
import time
import asyncio
import websockets
from datetime import datetime, timedelta 


# setting pins for pi
triggers = [7,13]  # Trigger pins
echos = [11,24]  # Echo pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'secret'
socketio = SocketIO( app )



def GetDistance(TRIG,ECHO):
    # driver code for ultrasonic sensor thats connected to raspberry pi
    # returns a string (True/False) based on the distance data accquired from the sensor
    # True = if distance greater than a pre defined value, False if lesser. which indicates if a spot is taken or available
    heightofLot = 10
    isThere = 'T'
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(0.2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    pulse_duration = pulse_duration/2
    distance = pulse_duration * 34000
    distance = round(distance, 2)

    if distance > heightofLot:
        isThere = 'F'
    else:
        isThere = 'T'

    return isThere


class SPSDriverClass:
    def __init__(self,triggerPins, echoPins):
        self.lots = [0,0,0,0,0,0]
        self.reservedLots = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}
        self.sensors = 2
        self.tempInfo = ''
        self.echoPins = echoPins
        self.triggerPins = triggerPins
        self.reserveTime = 1


    def parkingInfo(self):
            self.tempInfo = ''
            for sensor in range(self.sensors):
                self.tempInfo += GetDistance(self.triggerPins[sensor],self.echoPins[sensor])

    def reserveLot(self, lotId):
        self.lots[lotId] = 1
        self.reservedLots[lotId] = datetime.now() + timedelta(minutes = self.reserveTime)
        

    def getFinalValue(self):
        self.parkingInfo()
        self.validateReservations()
        for lot in range(len(self.lots)):
            if self.lots[lot] == 1:
                self.tempInfo = self.tempInfo[:lot]+'T'+self.tempInfo[lot+1:]
        return self.tempInfo

    def validateReservations(self):
        now = datetime.now()
        for slot in self.reservedLots.keys():
            if self.reservedLots[slot] is not None:
                if now > self.reservedLots[slot]:
                    self.lots[slot] = 0
            else:
                pass

def communicate():
    while True:
        spotsOccupied = SPS.getFinalValue()
        socketio.emit('spots', spotsOccupied)
        socketio.sleep(1)

@app.route('/')
def index():
    return render_template('./index.html')

@socketio.on('connected')
def messageRecived(msg):
  print( 'connection from ' + msg + "made")

@socketio.on('startCommunication')
def communicationHandler(msg):
    print("communicate called from :" + msg)
    communicate()

@socketio.on('reserveRequest')
def reservationHandler(msg):
    print("reserveRequest by spot ",msg)
    SPS.reserveLot(msg)
    

SPS = SPSDriverClass(triggers,echos)

if __name__ == '__main__':
    cors = CORS(app,resources={r"/*":{"origins":"*"}})
    socketio.run( app,host="192.168.0.7", port = 9999, debug = True)