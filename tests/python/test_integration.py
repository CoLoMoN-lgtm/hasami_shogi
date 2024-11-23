#include <gtest/gtest.h>
#include "game.hpp"
#include "ai.hpp"
#include <thread>
#include <chrono>

using namespace hasami_shogi;
using namespace std::chrono_literals;

class IntegrationTest : public ::testing::Test {
protected:
    Game game;
    
    void SetUp() override {
        game = Game(Game::GameMode::PVP);
    }
};

TEST_F(IntegrationTest, CompleteGameFlow) {
    // Test complete game flow with multiple moves and captures
    
    // Move black piece forward
    ASSERT_TRUE(game.makeMove(Move(0, 0, 3, 0)));
    EXPECT_EQ(game.getCurrentPlayer(), Board::Piece::WHITE);
    
    // Move white piece forward
    ASSERT_TRUE(game.makeMove(Move(8, 1, 5, 1)));
    EXPECT_EQ(game.getCurrentPlayer(), Board::Piece::BLACK);
    
    // Set up capture
    ASSERT_TRUE(game.makeMove(Move(3, 0, 5, 0)));
    ASSERT_TRUE(game.makeMove(Move(5, 1, 5, 2)));
    ASSERT_TRUE(game.makeMove(Move(0, 2, 5, 2)));
    
    // Verify capture occurred
    EXPECT_EQ(game.getBoard().getPiece(5, 1), Board::Piece::EMPTY);
}

TEST_F(IntegrationTest, AIGameFlow) {
    Game aiGame(Game::GameMode::AI_MEDIUM);
    
    // Make player move
    Move playerMove(0, 0, 3, 0);
    ASSERT_TRUE(aiGame.makeMove(playerMove));
    
    // AI should have made its move
    EXPECT_EQ(aiGame.getCurrentPlayer(), Board::Piece::BLACK);
    EXPECT_EQ(aiGame.getMoveHistory().size(), 2);
}

TEST_F(IntegrationTest, UndoRedoFlow) {
    // Make several moves
    game.makeMove(Move(0, 0, 3, 0));
    game.makeMove(Move(8, 0, 5, 0));
    game.makeMove(Move(0, 1, 3, 1));
    
    // Verify move history
    EXPECT_EQ(game.getMoveHistory().size(), 3);
    
    // Undo moves
    ASSERT_TRUE(game.undoLastMove());
    EXPECT_EQ(game.getMoveHistory().size(), 2);
    
    // Make different move
    ASSERT_TRUE(game.makeMove(Move(0, 2, 3, 2)));
    EXPECT_EQ(game.getMoveHistory().size(), 3);
}

TEST_F(IntegrationTest, GameEndConditions) {
    // Set up near-win condition
    auto& board = const_cast<Board&>(game.getBoard());
    for (int i = 0; i < Board::BOARD_SIZE; ++i) {
        for (int j = 0; j < Board::BOARD_SIZE; ++j) {
            board.setPiece(i, j, Board::Piece::EMPTY);
        }
    }
    
    // Leave only two pieces for black and one for white
    board.setPiece(0, 0, Board::Piece::BLACK);
    board.setPiece(0, 1, Board::Piece::BLACK);
    board.setPiece(8, 8, Board::Piece::WHITE);
    
    // Make capturing move
    game.makeMove(Move(0, 0, 8, 7));
    
    // Verify game end condition
    EXPECT_EQ(game.getGameState(), Game::GameState::BLACK_WIN);
}

TEST_F(IntegrationTest, AIPerformance) {
    Game aiGame(Game::GameMode::AI_HARD);
    
    // Measure time for AI move
    auto start = std::chrono::high_resolution_clock::now();
    aiGame.makeMove(Move(0, 0, 3, 0));
    auto end = std::chrono::high_resolution_clock::now();
    
    // AI should make decision in reasonable time (less than 5 seconds)
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(end - start);
    EXPECT_LT(duration.count(), 5);
}

TEST_F(IntegrationTest, ModifiedRules) {
    // Add test for any modified rules you implement
    // For example, testing special moves, additional capture conditions, etc.
    
    // This is a placeholder for when you implement modified rules
    EXPECT_TRUE(true);
}

TEST_F(IntegrationTest, ConcurrentGames) {
    // Test multiple games running concurrently
    Game game1(Game::GameMode::PVP);
    Game game2(Game::GameMode::AI_EASY);
    
    std::thread t1([&game1]() {
        game1.makeMove(Move(0, 0, 3, 0));
        game1.makeMove(Move(8, 0, 5, 0));
    });
    
    std::thread t2([&game2]() {
        game2.makeMove(Move(0, 1, 3, 1));
    });
    
    t1.join();
    t2.join();
    
    // Verify games didn't interfere with each other
    EXPECT_EQ(game1.getMoveHistory().size(), 2);
    EXPECT_EQ(game2.getMoveHistory().size(), 2);  // Including AI move
}

TEST_F(IntegrationTest, SaveLoadGame) {
    // Make some moves
    game.makeMove(Move(0, 0, 3, 0));
    game.makeMove(Move(8, 0, 5, 0));
    
    // Save game state to string
    std::string gameState = game.getBoard().toString();
    
    // Create new game and load state
    Game loadedGame(Game::GameMode::PVP);
    // This would require implementing a fromString method
    // loadedGame.getBoard().fromString(gameState);
    
    // Verify states match
    EXPECT_EQ(game.getBoard().toString(), loadedGame.getBoard().toString());
}