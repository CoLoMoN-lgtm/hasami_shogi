#pragma once
#include "board.hpp"
#include "move.hpp"
#include <vector>
#include <random>

namespace hasami_shogi {

class AI {
public:
    AI(const Board& board, Board::Piece player);
    
    Move getBestMove(int depth) const;
    
private:
    const Board& gameBoard;
    Board::Piece aiPlayer;
    
    // Evaluation functions
    int evaluatePosition(const Board& board) const;
    int minimax(Board board, int depth, int alpha, int beta, bool maximizingPlayer) const;
    
    // Helper functions
    std::vector<Move> getAllPossibleMoves(const Board& board, Board::Piece player) const;
    bool makeMove(Board& board, const Move& move, Board::Piece player) const;
    int getPieceDifference(const Board& board) const;
    int getPositionalScore(const Board& board) const;
    int getMobility(const Board& board, Board::Piece player) const;
    
    // Constants for evaluation
    static const int PIECE_VALUE = 100;
    static const int MOBILITY_WEIGHT = 10;
    static const int POSITION_WEIGHT = 5;
};

} // namespace hasami_shogi