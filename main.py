from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'secret'
socketio = SocketIO( app )

def sendData():
	while True:
		distance = random.randint(3, 9)
		if distance > 5:
			isThere = 'FT'
		else:
			isThere = 'TF'

		socketio.emit('spots', isThere)
		socketio.sleep(2)
	

@app.route('/')
def index():
	return render_template('./index.html')

@socketio.on('connected')
def messageRecived(msg):
  print( '+++++++++++++NEW CONNECTION HAS BEEN MADE+++++++++++++' )

@socketio.on('send_req')
def handler(msg):
	sendData()
	
@socketio.on('connected')
def messageRecived(msg):
  print( '+++++++++++++NEW CONNECTION HAS BEEN TERMINATED+++++++++++++' )


if __name__ == '__main__':
  socketio.run( app, port = 9999, debug = True )