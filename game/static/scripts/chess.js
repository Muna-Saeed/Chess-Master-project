// Define chessboard size
const BOARD_SIZE = 8;

// Constants for piece types
const PIECE_TYPES = {
    ROOK: '&#9814;',
    KNIGHT: '&#9816;',
    BISHOP: '&#9815;',
    QUEEN: '&#9813;',
    KING: '&#9812;',
    PAWN: '&#9817;'
};

// Variable to keep track of selected square
let selectedSquare = null;

// Function to create the chessboard UI
function createChessboard() {
    const chessboard = document.getElementById('chessboard');

    for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.classList.add((row + col) % 2 === 0 ? 'light' : 'dark'); // Alternating colors

            // Add click event listener to each square
            square.addEventListener('click', () => handleSquareClick(square));

            // Place pieces
            if (row === 1 || row === 6) {
                const pieceColor = row === 1 ? 'black' : 'white';
                square.innerHTML = `<div class="piece pawn ${pieceColor}">${row === 1 ? PIECE_TYPES.PAWN : PIECE_TYPES.PAWN}</div>`;
            } else if (row === 0 || row === 7) {
                const pieceColor = row === 0 ? 'black' : 'white';
                const piecesOrder = [PIECE_TYPES.ROOK, PIECE_TYPES.KNIGHT, PIECE_TYPES.BISHOP, PIECE_TYPES.QUEEN, PIECE_TYPES.KING, PIECE_TYPES.BISHOP, PIECE_TYPES.KNIGHT, PIECE_TYPES.ROOK];
                square.innerHTML = `<div class="piece ${pieceColor}">${piecesOrder[col]}</div>`;
            } else {
                square.innerHTML = ''; // Empty square
            }

            chessboard.appendChild(square);
        }
    }
}

// Function to handle click on a square
function handleSquareClick(square) {
    // If a square is already selected, move the piece to the clicked square
    if (selectedSquare) {
        // Implement move logic here
        // Example: Move the piece from selectedSquare to square

        // Clear the selection
        selectedSquare.classList.remove('selected');
        selectedSquare = null;
    } else {
        // Select the clicked square
        square.classList.add('selected');
        selectedSquare = square;
    }
}

// Call createChessboard when the page loads
window.onload = createChessboard;
