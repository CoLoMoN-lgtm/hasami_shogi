from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class BoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.selected_cell = None
        self.valid_moves = []
        self.board_state = [[0 for _ in range(9)] for _ in range(9)]
        self.initUI()

    def initUI(self):
        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: #2b2b2b;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate board size
        size = min(self.width(), self.height())
        cell_size = size / 9

        # Draw board background
        board_color = QColor('#DCB35C')  # Колір дошки
        painter.fillRect(0, 0, size, size, board_color)

        # Draw grid
        painter.setPen(QPen(QColor('#000000'), 1))
        for i in range(10):
            # Vertical lines
            x = int(i * cell_size)
            painter.drawLine(x, 0, x, size)
            # Horizontal lines
            painter.drawLine(0, x, size, x)

        # Draw pieces
        for row in range(9):
            for col in range(9):
                piece = self.board_state[row][col]
                if piece != 0:
                    x = int(col * cell_size)
                    y = int(row * cell_size)
                    center = QPointF(x + cell_size/2, y + cell_size/2)
                    radius = int(cell_size * 0.4)
                    
                    # Draw piece outline
                    painter.setPen(QPen(Qt.GlobalColor.black, 2))
                    if piece == 1:  # Black piece
                        painter.setBrush(QBrush(Qt.GlobalColor.black))
                    else:  # White piece
                        painter.setBrush(QBrush(Qt.GlobalColor.white))
                    painter.drawEllipse(center, radius, radius)

        # Highlight selected cell
        if self.selected_cell:
            row, col = self.selected_cell
            x = int(col * cell_size)
            y = int(row * cell_size)
            painter.fillRect(x, y, int(cell_size), int(cell_size), 
                           QColor(255, 255, 0, 100))

        # Highlight valid moves
        for row, col in self.valid_moves:
            x = int(col * cell_size)
            y = int(row * cell_size)
            painter.fillRect(x, y, int(cell_size), int(cell_size), 
                           QColor(0, 255, 0, 100))

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        # Calculate cell size
        size = min(self.width(), self.height())
        cell_size = size / 9

        # Get clicked cell
        col = int(event.position().x() // cell_size)
        row = int(event.position().y() // cell_size)

        if not (0 <= row < 9 and 0 <= col < 9):
            return

        # First click - select piece
        if self.selected_cell is None:
            if self.isValidPiece(row, col):
                self.selected_cell = (row, col)
                self.valid_moves = self.getValidMoves(row, col)
                self.update()
        # Second click - make move
        else:
            if (row, col) in self.valid_moves:
                from_row, from_col = self.selected_cell
                if self.parent.makeMove(from_row, from_col, row, col):
                    if self.parent.game_mode == 'PVE' and self.parent.current_player == 'White':
                        QTimer.singleShot(500, self.parent.makeAIMove)
            
            self.selected_cell = None
            self.valid_moves = []
            self.update()

    def isValidPiece(self, row, col):
        piece = self.board_state[row][col]
        current_player = self.parent.getCurrentPlayer()
        return ((piece == 1 and current_player == 'Black') or 
                (piece == 2 and current_player == 'White'))

    def getValidMoves(self, row, col):
        moves = []
        piece = self.board_state[row][col]

        # Check horizontal moves
        for c in range(9):
            if c != col:
                if self.parent.isValidMove(row, col, row, c):
                    moves.append((row, c))

        # Check vertical moves
        for r in range(9):
            if r != row:
                if self.parent.isValidMove(row, col, r, col):
                    moves.append((r, col))

        # If modified rules are enabled, add diagonal moves
        if self.parent.variant == 'Modified':
            # Add diagonal moves here
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 9 and 0 <= c < 9:
                    if self.parent.isValidMove(row, col, r, c):
                        moves.append((r, c))
                    r, c = r + dr, c + dc

        return moves

    def updateBoardState(self, state):
        self.board_state = state
        self.selected_cell = None
        self.valid_moves = []
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()