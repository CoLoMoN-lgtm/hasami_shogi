#include <gtest/gtest.h>
#include "game.hpp"

using namespace hasami_shogi;

class GameTest : public ::testing::Test {
protected:
    Game game;
};

TEST_F(GameTest, InitialGameState) {
    EXPECT_EQ(game.getCurrentPlayer(), Board::Piece::BLACK);
    EXPECT_EQ(game.getGameState(), Game::GameState::IN_PROGRESS);
    EXPECT_TRUE(game.getMoveHistory().empty());
}

TEST_F(GameTest, MakingMoves) {
    // Make valid move
    Move move{0, 0, 3, 0};
    EXPECT_TRUE(game.makeMove(move));
    EXPECT_EQ(game.getCurrentPlayer(), Board::Piece::WHITE);
    EXPECT_EQ(game.getMoveHistory().size(), 1);
    
    // Try invalid move
    Move invalidMove{8, 0, 5, 5};  // Diagonal move
    EXPECT_FALSE(game.makeMove(invalidMove));
    EXPECT_EQ(game.getCurrentPlayer(), Board::Piece::WHITE);
    EXPECT_EQ(game.getMoveHistory().size(), 1);
}

TEST_F(GameTest, UndoMove) {
    Move move{0, 0, 3, 0};
    game.makeMove(move);
    
    EXPECT_TRUE(game.undoLastMove());
    EXPECT_EQ(game.getCurrentPlayer(), Board::Piece::BLACK);
    EXPECT_TRUE(game.getMoveHistory().empty());
    
    // Try undo with no moves
    EXPECT_FALSE(game.undoLastMove());
}

TEST_F(GameTest, GameModes) {
    // Test PvP mode
    Game pvpGame(Game::GameMode::PVP);
    EXPECT_FALSE(pvpGame.isAITurn());
    
    // Test AI mode
    Game aiGame(Game::GameMode::AI_MEDIUM);
    EXPECT_FALSE(aiGame.isAITurn());  // Player should go first
    
    Move move{0, 0, 3, 0};
    aiGame.makeMove(move);
    EXPECT_TRUE(aiGame.isAITurn());
}

TEST_F(GameTest, Capturing) {
    // Set up capture scenario
    game.getBoard().setPiece(3, 3, Board::Piece::BLACK);
    game.getBoard().setPiece(3, 4, Board::Piece::WHITE);
    
    Move captureMove{3, 5, 3, 3};
    game.makeMove(captureMove);
    
    EXPECT_EQ(game.getBoard().getPiece(3, 4), Board::Piece::EMPTY);
}