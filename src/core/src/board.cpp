#include "board.hpp"
#include <sstream>
#include <stdexcept>

namespace hasami_shogi {

Board::Board() : board(BOARD_SIZE, std::vector<Piece>(BOARD_SIZE, Piece::EMPTY)) {
    resetBoard();
}

void Board::resetBoard() {
    // Clear the board
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            board[i][j] = Piece::EMPTY;
        }
    }
    
    // Set up initial positions
    for (int j = 0; j < BOARD_SIZE; ++j) {
        board[0][j] = Piece::BLACK;  // Black pieces on top
        board[BOARD_SIZE-1][j] = Piece::WHITE;  // White pieces on bottom
    }
}

Board::Piece Board::getPiece(int row, int col) const {
    if (!isInBounds(row, col)) {
        throw std::out_of_range("Position out of bounds");
    }
    return board[row][col];
}

bool Board::setPiece(int row, int col, Piece piece) {
    if (!isInBounds(row, col)) {
        return false;
    }
    board[row][col] = piece;
    return true;
}

bool Board::isEmpty(int row, int col) const {
    return getPiece(row, col) == Piece::EMPTY;
}

bool Board::isValidPosition(int row, int col) const {
    return isInBounds(row, col);
}

bool Board::isValidMove(int fromRow, int fromCol, int toRow, int toCol, Piece player) const {
    // Check if positions are valid
    if (!isInBounds(fromRow, fromCol) || !isInBounds(toRow, toCol)) {
        return false;
    }
    
    // Check if the piece belongs to the current player
    if (board[fromRow][fromCol] != player) {
        return false;
    }
    
    // Check if destination is empty
    if (board[toRow][toCol] != Piece::EMPTY) {
        return false;
    }
    
    // Check if move is either horizontal or vertical
    if (fromRow != toRow && fromCol != toCol) {
        return false;
    }
    
    // Check if path is clear
    return isPathClear(fromRow, fromCol, toRow, toCol);
}

bool Board::isPathClear(int fromRow, int fromCol, int toRow, int toCol) const {
    // Moving horizontally
    if (fromRow == toRow) {
        int start = std::min(fromCol, toCol) + 1;
        int end = std::max(fromCol, toCol);
        for (int col = start; col < end; ++col) {
            if (!isEmpty(fromRow, col)) return false;
        }
    }
    // Moving vertically
    else {
        int start = std::min(fromRow, toRow) + 1;
        int end = std::max(fromRow, toRow);
        for (int row = start; row < end; ++row) {
            if (!isEmpty(row, fromCol)) return false;
        }
    }
    return true;
}

bool Board::checkCaptures(int row, int col, Piece player) {
    bool captured = false;
    captured |= checkHorizontalCapture(row, col, player);
    captured |= checkVerticalCapture(row, col, player);
    return captured;
}

bool Board::checkHorizontalCapture(int row, int col, Piece player) {
    bool captured = false;
    Piece opponent = (player == Piece::BLACK) ? Piece::WHITE : Piece::BLACK;
    
    // Check left side
    if (col >= 2) {
        if (board[row][col-1] == opponent && board[row][col-2] == player) {
            board[row][col-1] = Piece::EMPTY;
            captured = true;
        }
    }
    
    // Check right side
    if (col <= BOARD_SIZE-3) {
        if (board[row][col+1] == opponent && board[row][col+2] == player) {
            board[row][col+1] = Piece::EMPTY;
            captured = true;
        }
    }
    
    return captured;
}

bool Board::checkVerticalCapture(int row, int col, Piece player) {
    bool captured = false;
    Piece opponent = (player == Piece::BLACK) ? Piece::WHITE : Piece::BLACK;
    
    // Check above
    if (row >= 2) {
        if (board[row-1][col] == opponent && board[row-2][col] == player) {
            board[row-1][col] = Piece::EMPTY;
            captured = true;
        }
    }
    
    // Check below
    if (row <= BOARD_SIZE-3) {
        if (board[row+1][col] == opponent && board[row+2][col] == player) {
            board[row+1][col] = Piece::EMPTY;
            captured = true;
        }
    }
    
    return captured;
}

bool Board::isInBounds(int row, int col) const {
    return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE;
}

std::vector<std::pair<int, int>> Board::getValidMoves(int row, int col) const {
    std::vector<std::pair<int, int>> moves;
    
    if (!isInBounds(row, col) || isEmpty(row, col)) {
        return moves;
    }
    
    // Check horizontal moves
    for (int c = 0; c < BOARD_SIZE; ++c) {
        if (c != col && isEmpty(row, c) && isPathClear(row, col, row, c)) {
            moves.emplace_back(row, c);
        }
    }
    
    // Check vertical moves
    for (int r = 0; r < BOARD_SIZE; ++r) {
        if (r != row && isEmpty(r, col) && isPathClear(row, col, r, col)) {
            moves.emplace_back(r, col);
        }
    }
    
    return moves;
}

std::string Board::toString() const {
    std::stringstream ss;
    ss << "  0 1 2 3 4 5 6 7 8\n";
    for (int i = 0; i < BOARD_SIZE; ++i) {
        ss << i << " ";
        for (int j = 0; j < BOARD_SIZE; ++j) {
            switch (board[i][j]) {
                case Piece::EMPTY: ss << ". "; break;
                case Piece::BLACK: ss << "B "; break;
                case Piece::WHITE: ss << "W "; break;
            }
        }
        ss << "\n";
    }
    return ss.str();
}

std::vector<std::vector<Board::Piece>> Board::getBoardState() const {
    return board;
}

} // namespace hasami_shogi