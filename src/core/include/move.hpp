#pragma once
#include <string>
#include <vector>
#include <utility>

namespace hasami_shogi {

struct Move {
    int fromRow;
    int fromCol;
    int toRow;
    int toCol;
    
    Move(int fr = 0, int fc = 0, int tr = 0, int tc = 0)
        : fromRow(fr), fromCol(fc), toRow(tr), toCol(tc) {}
    
    bool operator==(const Move& other) const {
        return fromRow == other.fromRow && 
               fromCol == other.fromCol && 
               toRow == other.toRow && 
               toCol == other.toCol;
    }
    
    bool operator!=(const Move& other) const {
        return !(*this == other);
    }
    
    // Add these member function declarations
    std::string toString() const;
    bool isValid() const;
    int getDistance() const;
    bool isHorizontal() const;
    bool isVertical() const;
    std::vector<std::pair<int, int>> getPath() const;
};

} // namespace hasami_shogi