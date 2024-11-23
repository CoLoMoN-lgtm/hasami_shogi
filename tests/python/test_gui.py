import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from game_window import GameWindow
from board_widget import BoardWidget

@pytest.fixture
def app(qtbot):
    return QApplication([])

@pytest.fixture
def window(qtbot):
    window = GameWindow()
    qtbot.addWidget(window)
    return window

def test_window_creation(window):
    """Test if the main window is created properly"""
    assert window.windowTitle() == 'Hasami Shogi'
    assert window.board_widget is not None
    assert window.isVisible()

def test_new_game(window, qtbot):
    """Test new game functionality"""
    qtbot.mouseClick(window.new_game_btn, Qt.MouseButton.LeftButton)
    assert window.game_lib.getCurrentPlayer() == 0  # Black should start
    assert window.status_label.text() == "Status: Game in progress"

def test_game_modes(window, qtbot):
    """Test switching between game modes"""
    window.showSettings()
    settings_dialog = window.findChild(QDialog)
    
    # Switch to PvE mode
    qtbot.mouseClick(settings_dialog.pve_radio, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(settings_dialog.medium_radio, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(settings_dialog.buttons.button(QDialogButtonBox.StandardButton.Ok),
                    Qt.MouseButton.LeftButton)
    
    assert window.game_mode == 'PVE'
    assert window.ai_difficulty == 'Medium'

def test_board_interaction(window, qtbot):
    """Test board clicking and piece movement"""
    # Click black piece
    qtbot.mouseClick(window.board_widget, Qt.MouseButton.LeftButton,
                    pos=QPoint(45, 45))  # Click first black piece
    
    assert window.board_widget.selected_cell is not None
    
    # Click valid destination
    qtbot.mouseClick(window.board_widget, Qt.MouseButton.LeftButton,
                    pos=QPoint(45, 145))  # Click empty cell below
    
    assert window.board_widget.selected_cell is None
    assert window.game_lib.getCurrentPlayer() == 1  # Should be White's turn

def test_invalid_moves(window, qtbot):
    """Test that invalid moves are not allowed"""
    # Click white piece when it's black's turn
    qtbot.mouseClick(window.board_widget, Qt.MouseButton.LeftButton,
                    pos=QPoint(45, 445))  # Click white piece
    
    assert window.board_widget.selected_cell is None
    assert window.game_lib.getCurrentPlayer() == 0  # Should still be Black's turn

def test_game_over_detection(window):
    """Test if game over is detected correctly"""
    # Set up a winning position
    for i in range(8):
        window.game_lib.getBoard().setPiece(i, 0, Board::Piece::EMPTY)

    # Should trigger game over
    window.updateStatus()
    assert "wins" in window.status_label.text()