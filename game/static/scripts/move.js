function handleSquareClick(square) {
    console.log("handleSquareClick function called");

    if (selectedSquare) {
        console.log("Selected square exists");

        const piece = selectedSquare.querySelector('.piece');

        const startPosition = getPosition(selectedSquare);
        const endPosition = getPosition(square);

        const pieceType = piece.textContent.trim();
        console.log(pieceType);
        // Get the current state of the board
        const board = getCurrentBoardState();

        // Send an AJAX request to check if the move is valid
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/api/is_valid_move", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log("Received response from server:", xhr.responseText);
                const isValidMove = JSON.parse(xhr.responseText);
                console.log(isValidMove);

                if (isValidMove.valid_move) {
		    playValidSound();
                    selectedSquare.removeChild(piece);

                    selectedSquare.classList.remove('selected');
                    selectedSquare = null;

                    square.appendChild(piece);
		    generateRandomMove(board);
                } else {
		    playInValidSound();
		    selectedSquare.classList.remove('selected');
		    selectedSquare = null;
		    
                }
            }
        };
        xhr.send(JSON.stringify({ board: board, start: startPosition, end: endPosition, pieceType: pieceType}));
    } else {
	const piece = square.querySelector('.piece');
	console.log(piece);
	console.log(getPieceColor(piece))
	if (getPieceColor(piece) == userColor){
	    square.classList.add('selected');
	    selectedSquare = square;
	} else {
	    console.log("user not allowed");
	}
    }
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


function generateRandomMove() {
    const chessboard = document.getElementById('chessboard');
    const squares = chessboard.querySelectorAll('.square');
    const pieceColors = [];

    squares.forEach(square => {
        const piece = square.querySelector('.piece');
        if (piece) {
            const color = getPieceColor(piece);
	    console.log(color);
            pieceColors.push(color);
        } else {
            pieceColors.push(null);
        }
    });

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/generate_random_move", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const start_position = response.start_position;
            const end_position = response.end_position;
	    const board = getChessboardSquares();
	    start_square = board[start_position.row * 8 + start_position.col];
	    end_square = board[end_position.row * 8 + end_position.col];
	    console.log(start_square);
	    console.log(end_square);
	    
	    const pieceToMove = start_square.querySelector('.piece');
	    start_square.removeChild(pieceToMove);
	    console.log(pieceToMove);
	    end_square.appendChild(pieceToMove);
	    
            console.log("End Position:", end_position);

        }
    };
    xhr.send(JSON.stringify({ board: pieceColors }));
}
