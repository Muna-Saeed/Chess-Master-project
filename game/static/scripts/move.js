function handleSquareClick(square) {
    console.log("handleSquareClick function called");
    updateBoard();
    if (selectedSquare) {
	if (! computer) {document.getElementById('turn').innerHTML = "";}
        removePossibleClass();
        const piece = selectedSquare.querySelector('.piece');
	const endPiece = square.querySelector('.piece');
	const enemy = getPieceColor(piece) != getPieceColor(endPiece);
	const ColorBoard = boardOfColors();
        const startPosition = getPosition(selectedSquare);
        const endPosition = getPosition(square);

        const pieceType = piece.textContent.trim();
	console.log(pieceType);
        const board = getCurrentBoardState();

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/api/is_valid_move", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log("Received response from server:", xhr.responseText);
                const isValidMove = JSON.parse(xhr.responseText);
                console.log(isValidMove);

                if (isValidMove.valid_move) {
		    if (pieceType == '♙' && (endPosition[0] == 7 || endPosition[0] == 0)) {
			replace_pawn()
			    .then((newPiece) => {
				if (newPiece) {
				    piece.textContent = newPiece;
				} else {
				    console.log("Pawn promotion cancelled.");
				}
			    })
			    .catch((error) => {
				console.error("Error during promotion selection:", error);
			    });
		    }
		    if (isValidMove.killed){
			const killedpieceType = endPiece.textContent.trim();
			if (killedpieceType == '♔') {
			    for (let i = 0; i < 100; i++) {
				setTimeout(createConfetti, Math.random() * 3000);
			    }
			    setTimeout(() => {
				alert("Game finished\n new game will start");
				location.reload();
			    }, 7000);
			}
			square.removeChild(endPiece);
		    }
		    playValidSound();
                    selectedSquare.removeChild(piece);
                    selectedSquare.classList.remove('selected');
                    selectedSquare = null;
                    square.appendChild(piece);
		    
		    if (computer) {
			generateRandomMove();
		    }
		    else {
			turn = false;
			socket.emit("message", {"message":"board", start:startPosition, end:endPosition, game:gameId});
		    }
                } else {
		    playInValidSound();
		    selectedSquare.classList.remove('selected');
		    selectedSquare = null;		    
                }
            }
        };
        xhr.send(JSON.stringify({ board: board, boardColor:ColorBoard, enemy:enemy, start: startPosition, end: endPosition, pieceType: pieceType, color:userColor}));
    } else {
	const piece = square.querySelector('.piece');
	if (getPieceColor(piece) == userColor && turn){
	    possible_moves(square, piece);
	    square.classList.add('selected');
	    selectedSquare = square;
	    
	} else {
	    console.log("user not allowed");
	}
    }
}


function possible_moves(square, piece) {
    const pieceType = piece.textContent.trim();
    const color = getPieceColor(piece);
    const start = getPosition(square);
    const board = getChessboardSquares();
    const xhr = new XMLHttpRequest();
    const ColorBoard = boardOfColors();
    xhr.open("POST", "/api/possible", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
	if (xhr.readyState === 4 && xhr.status === 200) {
	    const moves = JSON.parse(xhr.responseText).moves;
	    
	    moves.forEach(index => {
                const square = board[index];
		square.classList.add('possible');
		const dotContainer = document.createElement('div');
                dotContainer.classList.add('dot-container');
                square.appendChild(dotContainer);
	     });
	}
    }

    xhr.send(JSON.stringify({color:color, start:start, board:ColorBoard, pieceType:pieceType, gameId:gameId}));
	  
}


// Function to get the position of a square
function getPosition(square) {
    // Get the index of the square within its parent container
    const index = Array.from(square.parentNode.children).indexOf(square);
    const row = Math.floor(index / 8);
    const col = index % 8;

    return [row, col];
}


function getCurrentBoardState() {
    const chessboard = document.getElementById('chessboard');
    const squares = chessboard.querySelectorAll('.square');
    const board = [];

    squares.forEach(square => {
        const piece = square.querySelector('.piece');
        if (piece) {
            const pieceType = piece.textContent.trim();
            board.push(pieceType);
        } else {
            board.push(null);
        }
    });

    return board;
}


function getChessboardSquares() {
    const chessboard = document.getElementById('chessboard');
    const squares = chessboard.querySelectorAll('.square');
    const board = [];

    squares.forEach(square => {
        board.push(square);
    });

    return board;
}

function getPieceColor(piece) {
    if (piece) {
        if (piece.classList.contains('white')) {
            return 'white';
        } else if (piece.classList.contains('black')) {
            return 'black';
        }
    }
    return null;
}


function boardOfColors(){
     const chessboard = document.getElementById('chessboard');
    const squares = chessboard.querySelectorAll('.square');
    const pieceColors = [];

    squares.forEach(square => {
        const piece = square.querySelector('.piece');
        if (piece) {
            const color = getPieceColor(piece);
            pieceColors.push(color);
        } else {
            pieceColors.push(null);
        }
    });
    return pieceColors;
}

function generateRandomMove() {
    updateBoard();
    const pieceColors = boardOfColors();
    const pieceBoard = getCurrentBoardState();
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/generate_random_move", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
	    console.log(response);
            const start_position = response.start_position;
            const end_position = response.end_position;
	    const board = getChessboardSquares();
	    start_square = board[start_position.row * 8 + start_position.col];
	    end_square = board[end_position.row * 8 + end_position.col];
	    console.log(start_position);
	    console.log(end_position);
	    if (response.killed) {
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
	    console.log(pieceToMove);
	    end_square.appendChild(pieceToMove);
	    
            console.log("End Position:", end_position);

        }
    };
    xhr.send(JSON.stringify({ board: pieceColors, pieceBoard: pieceBoard}));
}



function createConfetti() {
  const confetti = document.createElement('div');
  confetti.classList.add('confetti');
  confetti.style.left = `${Math.random() * 100}vw`;
  document.getElementById('celebration').appendChild(confetti);
  setTimeout(() => {
    confetti.remove();
  }, 5000);
}


function removePossibleClass() {
    const squares = document.querySelectorAll('.possible');
    squares.forEach(square => {
        square.classList.remove('possible');
    });
}



function updateBoard(){
       console.log(userId);
    const ColorBoard = boardOfColors();
    fetch('/api/board', {
	method: 'POST',
	headers: {
	    'Content-Type': 'application/json'
	},
	body: JSON.stringify({ ColorBoard: ColorBoard, gameId:gameId, userId:userId })
    });
}

updateBoard();

async function replace_pawn() {
 const replaceDiv = document.getElementById("replace");
 replaceDiv.style.display = "block";

 return new Promise((resolve) => {
  const buttonClickHandler = (event) => {
   if (event.target.closest("#replace")) { // Ensure click is within the replace div
    const selectedPiece = event.target.textContent.toLowerCase(); // Get clicked button text (lowercase)
    if (selectedPiece === "♕" || selectedPiece === "♖" || selectedPiece === "♗" || selectedPiece === "♘") {
     replaceDiv.style.display = "none"; // Hide the div after selection
     resolve(selectedPiece); // Resolve with selected piece
    }
     else {
       alert(false);
     }
   }
  };
  document.body.addEventListener("click", buttonClickHandler);
 });
}
