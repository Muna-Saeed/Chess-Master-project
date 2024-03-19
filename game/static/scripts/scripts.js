
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
    // Add event listeners for handling user interactions (e.g., moving pieces)
    // Implement game logic (e.g., piece movements, capturing)
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
    // Logic for placing pieces on the initial board position
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
