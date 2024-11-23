#include <gtest/gtest.h>
#include "board.hpp"

using namespace hasami_shogi;

class BoardTest : public ::testing::Test {
protected:
    Board board;
};

TEST_F(BoardTest, InitialBoardSetup) {
    // Check initial piece positions
    for (int col = 0; col < Board::BOARD_SIZE; ++col) {
        EXPECT_EQ(board.getPiece(0, col), Board::Piece::BLACK);
        EXPECT_EQ(board.getPiece(Board::BOARD_SIZE-1, col), Board::Piece::WHITE);
    }
    
    // Check middle rows are empty
    for (int row = 1; row < Board::BOARD_SIZE-1; ++row) {
        for (int col = 0; col < Board::BOARD_SIZE; ++col) {
            EXPECT_EQ(board.getPiece(row, col), Board::Piece::EMPTY);
        }
    }
}

TEST_F(BoardTest, ValidMoves) {
    // Test horizontal move
    EXPECT_TRUE(board.isValidMove(0, 0, 0, 2, Board::Piece::BLACK));
    
    // Test vertical move
    EXPECT_TRUE(board.isValidMove(0, 0, 2, 0, Board::Piece::BLACK));
    
    // Test invalid diagonal move
    EXPECT_FALSE(board.isValidMove(0, 0, 1, 1, Board::Piece::BLACK));
    
    // Test move through pieces
    EXPECT_FALSE(board.isValidMove(0, 0, 0, 3, Board::Piece::BLACK));
    
    // Test move to occupied space
    EXPECT_FALSE(board.isValidMove(0, 0, 0, 1, Board::Piece::BLACK));
}

TEST_F(BoardTest, Captures) {
    // Set up capture scenario
    board.setP

    // Set up capture scenario
    board.setPiece(3, 3, Board::Piece::BLACK);
    board.setPiece(3, 4, Board::Piece::WHITE);
    board.setPiece(3, 5, Board::Piece::EMPTY);
    
    // Test capture
    board.setPiece(3, 5, Board::Piece::BLACK);
    EXPECT_TRUE(board.checkCaptures(3, 5, Board::Piece::BLACK));
    EXPECT_EQ(board.getPiece(3, 4), Board::Piece::EMPTY);
    
    // Test multiple captures
    board.setPiece(4, 3, Board::Piece::WHITE);
    board.setPiece(5, 3, Board::Piece::WHITE);
    board.setPiece(6, 3, Board::Piece::BLACK);
    EXPECT_TRUE(board.checkCaptures(2, 3, Board::Piece::BLACK));
    EXPECT_EQ(board.getPiece(4, 3), Board::Piece::EMPTY);
    EXPECT_EQ(board.getPiece(5, 3), Board::Piece::EMPTY);
}

TEST_F(BoardTest, ValidMovesGeneration) {
    auto moves = board.getValidMoves(0, 0);
    
    // Check number of valid moves from initial position
    EXPECT_EQ(moves.size(), 7);  // Can move up to 7 spaces forward
    
    // Check if all moves are either horizontal or vertical
    for (const auto& move : moves) {
        EXPECT_TRUE(move.first == 0 || move.second == 0);
    }
}

TEST_F(BoardTest, GameEndConditions) {
    // Set up a near-win condition for Black
    board.resetBoard();
    for (int i = 0; i < Board::BOARD_SIZE; ++i) {
        for (int j = 0; j < Board::BOARD_SIZE; ++j) {
            board.setPiece(i, j, Board::Piece::EMPTY);
        }
    }
    
    board.setPiece(0, 0, Board::Piece::BLACK);
    board.setPiece(0, 1, Board::Piece::BLACK);
    board.setPiece(8, 8, Board::Piece::WHITE);
    
    // Verify game is not over with 2 black pieces
    EXPECT_FALSE(board.isGameOver());
    
    // Remove one black piece to create win condition
    board.setPiece(0, 1, Board::Piece::EMPTY);
    EXPECT_TRUE(board.isGameOver());
}