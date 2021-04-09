var socket = io.connect('http://127.0.0.1:9999/');

socket.on('connect', function(){
    socket.emit('connected', '');
    start_comm()
})

function start_comm(){
	socket.emit('send_req', '');
}

socket.on('spots', function feast(msg){
	console.log(msg)
	if (msg[0] == 'T') { document.getElementById("spot1").style.backgroundColor = "green";}
    else{ document.getElementById("spot1").style.backgroundColor = "red";}

    if (msg[1] == 'T') { document.getElementById("spot2").style.backgroundColor = "green";}
	else{document.getElementById("spot2").style.backgroundColor = "red";}	})
/*
var spotIndex = [0,0,0,0,0,0]
var reserve = -1

ws.onmessage = function (event) {     
    if (event.data[0] == 'T') { document.getElementById("spot1").style.backgroundColor = "green";}
    else{ document.getElementById("spot1").style.backgroundColor = "red";}

    if (event.data[1] == 'T') { document.getElementById("spot2").style.backgroundColor = "green";}
	else{document.getElementById("spot2").style.backgroundColor = "red";}

	sendMessage();

		 };

function sendMessage() {
	for (var i = 0; i < spotIndex.length; i++) {
		if(spotIndex[i] == 1){
			reserve = i;
			spotIndex[i] = 0;}
		}
		ws.send(reserve);
		reserve = -1
}

function reserveSpot(spotId) {
	spotIndex[spotId] = 1;
}*/