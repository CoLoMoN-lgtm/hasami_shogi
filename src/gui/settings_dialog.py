from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Game Settings')
        layout = QVBoxLayout(self)
        
        # Game mode selection
        mode_group = QGroupBox("Game Mode")
        mode_layout = QVBoxLayout()
        
        self.pvp_radio = QRadioButton("Player vs Player")
        self.pve_radio = QRadioButton("Player vs AI")
        
        if getattr(self.parent, 'game_mode', 'PVP') == 'PVP':
            self.pvp_radio.setChecked(True)
        else:
            self.pve_radio.setChecked(True)
        
        mode_layout.addWidget(self.pvp_radio)
        mode_layout.addWidget(self.pve_radio)
        mode_group.setLayout(mode_layout)
        
        # AI difficulty selection
        difficulty_group = QGroupBox("AI Difficulty")
        difficulty_layout = QVBoxLayout()
        
        self.easy_radio = QRadioButton("Easy")
        self.medium_radio = QRadioButton("Medium")
        self.hard_radio = QRadioButton("Hard")
        
        current_difficulty = getattr(self.parent, 'ai_difficulty', 'Medium')
        if current_difficulty == 'Easy':
            self.easy_radio.setChecked(True)
        elif current_difficulty == 'Medium':
            self.medium_radio.setChecked(True)
        else:
            self.hard_radio.setChecked(True)
        
        difficulty_layout.addWidget(self.easy_radio)
        difficulty_layout.addWidget(self.medium_radio)
        difficulty_layout.addWidget(self.hard_radio)
        difficulty_group.setLayout(difficulty_layout)
        
        # Game variant selection
        variant_group = QGroupBox("Game Variant")
        variant_layout = QVBoxLayout()
        
        variant_header = QHBoxLayout()
        self.standard_radio = QRadioButton("Standard Rules")
        self.modified_radio = QRadioButton("Modified Rules")
        self.rules_info_btn = QPushButton("?")
        self.rules_info_btn.setMaximumWidth(30)
        self.rules_info_btn.clicked.connect(self.showVariantRules)
        
        variant_header.addWidget(self.standard_radio)
        variant_header.addWidget(self.modified_radio)
        variant_header.addWidget(self.rules_info_btn)
        
        variant_layout.addLayout(variant_header)
        variant_group.setLayout(variant_layout)
        
        if getattr(self.parent, 'variant', 'Standard') == 'Standard':
            self.standard_radio.setChecked(True)
        else:
            self.modified_radio.setChecked(True)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal, 
            self
        )
        
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        # Add all widgets to main layout
        layout.addWidget(mode_group)
        layout.addWidget(difficulty_group)
        layout.addWidget(variant_group)
        layout.addWidget(buttons)
        
        # Enable/disable difficulty settings based on game mode
        self.pvp_radio.toggled.connect(lambda checked: difficulty_group.setEnabled(not checked))
        difficulty_group.setEnabled(not self.pvp_radio.isChecked())
    
    def showVariantRules(self):
        variant_rules = """
Модифіковані правила включають:

1. Додаткове захоплення по діагоналі
- Фігури можуть захоплювати не тільки по горизонталі та вертикалі, 
  але й по діагоналі, якщо вони затискають фігуру суперника.

2. Перестрибування через свої фігури
- Фігура може перестрибнути через одну свою фігуру, 
  якщо за нею є вільна клітинка.

3. Спеціальні клітинки
- Захисна клітинка: захищає фігуру від захоплення на один хід
- Бонусна клітинка: дозволяє зробити додатковий хід
- Атакуюча клітинка: дозволяє захопити фігуру без формування "затиску"

Ці модифікації додають нові стратегічні можливості до гри."""
        QMessageBox.information(self, "Variant Rules", variant_rules)
    
    def getGameMode(self):
        return 'PVP' if self.pvp_radio.isChecked() else 'PVE'
    
    def getAIDifficulty(self):
        if self.easy_radio.isChecked():
            return 'Easy'
        elif self.medium_radio.isChecked():
            return 'Medium'
        return 'Hard'
    
    def getVariant(self):
        return 'Standard' if self.standard_radio.isChecked() else 'Modified'