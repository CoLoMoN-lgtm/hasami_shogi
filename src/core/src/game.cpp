#include "game.hpp"
#include "ai.hpp"
#include <algorithm>

namespace hasami_shogi {

Game::Game(GameMode mode)
    : currentPlayer(Board::Piece::BLACK)
    , state(GameState::IN_PROGRESS)
    , mode(mode) {
    reset();
}

bool Game::makeMove(const Move& move) {
    // Check if game is already over
    if (state != GameState::IN_PROGRESS) {
        return false;
    }
    
    // Validate and make the move
    if (!board.isValidMove(move.fromRow, move.fromCol, move.toRow, move.toCol, currentPlayer)) {
        return false;
    }
    
    // Make the move
    board.setPiece(move.fromRow, move.fromCol, Board::Piece::EMPTY);
    board.setPiece(move.toRow, move.toCol, currentPlayer);
    
    // Record move in history
    moveHistory.push_back(move);
    
    // Check for captures and record the number of captured pieces
    bool captured = board.checkCaptures(move.toRow, move.toCol, currentPlayer);
    int capturedCount = captured ? countPieces(currentPlayer == Board::Piece::BLACK ? 
                                             Board::Piece::WHITE : Board::Piece::BLACK) : 0;
    captureHistory.push_back({capturedCount, 0});
    
    // Update game state
    updateGameState();
    
    // Switch players if game isn't over
    if (state == GameState::IN_PROGRESS) {
        switchPlayer();
        
        // If playing against AI and it's AI's turn, make AI move
        if (mode != GameMode::PVP && currentPlayer == Board::Piece::WHITE) {
            Move aiMove = getAIMove();
            makeMove(aiMove);
        }
    }
    
    return true;
}

Game::GameState Game::getGameState() const {
    return state;
}

Board::Piece Game::getCurrentPlayer() const {
    return currentPlayer;
}

const Board& Game::getBoard() const {
    return board;
}

void Game::reset() {
    board.resetBoard();
    currentPlayer = Board::Piece::BLACK;
    state = GameState::IN_PROGRESS;
    moveHistory.clear();
    captureHistory.clear();
}

bool Game::undoLastMove() {
    if (moveHistory.empty()) {
        return false;
    }
    
    // If in AI mode and undoing player's move, need to undo AI move as well
    if (mode != GameMode::PVP && moveHistory.size() >= 2) {
        // Undo AI move first
        Move aiMove = moveHistory.back();
        moveHistory.pop_back();
        captureHistory.pop_back();
        board.setPiece(aiMove.toRow, aiMove.toCol, Board::Piece::EMPTY);
        board.setPiece(aiMove.fromRow, aiMove.fromCol, Board::Piece::WHITE);
        
        // Then undo player's move
        Move playerMove = moveHistory.back();
        moveHistory.pop_back();
        captureHistory.pop_back();
        board.setPiece(playerMove.toRow, playerMove.toCol, Board::Piece::EMPTY);
        board.setPiece(playerMove.fromRow, playerMove.fromCol, Board::Piece::BLACK);
        
        currentPlayer = Board::Piece::BLACK;
    } else {
        // Regular undo for PvP mode
        Move lastMove = moveHistory.back();
        moveHistory.pop_back();
        captureHistory.pop_back();
        
        board.setPiece(lastMove.toRow, lastMove.toCol, Board::Piece::EMPTY);
        board.setPiece(lastMove.fromRow, lastMove.fromCol, currentPlayer);
        
        switchPlayer();
    }
    
    state = GameState::IN_PROGRESS;
    return true;
}

void Game::updateGameState() {
    int blackPieces = countPieces(Board::Piece::BLACK);
    int whitePieces = countPieces(Board::Piece::WHITE);
    
    if (blackPieces <= 1) {
        state = GameState::WHITE_WIN;
    } else if (whitePieces <= 1) {
        state = GameState::BLACK_WIN;
    } else if (moveHistory.size() >= 200) { // Prevent infinite games
        state = GameState::DRAW;
    }
}

int Game::countPieces(Board::Piece player) const {
    int count = 0;
    for (int i = 0; i < Board::BOARD_SIZE; ++i) {
        for (int j = 0; j < Board::BOARD_SIZE; ++j) {
            if (board.getPiece(i, j) == player) {
                count++;
            }
        }
    }
    return count;
}

Move Game::getAIMove() const {
    AI ai(board, Board::Piece::WHITE);
    int depth;
    
    switch (mode) {
        case GameMode::AI_EASY:
            depth = 2;
            break;
        case GameMode::AI_MEDIUM:
            depth = 4;
            break;
        case GameMode::AI_HARD:
            depth = 6;
            break;
        default:
            depth = 4;
    }
    
    return ai.getBestMove(depth);
}

const std::vector<Move>& Game::getMoveHistory() const {
    return moveHistory;
}

void Game::switchPlayer() {
    currentPlayer = (currentPlayer == Board::Piece::BLACK) ? 
                    Board::Piece::WHITE : Board::Piece::BLACK;
}

std::string Game::getGameStateString() const {
    switch (state) {
        case GameState::IN_PROGRESS:
            return "Game in progress";
        case GameState::BLACK_WIN:
            return "Black wins!";
        case GameState::WHITE_WIN:
            return "White wins!";
        case GameState::DRAW:
            return "Game drawn";
        default:
            return "Unknown state";
    }
}

} // namespace hasami_shogi