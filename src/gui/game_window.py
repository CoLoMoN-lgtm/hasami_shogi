from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from .board_widget import BoardWidget
from .settings_dialog import SettingsDialog
import copy

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize game settings
        self.game_mode = 'PVP'
        self.ai_difficulty = 'Medium'
        self.variant = 'Standard'
        self.current_player = 'Black'
        
        # Create initial board state
        self.board_state = [[0 for _ in range(9)] for _ in range(9)]
        self.move_history = []
        
        # Create UI
        self.setupUI()
        
        # Start new game
        self.setupNewGame()

    def setupUI(self):

        self.setWindowTitle('Hasami Shogi')
        self.setMinimumSize(800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create board widget
        self.board_widget = BoardWidget(self)
        layout.addWidget(self.board_widget)

        # Create control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # Game info group
        info_group = QGroupBox("Game Info")
        info_layout = QVBoxLayout()
        self.player_label = QLabel("Current Player: Black")
        self.status_label = QLabel("Status: Game in progress")
        info_layout.addWidget(self.player_label)
        info_layout.addWidget(self.status_label)
        info_group.setLayout(info_layout)

        # Control buttons
        button_group = QVBoxLayout()
        button_group.addStretch()

        button_style = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """

        # Create and style buttons
        self.new_game_btn = QPushButton("New Game")
        self.undo_btn = QPushButton("Undo Move")
        self.settings_btn = QPushButton("Settings")
        self.rules_btn = QPushButton("Show Rules")
        self.quit_btn = QPushButton("Quit")

        for btn in [self.new_game_btn, self.undo_btn, self.settings_btn, 
                   self.rules_btn, self.quit_btn]:
            btn.setStyleSheet(button_style)
            btn.setFixedHeight(40)
            button_group.addWidget(btn)
            button_group.addSpacing(10)

        # Connect buttons
        self.new_game_btn.clicked.connect(self.setupNewGame)
        self.undo_btn.clicked.connect(self.undoMove)
        self.settings_btn.clicked.connect(self.showSettings)
        self.rules_btn.clicked.connect(self.showRules)
        self.quit_btn.clicked.connect(self.close)

        button_group.addStretch()

        # Add widgets to layout
        control_layout.addWidget(info_group)
        control_layout.addLayout(button_group)
        control_panel.setLayout(control_layout)
        control_panel.setFixedWidth(200)

        layout.addWidget(control_panel)

        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QGroupBox {
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                margin-top: 10px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QLabel {
                color: white;
            }
        """)

    def setupNewGame(self):
        # Reset board state
        self.board_state = [[0 for _ in range(9)] for _ in range(9)]
        
        # Place initial pieces
        for col in range(9):
            self.board_state[0][col] = 1  # Black pieces
            self.board_state[8][col] = 2  # White pieces
        
        # Reset game state
        self.current_player = 'Black'
        self.move_history = []
        
        # Update display
        self.updateBoard()
        self.updateStatus()

    def updateBoard(self):
        self.board_widget.updateBoardState(self.board_state)

    def updateStatus(self):
        self.player_label.setText(f"Current Player: {self.current_player}")
        
        # Check for win conditions
        black_pieces = sum(row.count(1) for row in self.board_state)
        white_pieces = sum(row.count(2) for row in self.board_state)
        
        if black_pieces <= 1:
            self.status_label.setText("Status: White wins!")
        elif white_pieces <= 1:
            self.status_label.setText("Status: Black wins!")
        else:
            self.status_label.setText("Status: Game in progress")
        
        self.undo_btn.setEnabled(len(self.move_history) > 0)

    def makeMove(self, fromRow, fromCol, toRow, toCol):
        if not self.isValidMove(fromRow, fromCol, toRow, toCol):
            return False
            
        # Save current state for undo
        self.move_history.append({
            'board_state': copy.deepcopy(self.board_state),
            'current_player': self.current_player
        })
        
        # Make the move
        piece = self.board_state[fromRow][fromCol]
        self.board_state[fromRow][fromCol] = 0
        self.board_state[toRow][toCol] = piece
        
        # Check for captures
        self.checkCaptures(toRow, toCol)
        
        # Switch players
        self.current_player = 'White' if self.current_player == 'Black' else 'Black'
        
        # Update display
        self.updateBoard()
        self.updateStatus()
        
        return True

    def undoMove(self):
        if not self.move_history:
            return
            
        # Restore previous state
        previous_state = self.move_history.pop()
        self.board_state = previous_state['board_state']
        self.current_player = previous_state['current_player']
        
        # Update display
        self.updateBoard()
        self.updateStatus()

    def isValidMove(self, fromRow, fromCol, toRow, toCol):
        # Check if coordinates are valid
        if not (0 <= fromRow < 9 and 0 <= fromCol < 9 and 
                0 <= toRow < 9 and 0 <= toCol < 9):
            return False
            
        # Check if moving own piece
        piece = self.board_state[fromRow][fromCol]
        if ((self.current_player == 'Black' and piece != 1) or 
            (self.current_player == 'White' and piece != 2)):
            return False
            
        # Check if destination is empty
        if self.board_state[toRow][toCol] != 0:
            return False
            
        # Handle modified rules
        if self.variant == 'Modified':
            # Allow diagonal moves
            if abs(fromRow - toRow) == abs(fromCol - toCol):
                return self.isPathClear(fromRow, fromCol, toRow, toCol)
                
            # Allow jumping over own pieces
            if self.canJumpOverOwnPiece(fromRow, fromCol, toRow, toCol):
                return True
        
        # Standard orthogonal moves
        if fromRow != toRow and fromCol != toCol:
            return False
            
        return self.isPathClear(fromRow, fromCol, toRow, toCol)

    def isPathClear(self, fromRow, fromCol, toRow, toCol):
        if fromRow == toRow:  # Horizontal move
            start = min(fromCol, toCol) + 1
            end = max(fromCol, toCol)
            return all(self.board_state[fromRow][col] == 0 
                      for col in range(start, end))
        else:  # Vertical move
            start = min(fromRow, toRow) + 1
            end = max(fromRow, toRow)
            return all(self.board_state[row][fromCol] == 0 
                      for row in range(start, end))

    def canJumpOverOwnPiece(self, fromRow, fromCol, toRow, toCol):
        piece = self.board_state[fromRow][fromCol]
        
        # Check horizontal jump
        if fromRow == toRow and abs(fromCol - toCol) == 2:
            middle_col = (fromCol + toCol) // 2
            return self.board_state[fromRow][middle_col] == piece
            
        # Check vertical jump
        if fromCol == toCol and abs(fromRow - toRow) == 2:
            middle_row = (fromRow + toRow) // 2
            return self.board_state[middle_row][fromCol] == piece
            
        return False

    def checkCaptures(self, row, col):
        piece = self.board_state[row][col]
        opponent = 2 if piece == 1 else 1
        
        # Check all directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Orthogonal
        if self.variant == 'Modified':
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal
            
        for drow, dcol in directions:
            self.checkLineCaptures(row, col, drow, dcol)

    def checkLineCaptures(self, row, col, drow, dcol):
        piece = self.board_state[row][col]
        opponent = 2 if piece == 1 else 1
        
        captured = []
        r, c = row + drow, col + dcol
        
        # Find opponent pieces
        while (0 <= r < 9 and 0 <= c < 9 and 
               self.board_state[r][c] == opponent):
            captured.append((r, c))
            r, c = r + drow, c + dcol
            
        # Check if captured pieces are sandwiched
        if (0 <= r < 9 and 0 <= c < 9 and 
            self.board_state[r][c] == piece and captured):
            # Remove captured pieces
            for cr, cc in captured:
                self.board_state[cr][cc] = 0

    def showSettings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.game_mode = dialog.getGameMode()
            self.ai_difficulty = dialog.getAIDifficulty()
            self.variant = dialog.getVariant()
            self.setupNewGame()

    def showRules(self):
        rules_text = """
Hasami Shogi - Правила гри

Стандартні правила:
1. Мета гри - захопити всі фігури суперника, окрім однієї.
2. Фігури можуть рухатися по горизонталі та вертикалі на будь-яку кількість вільних клітин.
3. Захоплення відбувається, коли фігура суперника опиняється між двома вашими фігурами:
   - по горизонталі
   - по вертикалі
4. Можна захопити декілька фігур одним ходом.
5. Чорні ходять першими.

Модифіковані правила:
1. Додаткове захоплення по діагоналі.
2. Можливість "перестрибувати" через одну свою фігуру.
3. Спеціальні клітинки на дошці, які дають додаткові можливості:
   - захист від захоплення на один хід
   - можливість зробити додатковий хід
   - можливість захопити фігуру без формування "затиску"
"""
        QMessageBox.information(self, "Game Rules", rules_text)

    def getCurrentPlayer(self):
        return self.current_player

    def makeAIMove(self):
        """Make AI move based on current difficulty"""
        if self.current_player != 'White' or self.game_mode != 'PVE':
            return

        move = self.getAIMove()
        if move:
            fromRow, fromCol, toRow, toCol = move
            self.makeMove(fromRow, fromCol, toRow, toCol)

    def getAIMove(self):
        """Get best move based on current difficulty"""
        if self.ai_difficulty == 'Easy':
            return self.getRandomMove()
        elif self.ai_difficulty == 'Medium':
            return self.getMediumMove()
        else:
            return self.getHardMove()

    def getRandomMove(self):
        """Get random valid move"""
        import random
        possible_moves = []
        
        # Collect all valid moves
        for fromRow in range(9):
            for fromCol in range(9):
                if self.board_state[fromRow][fromCol] == 2:  # White piece
                    for toRow in range(9):
                        for toCol in range(9):
                            if self.isValidMove(fromRow, fromCol, toRow, toCol):
                                possible_moves.append((fromRow, fromCol, toRow, toCol))
        
        if possible_moves:
            return random.choice(possible_moves)
        return None

    def getMediumMove(self):
        """Get move with basic strategy"""
        best_move = None
        best_score = float('-inf')
        
        for fromRow in range(9):
            for fromCol in range(9):
                if self.board_state[fromRow][fromCol] == 2:  # White piece
                    for toRow in range(9):
                        for toCol in range(9):
                            if self.isValidMove(fromRow, fromCol, toRow, toCol):
                                # Try move
                                score = self.evaluateMove(fromRow, fromCol, toRow, toCol)
                                if score > best_score:
                                    best_score = score
                                    best_move = (fromRow, fromCol, toRow, toCol)
        
        return best_move

    def getHardMove(self):
        """Get best move using minimax algorithm"""
        def minimax(depth, alpha, beta, maximizing_player):
            if depth == 0:
                return self.evaluatePosition()
            
            if maximizing_player:
                max_eval = float('-inf')
                for move in self.getAllPossibleMoves(2):  # White pieces
                    # Make move
                    fromRow, fromCol, toRow, toCol = move
                    backup = self.makeTemporaryMove(fromRow, fromCol, toRow, toCol)
                    
                    eval = minimax(depth - 1, alpha, beta, False)
                    
                    # Undo move
                    self.undoTemporaryMove(backup)
                    
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval
            else:
                min_eval = float('inf')
                for move in self.getAllPossibleMoves(1):  # Black pieces
                    # Make move
                    fromRow, fromCol, toRow, toCol = move
                    backup = self.makeTemporaryMove(fromRow, fromCol, toRow, toCol)
                    
                    eval = minimax(depth - 1, alpha, beta, True)
                    
                    # Undo move
                    self.undoTemporaryMove(backup)
                    
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval

        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self.getAllPossibleMoves(2):  # White pieces
            fromRow, fromCol, toRow, toCol = move
            backup = self.makeTemporaryMove(fromRow, fromCol, toRow, toCol)
            
            value = minimax(3, alpha, beta, False)  # Depth = 3
            
            self.undoTemporaryMove(backup)
            
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_move

    def evaluatePosition(self):
        """Evaluate current board position"""
        # Count pieces
        white_pieces = sum(row.count(2) for row in self.board_state)
        black_pieces = sum(row.count(1) for row in self.board_state)
        
        # Basic material score
        score = (white_pieces - black_pieces) * 100
        
        # Add positional bonus
        for row in range(9):
            for col in range(9):
                if self.board_state[row][col] == 2:  # White piece
                    # Bonus for controlling center
                    center_distance = abs(4 - row) + abs(4 - col)
                    score += (8 - center_distance) * 5
                elif self.board_state[row][col] == 1:  # Black piece
                    center_distance = abs(4 - row) + abs(4 - col)
                    score -= (8 - center_distance) * 5
        
        return score

    def evaluateMove(self, fromRow, fromCol, toRow, toCol):
        """Evaluate a single move"""
        score = 0
        
        # Try the move
        backup = self.makeTemporaryMove(fromRow, fromCol, toRow, toCol)
        
        # Check for captures
        captured = self.countPotentialCaptures(toRow, toCol)
        score += captured * 100
        
        # Position evaluation
        center_distance = abs(4 - toRow) + abs(4 - toCol)
        score += (8 - center_distance) * 5
        
        # Undo the move
        self.undoTemporaryMove(backup)
        
        return score

    def makeTemporaryMove(self, fromRow, fromCol, toRow, toCol):
        """Make a temporary move and return backup for undoing"""
        backup = {
            'board_state': copy.deepcopy(self.board_state),
            'current_player': self.current_player
        }
        
        # Make move
        piece = self.board_state[fromRow][fromCol]
        self.board_state[fromRow][fromCol] = 0
        self.board_state[toRow][toCol] = piece
        
        # Check captures
        self.checkCaptures(toRow, toCol)
        
        return backup

    def undoTemporaryMove(self, backup):
        """Restore position from backup"""
        self.board_state = backup['board_state']
        self.current_player = backup['current_player']

    def getAllPossibleMoves(self, piece):
        """Get all possible moves for given piece"""
        moves = []
        for fromRow in range(9):
            for fromCol in range(9):
                if self.board_state[fromRow][fromCol] == piece:
                    for toRow in range(9):
                        for toCol in range(9):
                            if self.isValidMove(fromRow, fromCol, toRow, toCol):
                                moves.append((fromRow, fromCol, toRow, toCol))
        return moves

    def countPotentialCaptures(self, row, col):
        """Count how many pieces would be captured from a position"""
        piece = self.board_state[row][col]
        opponent = 1 if piece == 2 else 2
        count = 0
        
        # Check all directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if self.variant == 'Modified':
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for drow, dcol in directions:
            r, c = row + drow, col + dcol
            captured = []
            
            while 0 <= r < 9 and 0 <= c < 9 and self.board_state[r][c] == opponent:
                captured.append((r, c))
                r, c = r + drow, c + dcol
            
            if 0 <= r < 9 and 0 <= c < 9 and self.board_state[r][c] == piece:
                count += len(captured)
        
        return count
    def getAllPossibleMoves(self, player):
        moves = []
        piece = 2 if player == 'White' else 1

        for fromRow in range(9):
            for fromCol in range(9):
                if self.board_state[fromRow][fromCol] == piece:
                    # Check horizontal moves
                    for toCol in range(9):
                        if toCol != fromCol and self.isValidMove(fromRow, fromCol, fromRow, toCol):
                            moves.append((fromRow, fromCol, fromRow, toCol))
                    
                    # Check vertical moves
                    for toRow in range(9):
                        if toRow != fromRow and self.isValidMove(fromRow, fromCol, toRow, fromCol):
                            moves.append((fromRow, fromCol, toRow, fromCol))

        return moves

