var socket = io({
  reconnect: true,
  reconnectionAttempts: 3,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  randomizationFactor: 0.5,
  timeout: 20000,
  autoConnect: true,
});

var from_id = null;
var room = null;
var turn = null;
gameId = null;
userColor = null;

function createMessage(name, message) {
    alert(name);
}

function sendMessage(player_id) {
    userColor = "black";
    turn = true;
    socket.emit("invite", {from_name:username, from_id:userId,  message: "invite" });
}

socket.on("message", function(data) {
    if (data.player_id != userId) {
	if (data.message == "board") {
	    turn = true;
	    const board = getChessboardSquares();
	    start_square = board[data.start[0] * 8 + data.start[1]];
	    end_square = board[data.end[0] * 8 + data.end[1]];
	    const pieceToRemove = end_square.querySelector('.piece');
	    if (pieceToRemove != null) {
		const pieceToRemove = end_square.querySelector('.piece');
		const pieceType = pieceToRemove.textContent.trim();
		if (pieceType == '♔') {
		    alert("You lost\n new game will start");
		    location.reload();
		}
		end_square.removeChild(pieceToRemove);
		
	    }
	    const pieceToMove = start_square.querySelector('.piece');
	    start_square.removeChild(pieceToMove);
	    end_square.appendChild(pieceToMove);
	}

	else if (data.message == "chat")
	{
	    const chatHistory = document.getElementById("chat-history");
	    const messageElement = document.createElement("p");
	    messageElement.textContent = `${data.name}: ${data.content}`;
	    chatHistory.appendChild(messageElement);

	}
	else if (data.message == "connected")
	{
	    updateOnline(data);
	}
	else if (data.message == "disconnected")
	{
	    removeUser(data);
	}

    }
});

function accept() {
    hidePopup();
    userColor = "white";
    turn = false;
    socket.emit("accept", {from_id: from_id,  to_id: userId, message: "accept", 'room': room });
}

function showPopup() {
    document.getElementById('popup').style.display = 'block';
}

function decline() {
    console.log('Invitation declined');
    hidePopup();
}

function hidePopup() {
    document.getElementById('popup').style.display = 'none';
}

function updateOnline(data) {
    var tag = document.getElementById("online");
    var li = document.createElement('li');
    li.innerHTML = `${data.name} <button id="${data.name}" onclick="sendMessage('${data.player_id}')">Invite To Play</button>`;
    tag.appendChild(li);
}

function removeUser(data) {
    var el = document.getElementById("online");
    var rem = document.getElementById(`${data.name}`);
    if (rem) {
        el.removeChild(rem);
    }
}

socket.on("invite", (data) => {
    room = data.room;
    from_id = data.from_id;
    if (from_id != userId) {showPopup();}
});

socket.on("play", (data) => {
    gameId = data.game;
    document.getElementById('before').style.display = 'none';
    document.getElementById('chessboard').style.display = 'grid';
    document.getElementById("container").style.display = "block";
    document.getElementById("name").innerHTML = data.name;
});


