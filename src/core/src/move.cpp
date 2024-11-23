#include "move.hpp"
#include <sstream>
#include <cstdlib>
#include <algorithm>

namespace hasami_shogi {

std::string Move::toString() const {
    std::stringstream ss;
    ss << "Move from (" << fromRow << "," << fromCol << ") to ("
       << toRow << "," << toCol << ")";
    return ss.str();
}

bool Move::isValid() const {
    // Check if coordinates are within board bounds
    if (fromRow < 0 || fromRow >= 9 || fromCol < 0 || fromCol >= 9 ||
        toRow < 0 || toRow >= 9 || toCol < 0 || toCol >= 9) {
        return false;
    }
    
    // Check if move is either horizontal or vertical
    if (fromRow != toRow && fromCol != toCol) {
        return false;
    }
    
    // Check that the move actually changes position
    if (fromRow == toRow && fromCol == toCol) {
        return false;
    }
    
    return true;
}

int Move::getDistance() const {
    if (fromRow == toRow) {
        return std::abs(toCol - fromCol);
    } else {
        return std::abs(toRow - fromRow);
    }
}

bool Move::isHorizontal() const {
    return fromRow == toRow;
}

bool Move::isVertical() const {
    return fromCol == toCol;
}

std::vector<std::pair<int, int>> Move::getPath() const {
    std::vector<std::pair<int, int>> path;
    
    if (isHorizontal()) {
        int start = std::min(fromCol, toCol);
        int end = std::max(fromCol, toCol);
        for (int col = start + 1; col < end; ++col) {
            path.emplace_back(fromRow, col);
        }
    } else {
        int start = std::min(fromRow, toRow);
        int end = std::max(fromRow, toRow);
        for (int row = start + 1; row < end; ++row) {
            path.emplace_back(row, fromCol);
        }
    }
    
    return path;
}

} // namespace hasami_shogi