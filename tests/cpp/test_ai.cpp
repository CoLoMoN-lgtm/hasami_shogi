#include <gtest/gtest.h>
#include "ai.hpp"
#include "game.hpp"

using namespace hasami_shogi;

class AITest : public ::testing::Test {
protected:
    Game game;
    AI ai;
    
    AITest() : game(Game::GameMode::AI_MEDIUM), 
               ai(game.getBoard(), Board::Piece::WHITE) {}
};

TEST_F(AITest, GeneratesValidMove) {
    Move aiMove = ai.getBestMove(3);  // depth 3
    
    // Check if move is within board boundaries
    EXPECT_GE(aiMove.fromRow, 0);
    EXPECT_LT(aiMove.fromRow, Board::BOARD_SIZE);
    EXPECT_GE(aiMove.fromCol, 0);
    EXPECT_LT(aiMove.fromCol, Board::BOARD_SIZE);
    EXPECT_GE(aiMove.toRow, 0);
    EXPECT_LT(aiMove.toRow, Board::BOARD_SIZE);
    EXPECT_GE(aiMove.toCol, 0);
    EXPECT_LT(aiMove.toCol, Board::BOARD_SIZE);
    
    // Check if move is valid according to game rules
    EXPECT_TRUE(game.getBoard().isValidMove(
        aiMove.fromRow, aiMove.fromCol,
        aiMove.toRow, aiMove.toCol,
        Board::Piece::WHITE
    ));
}

TEST_F(AITest, DifferentDifficulties) {
    // Easy AI should calculate faster than hard AI
    auto start = std::chrono::high_resolution_clock::now();
    Move easyMove = ai.getBestMove(1);
    auto easyDuration = std::chrono::high_resolution_clock::now() - start;
    
    start = std::chrono::high_resolution_clock::now();
    Move hardMove = ai.getBestMove(4);
    auto hardDuration = std::chrono::high_resolution_clock::now() - start;
    
    EXPECT_LT(easyDuration, hardDuration);
}

TEST_F(AITest, PrefersCaptureMove) {
    // Set up a capture opportunity
    game.getBoard().setPiece(3, 3, Board::Piece::WHITE);
    game.getBoard().setPiece(3, 4, Board::Piece::BLACK);
    game.getBoard().setPiece(3, 5, Board::Piece::EMPTY);
    
    Move aiMove = ai.getBestMove(3);
    
    // AI should choose the capture move
    EXPECT_EQ(aiMove.toRow, 3);
    EXPECT_EQ(aiMove.toCol, 5);
}

TEST_F(AITest, AvoidsSuicide) {
    // Set up a situation where moving would allow capture
    game.getBoard().setPiece(3, 3, Board::Piece::WHITE);
    game.getBoard().setPiece(3, 4, Board::Piece::EMPTY);
    game.getBoard().setPiece(3, 5, Board::Piece::BLACK);
    game.getBoard().setPiece(3, 2, Board::Piece::BLACK);
    
    Move aiMove = ai.getBestMove(3);
    
    // AI should not move to position 3,4 as it would be captured
    EXPECT_FALSE(aiMove.toRow == 3 && aiMove.toCol == 4);
}