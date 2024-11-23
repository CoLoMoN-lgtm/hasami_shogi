#pragma once
#include "board.hpp"
#include "move.hpp"
#include <vector>
#include <memory>

namespace hasami_shogi {

class Game {
public:
    enum class GameState { IN_PROGRESS, BLACK_WIN, WHITE_WIN, DRAW };
    enum class GameMode { PVP, AI_EASY, AI_MEDIUM, AI_HARD };
    
    Game(GameMode mode = GameMode::PVP);
    
    // Game state
    bool makeMove(const Move& move);
    GameState getGameState() const;
    Board::Piece getCurrentPlayer() const;
    const Board& getBoard() const;
    
    // Game history
    const std::vector<Move>& getMoveHistory() const;
    bool undoLastMove();
    
    // AI
    Move getAIMove() const;
    
    // Game management
    void reset();
    std::string getGameStateString() const;
    
    // Helper function
    bool isAITurn() const {
        return currentPlayer == Board::Piece::WHITE && 
               mode != GameMode::PVP;
    }
    
private:
    Board board;
    Board::Piece currentPlayer;
    GameState state;
    GameMode mode;
    std::vector<Move> moveHistory;
    std::vector<std::pair<int, int>> captureHistory;
    
    void switchPlayer();
    int countPieces(Board::Piece player) const;
    void updateGameState();
};

} // namespace hasami_shogi