from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from os import path
import sys


# Import UI file
FORM_CLASS, QMainWindow = loadUiType(path.join(path.dirname(__file__), "GUI.ui"))


class TicTacToe(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(TicTacToe, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.board = [''] * 9
        self.current_player = None
        self.winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        )

        # handle buttons
        self.button_play.clicked.connect(self.start_game)  # play button
        self.button_quit.clicked.connect(self.close)  # exit button

        self.buttons = [
            self.spot_1, self.spot_2, self.spot_3,
            self.spot_4, self.spot_5, self.spot_6,
            self.spot_7, self.spot_8, self.spot_9
        ]

        # disable the buttons on start
        self.update_buttons_state(False)

        for button in self.buttons:
            button.clicked.connect(lambda _, btn=button: self.make_move(btn))

    def start_game(self):
        self.board = [''] * 9
        self.current_player = self.getSymbol()
        self.update_buttons_state(True)
        self.label_message.setText(self.current_player + "'s turn. Click a spot.")

        # Reset the options
        self.button_play.setEnabled(False)
        self.input_choice.setEnabled(False)

        for button in self.buttons:
            button.setText("")

    def getSymbol(self):
        # get the user choice
        choice = self.input_choice.currentText()

        # disable user input
        self.input_choice.setEnabled(False)

        return choice

    def ai_make_move(self):
        best_score = float('-inf')  # change to 'best_score = float(5)' for two players
        best_move = None

        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, False)
                self.board[i] = ''

                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.make_move(self.buttons[best_move])

    def make_move(self, button):
        index = self.buttons.index(button)

        if self.board[index] == '':
            self.board[index] = self.current_player
            button.setText(self.current_player)
            button.setEnabled(False)

            if self.check_winner(self.current_player):
                self.update_buttons_state(False)
                self.label_message.setText(f"{self.current_player} wins!")
            elif '' not in self.board:
                self.update_buttons_state(False)
                self.label_message.setText("It's a tie!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.label_message.setText(f"It's {self.current_player}'s turn.")

            if self.current_player == 'O' and '' in self.board:
                self.ai_make_move()

    def check_winner(self, player):
        for combination in self.winning_combinations:
            if all(self.board[i] == player for i in combination):
                self.button_play.setEnabled(True)
                return True
        return False

    def minimax(self, board, is_maximizing):
        scores = {'X': -1, 'O': 1, 'tie': 0}

        if self.check_winner('X'):
            return scores['X']
        elif self.check_winner('O'):
            return scores['O']
        elif '' not in board:
            return scores['tie']

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def update_buttons_state(self, enabled):
        for button in self.buttons:
            button.setEnabled(enabled)

    def closeEvent(self, event):
        # Override closeEvent to display a confirmation dialog
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.show()
    sys.exit(app.exec_())
