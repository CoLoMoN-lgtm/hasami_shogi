#pragma once
#include <vector>
#include <optional>
#include <string>

namespace hasami_shogi {

class Board {
public:
    static const int BOARD_SIZE = 9;
    enum class Piece { EMPTY, BLACK, WHITE };
    
    Board();
    
    // Board state operations
    Piece getPiece(int row, int col) const;
    bool setPiece(int row, int col, Piece piece);
    bool isEmpty(int row, int col) const;
    bool isValidPosition(int row, int col) const;
    
    // Move validation
    bool isValidMove(int fromRow, int fromCol, int toRow, int toCol, Piece player) const;
    std::vector<std::pair<int, int>> getValidMoves(int row, int col) const;
    
    // Capture checking
    bool checkCaptures(int row, int col, Piece player);
    int removeCapturedPieces(Piece player);
    
    // Board state
    std::string toString() const;
    void resetBoard();
    std::vector<std::vector<Piece>> getBoardState() const;
    
private:
    std::vector<std::vector<Piece>> board;
    
    bool checkVerticalCapture(int row, int col, Piece player);
    bool checkHorizontalCapture(int row, int col, Piece player);
    bool isPathClear(int fromRow, int fromCol, int toRow, int toCol) const;
    bool isInBounds(int row, int col) const;
};

} // namespace hasami_shogi