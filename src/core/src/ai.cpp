#include "ai.hpp"
#include <algorithm>
#include <limits>
#include <random>

namespace hasami_shogi {

AI::AI(const Board& board, Board::Piece player) 
    : gameBoard(board), aiPlayer(player) {}

Move AI::getBestMove(int depth) const {
    std::vector<Move> possibleMoves = getAllPossibleMoves(gameBoard, aiPlayer);
    
    if (possibleMoves.empty()) {
        return Move();
    }
    
    int bestValue = std::numeric_limits<int>::min();
    Move bestMove = possibleMoves[0];
    
    for (const Move& move : possibleMoves) {
        Board tempBoard = gameBoard;
        if (makeMove(tempBoard, move, aiPlayer)) {
            int value = minimax(tempBoard, depth - 1, 
                              std::numeric_limits<int>::min(), 
                              std::numeric_limits<int>::max(), 
                              false);
            
            if (value > bestValue) {
                bestValue = value;
                bestMove = move;
            }
        }
    }
    
    return bestMove;
}

int AI::minimax(Board board, int depth, int alpha, int beta, bool maximizingPlayer) const {
    if (depth == 0) {
        return evaluatePosition(board);
    }
    
    Board::Piece currentPlayer = maximizingPlayer ? aiPlayer : 
        (aiPlayer == Board::Piece::BLACK ? Board::Piece::WHITE : Board::Piece::BLACK);
    
    std::vector<Move> possibleMoves = getAllPossibleMoves(board, currentPlayer);
    
    if (possibleMoves.empty()) {
        return evaluatePosition(board);
    }
    
    if (maximizingPlayer) {
        int maxEval = std::numeric_limits<int>::min();
        for (const Move& move : possibleMoves) {
            Board tempBoard = board;
            if (makeMove(tempBoard, move, currentPlayer)) {
                int eval = minimax(tempBoard, depth - 1, alpha, beta, false);
                maxEval = std::max(maxEval, eval);
                alpha = std::max(alpha, maxEval);
                if (beta <= alpha)
                    break;
            }
        }
        return maxEval;
    } else {
        int minEval = std::numeric_limits<int>::max();
        for (const Move& move : possibleMoves) {
            Board tempBoard = board;
            if (makeMove(tempBoard, move, currentPlayer)) {
                int eval = minimax(tempBoard, depth - 1, alpha, beta, true);
                minEval = std::min(minEval, eval);
                beta = std::min(beta, minEval);
                if (beta <= alpha)
                    break;
            }
        }
        return minEval;
    }
}

int AI::evaluatePosition(const Board& board) const {
    int score = 0;
    
    // Piece count
    score += getPieceDifference(board) * 100;
    
    // Control of center
    for (int i = 0; i < Board::BOARD_SIZE; i++) {
        for (int j = 0; j < Board::BOARD_SIZE; j++) {
            if (board.getPiece(i, j) == aiPlayer) {
                // Add bonus for controlling center squares
                int centerDist = std::abs(4 - i) + std::abs(4 - j);
                score += (8 - centerDist) * 5;
            }
        }
    }
    
    // Mobility
    score += getMobility(board) * 10;
    
    return score;
}

int AI::getPieceDifference(const Board& board) const {
    int aiPieces = 0;
    int oppPieces = 0;
    Board::Piece opponent = (aiPlayer == Board::Piece::BLACK) ? 
                            Board::Piece::WHITE : Board::Piece::BLACK;
    
    for (int i = 0; i < Board::BOARD_SIZE; i++) {
        for (int j = 0; j < Board::BOARD_SIZE; j++) {
            if (board.getPiece(i, j) == aiPlayer)
                aiPieces++;
            else if (board.getPiece(i, j) == opponent)
                oppPieces++;
        }
    }
    
    return aiPieces - oppPieces;
}

int AI::getMobility(const Board& board) const {
    return getAllPossibleMoves(board, aiPlayer).size();
}

std::vector<Move> AI::getAllPossibleMoves(const Board& board, Board::Piece player) const {
    std::vector<Move> moves;
    
    for (int fromRow = 0; fromRow < Board::BOARD_SIZE; fromRow++) {
        for (int fromCol = 0; fromCol < Board::BOARD_SIZE; fromCol++) {
            if (board.getPiece(fromRow, fromCol) == player) {
                // Check horizontal moves
                for (int toCol = 0; toCol < Board::BOARD_SIZE; toCol++) {
                    if (toCol != fromCol && board.isValidMove(fromRow, fromCol, fromRow, toCol, player)) {
                        moves.emplace_back(fromRow, fromCol, fromRow, toCol);
                    }
                }
                
                // Check vertical moves
                for (int toRow = 0; toRow < Board::BOARD_SIZE; toRow++) {
                    if (toRow != fromRow && board.isValidMove(fromRow, fromCol, toRow, fromCol, player)) {
                        moves.emplace_back(fromRow, fromCol, toRow, fromCol);
                    }
                }
            }
        }
    }
    
    return moves;
}

bool AI::makeMove(Board& board, const Move& move, Board::Piece player) const {
    if (!board.isValidMove(move.fromRow, move.fromCol, move.toRow, move.toCol, player)) {
        return false;
    }
    
    board.setPiece(move.fromRow, move.fromCol, Board::Piece::EMPTY);
    board.setPiece(move.toRow, move.toCol, player);
    board.checkCaptures(move.toRow, move.toCol, player);
    
    return true;
}

} // namespace hasami_shogi