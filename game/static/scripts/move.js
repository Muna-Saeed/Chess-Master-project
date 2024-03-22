// Function to handle click on a square
function handleSquareClick(square) {
    console.log("handleSquareClick function called");

    // If a square is already selected, move the piece to the clicked square
    if (selectedSquare) {
        console.log("Selected square exists");

        // Get the piece from the selected square
        const piece = selectedSquare.querySelector('.piece');

        // Get the start and end positions of the move
        const startPosition = getPosition(selectedSquare);
        const endPosition = getPosition(square);



        // Get the piece type from the selected square
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


                    // Remove the piece from the starting square
                    selectedSquare.removeChild(piece);

                    // Clear the selection
                    selectedSquare.classList.remove('selected');
                    selectedSquare = null;

                    // Move the piece visually to the clicked square
                    square.appendChild(piece);
                } else {
                    // Handle invalid move (e.g., display an error message)

                }
            }
        };
        xhr.send(JSON.stringify({ board: board, start: startPosition, end: endPosition, pieceType: pieceType}));
    } else {
        // Select the clicked square
        square.classList.add('selected');
        selectedSquare = square;
    }
}



// Function to get the position of a square
function getPosition(square) {
    // Get the index of the square within its parent container
    const index = Array.from(square.parentNode.children).indexOf(square);

    // Calculate row and column indices based on the linear index
    const row = Math.floor(index / 8); // Assuming 8 squares per row
    const col = index % 8; // Column is the remainder when divided by 8

    return [row, col];
}
    
 
 







// Function to get the current state of the board
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