def newGame(self):
    self.board_state = [[0 for _ in range(9)] for _ in range(9)]
    for col in range(9):
        self.board_state[0][col] = 1  # Black pieces
        self.board_state[8][col] = 2  # White pieces
        
    self.current_player = 'Black'
    self.move_history = []
        
    self.updateBoard()
    self.updateStatus()
        
    print(f"New game started - Mode: {self.game_mode}, Difficulty: {self.ai_difficulty}")

    def makeMove(self, fromRow, fromCol, toRow, toCol):
        try:
            print(f"Attempting move: {fromRow},{fromCol} -> {toRow},{toCol}")
            
            if not self.isValidMove(fromRow, fromCol, toRow, toCol):
                print("Invalid move")
                return False

            # Save move for undo
            self.move_history.append({
                'fromRow': fromRow,
                'fromCol': fromCol,
                'toRow': toRow,
                'toCol': toCol,
                'piece': self.board_state[fromRow][fromCol],
                'board_state': copy.deepcopy(self.board_state)
            })

            # Make the move
            piece = self.board_state[fromRow][fromCol]
            self.board_state[fromRow][fromCol] = 0
            self.board_state[toRow][toCol] = piece

            # Check for captures
            captures = self.checkCaptures(toRow, toCol)

            # Switch players
            self.current_player = 'White' if self.current_player == 'Black' else 'Black'

            # Update display
            self.updateBoard()
            self.updateStatus()

            # Make AI move if needed
            if self.game_mode == 'PVE' and self.current_player == 'White':
                QTimer.singleShot(500, self.makeAIMove)  # Delay AI move for better UX

            return True

        except Exception as e:
            print(f"Error making move: {e}")
            print(traceback.format_exc())
            QMessageBox.warning(self, "Invalid Move", str(e))
            return False

    def undoMove(self):
        if not self.move_history:
            return
        
        # If playing against AI, undo both player's and AI's moves
        if self.game_mode == 'PVE':
            if len(self.move_history) >= 2:
                # Undo AI move
                last_state = self.move_history.pop()
                self.board_state = last_state['board_state']
                # Undo player move
                last_state = self.move_history.pop()
                self.board_state = last_state['board_state']
                self.current_player = 'Black'
        else:
            # Undo last move in PVP mode
            last_state = self.move_history.pop()
            self.board_state = last_state['board_state']
            self.current_player = 'Black' if self.current_player == 'White' else 'White'
            
        self.updateBoard()
        self.updateStatus()

    def isValidMove(self, fromRow, fromCol, toRow, toCol):
        # Check if coordinates are valid
        if not (0 <= fromRow < 9 and 0 <= fromCol < 9 and 0 <= toRow < 9 and 0 <= toCol < 9):
            return False
            
        # Check if moving own piece
        piece = self.board_state[fromRow][fromCol]
        if (self.current_player == 'Black' and piece != 1) or \
           (self.current_player == 'White' and piece != 2):
            return False
            
        # Check if destination is empty
        if self.board_state[toRow][toCol] != 0:
            return False
            
        # Handle modified rules
        if self.variant == 'Modified':
            # Allow diagonal moves
            if abs(fromRow - toRow) == abs(fromCol - toCol):
                return self.isPathClear(fromRow, fromCol, toRow, toCol)
                
            # Allow jumping over one own piece
            if self.canJumpOverOwnPiece(fromRow, fromCol, toRow, toCol):
                return True
        
        # Standard orthogonal moves
        if fromRow != toRow and fromCol != toCol:
            return False
            
        return self.isPathClear(fromRow, fromCol, toRow, toCol)

    def isPathClear(self, fromRow, fromCol, toRow, toCol):
    # For diagonal moves
        if abs(fromRow - toRow) == abs(fromCol - toCol):
            rowStep = 1 if toRow > fromRow else -1
            colStep = 1 if toCol > fromCol else -1
            
            row, col = fromRow + rowStep, fromCol + colStep
            while row != toRow and col != toCol:
                if self.board_state[row][col] != 0:
                    return False
                row += rowStep
                col += colStep
            return True
            
        # For orthogonal moves
        if fromRow == toRow:  # Horizontal move
            start = min(fromCol, toCol) + 1
            end = max(fromCol, toCol)
            return all(self.board_state[fromRow][col] == 0 for col in range(start, end))
        else:  # Vertical move
            start = min(fromRow, toRow) + 1
            end = max(fromRow, toRow)
            return all(self.board_state[row][fromCol] == 0 for row in range(start, end))

    def canJumpOverOwnPiece(self, fromRow, fromCol, toRow, toCol):
        # Only for modified rules
        if self.variant != 'Modified':
            return False
            
        piece = self.board_state[fromRow][fromCol]
        
        # Check horizontal jump
        if fromRow == toRow and abs(fromCol - toCol) == 2:
            middle_col = (fromCol + toCol) // 2
            return self.board_state[fromRow][middle_col] == piece
            
        # Check vertical jump
        if fromCol == toCol and abs(fromRow - toRow) == 2:
            middle_row = (fromRow + toRow) // 2
        return self.board_state[middle_row][fromCol] == piece
            
        return False

    def checkCaptures(self, row, col):
        piece = self.board_state[row][col]
        opponent = 2 if piece == 1 else 1
        captures = []
        
        # Standard captures (orthogonal)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if self.variant == 'Modified':
            # Add diagonal directions for modified rules
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
            
        for drow, dcol in directions:
            captured = self.checkLineCaptures(row, col, drow, dcol, opponent)
            captures.extend(captured)
        
        return captures

    def checkLineCaptures(self, row, col, drow, dcol, opponent):
        captured = []
        r, c = row + drow, col + dcol
        
        while 0 <= r < 9 and 0 <= c < 9 and self.board_state[r][c] == opponent:
            captured.append((r, c))
            r, c = r + drow, c + dcol
            
        if (0 <= r < 9 and 0 <= c < 9 and 
            self.board_state[r][c] == self.board_state[row][col] and 
            captured):
            # Remove captured pieces
            for cr, cc in captured:
                self.board_state[cr][cc] = 0
            return captured
            
        return []

    def updateBoard(self):
        self.board_widget.updateBoardState(self.board_state)

        def updateStatus(self):
            self.player_label.setText(f"Current Player: {self.current_player}")
    
        # Check win conditions
        black_pieces = sum(row.count(1) for row in self.board_state)
        white_pieces = sum(row.count(2) for row in self.board_state)
    
        if black_pieces <= 1:
            self.status_label.setText("Status: White wins!")
        elif white_pieces <= 1:
            self.status_label.setText("Status: Black wins!")
        else:
            self.status_label.setText("Status: Game in progress")
            
        self.undo_btn.setEnabled(len(self.move_history) > 0)

    def getCurrentPlayer(self):
        return self.current_player