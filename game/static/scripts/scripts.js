
// Define chessboard size and colors
const BOARD_SIZE = 8;
const LIGHT_SQUARE_COLOR = '#f0d9b5';
const DARK_SQUARE_COLOR = '#b58863';

// Constants for piece types
const PIECE_TYPES = {
    PAWN: 'pawn',
    ROOK: 'rook',
    KNIGHT: 'knight',
    BISHOP: 'bishop',
    QUEEN: 'queen',
    KING: 'king'
};

// Player colors
const PLAYER_COLORS = {
    WHITE: 'white',
    BLACK: 'black'
};

// Function to create the chessboard UI
function createChessboard() {
    const chessboard = document.getElementById('chessboard');

    for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
	    square.dataset.row = row;
            square.dataset.col = col;
            square.style.backgroundColor = (row + col) % 2 === 0 ? LIGHT_SQUARE_COLOR : DARK_SQUARE_COLOR;
            chessboard.appendChild(square);
        }
    }
}

// Function to create a chess piece
function createChessPiece(type, color) {
    const piece = document.createElement('div');
    piece.classList.add('piece', type, color);
    return piece;
}

// Function to initialize the chess game
function initializeChessGame() {
    createChessboard();
    setupPieces();
    addSquareClickListeners();
}

// Function to set up chess pieces on the board
function setupPieces() {
    const chessboard = document.getElementById('chessboard');

    // Place pawns
    for (let col = 0; col < BOARD_SIZE; col++) {
        chessboard.appendChild(createChessPiece(PIECE_TYPES.PAWN, PLAYER_COLORS.WHITE));
        chessboard.appendChild(createChessPiece(PIECE_TYPES.PAWN, PLAYER_COLORS.BLACK));
    }

    // Place other pieces (rooks, knights, bishops, queens, kings)
    for (let col = 0; col < BOARD_SIZE; col++) {
        const whitePieceTypes = [PIECE_TYPES.ROOK, PIECE_TYPES.KNIGHT, PIECE_TYPES.BISHOP, PIECE_TYPES.QUEEN, PIECE_TYPES.KING];
        const blackPieceTypes = [PIECE_TYPES.KING, PIECE_TYPES.QUEEN, PIECE_TYPES.BISHOP, PIECE_TYPES.KNIGHT, PIECE_TYPES.ROOK];
     // Logic for placing pieces on the initial board position   
        chessboard.appendChild(createChessPiece(whitePieceTypes[col], PLAYER_COLORS.WHITE));
        chessboard.appendChild(createChessPiece(blackPieceTypes[col], PLAYER_COLORS.BLACK));
    }
}

// Function to add event listeners for square clicks
function addSquareClickListeners() {
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        square.addEventListener('click', handleSquareClick);
    });
}

// Function to handle square click event
function handleSquareClick(event) {
    const clickedSquare = event.target;

    // Check if the clicked square contains a piece
    if (clickedSquare.classList.contains('piece')) {
        const selectedPiece = clickedSquare;
        // Implement logic to handle piece selection and movement
        handlePieceSelection(selectedPiece);
    } else {
        // Implement logic for empty square click
        handleEmptySquareClick(clickedSquare);
    }
}

// Function to handle piece selection and movement
function handlePieceSelection(piece) {
    // Remove highlighting from previously selected squares
    const previouslySelectedSquares = document.querySelectorAll('.selected');
    previouslySelectedSquares.forEach(square => square.classList.remove('selected'));

    // Highlight the clicked piece and its valid move squares
    piece.classList.add('selected');
    highlightValidMoves(piece);
}

// Function to highlight valid move squares for the selected piece
function highlightValidMoves(piece) {

    // Get valid moves for the selected piece based on its type and current position
    const validMoves = getValidMoves(piece);

    // Highlight valid move squares
    validMoves.forEach(move => {
        const [row, col] = move;
        const targetSquare = document.querySelector(`.square[data-row="${row}"][data-col="${col}"]`);
        targetSquare.classList.add('valid-move');
    });
}

// Function to get valid moves for a piece based on its type and position
function getValidMoves(piece) {

    // Get the current position of the piece
    const currentPosition = piece.parentElement;
    const currentRow = parseInt(currentPosition.dataset.row);
    const currentCol = parseInt(currentPosition.dataset.col);
    const validMoves = [];

    // Implement logic to determine valid moves based on the piece type
    switch (piece.classList[1]) {
        case PIECE_TYPES.PAWN:
            // Logic for pawn moves
            // Example: For now, let's say pawns can move one square forward
            const forwardSquare = document.querySelector(`[data-row="${currentRow + 1}"][data-col="${currentCol}"]`);
            if (forwardSquare) {
                validMoves.push([currentRow + 1, currentCol]);
            }
            break;
        // Add cases for other piece types: rook, knight, bishop, queen, king
        // Implement logic for their valid moves based on their movement rules
        default:
            break;
    }

    return validMoves;
}

// Function to handle empty square click
function handleEmptySquareClick(square) {
    const selectedPiece = document.querySelector('.piece.selected');

    // Check if there is a selected piece
    if (selectedPiece) {
        const targetSquare = square;
        // Move the selected piece to the empty square if it's a valid move
        if (targetSquare.classList.contains('valid-move')) {
            movePiece(selectedPiece, targetSquare);
        }
    }
}

// Function to move the piece to the target square
function movePiece(piece, targetSquare) {
    // Remove highlighting from all squares
    const allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => square.classList.remove('valid-move', 'selected'));

    // Move the piece to the target square
    targetSquare.appendChild(piece);
}



// Function to handle capturing opponent's piece
function handleCapturePiece(piece, targetSquare) {
    // Move capturing piece to the target square and remove captured piece
    handlePieceMovement(piece, targetSquare);
    targetSquare.removeChild(targetSquare.firstElementChild);
}

// Function to check if the move is a capture
function isCaptureMove(targetSquare) {
    return targetSquare.childElementCount > 0;
}



// Call initializeChessGame when the page loads
window.onload = initializeChessGame;

// Utility functions for API calls
// Function to fetch players data
async function fetchPlayers() {
    try {
        const response = await fetch('/api/players');
        const data = await response.json();
        console.log(data);
        // Process the received data (e.g., update UI)
    } catch (error) {
        console.error('Error fetching players:', error);
    }
}

// Function to create a new game
async function createGame() {
    try {
        const response = await fetch('/api/games', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ /* game data */ })
        });
        const result = await response.json();
        console.log(result);
        // Process the result (e.g., update UI)
    } catch (error) {
        console.error('Error creating game:', error);
    }
}
