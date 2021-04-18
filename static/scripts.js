var socket = io.connect('http://192.168.0.7:9999/');
var spotIndex = [0,0,0,0,0,0]
var reserve = -1

socket.on('connect', function(){
    socket.emit('connected', 'client test 1');
    start_comm()
})



function start_comm(){
	socket.emit('startCommunication', 'client test 1');
}



socket.on('spots', function feast(msg){
	console.log(msg)
	if (msg[0] == 'T') { document.getElementById("spot1").style.backgroundColor = "green";}
    else{ document.getElementById("spot1").style.backgroundColor = "red";}

    if (msg[1] == 'T') { document.getElementById("spot2").style.backgroundColor = "green";}
	else{document.getElementById("spot2").style.backgroundColor = "red";}

	if (msg[2] == 'T') { document.getElementById("spot3").style.backgroundColor = "green";}
	else{document.getElementById("spot3").style.backgroundColor = "red";}

	if (msg[3] == 'T') { document.getElementById("spot4").style.backgroundColor = "green";}
	else{document.getElementById("spot4").style.backgroundColor = "red";}

	if (msg[4] == 'T') { document.getElementById("spot5").style.backgroundColor = "green";}
	else{document.getElementById("spot5").style.backgroundColor = "red";}

	if (msg[5] == 'T') { document.getElementById("spot6").style.backgroundColor = "green";}
	else{document.getElementById("spot6").style.backgroundColor = "red";}

})

function reserveSpot(number){
	socket.emit('reserveRequest', number);
}

