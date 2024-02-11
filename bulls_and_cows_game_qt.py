#!/usr/bin/env python

import sys
import re
import random

# And this goes against the Python practices I guess. Problem is
# I want to make a Debian .deb package, but I am using Lubuntu 22.04 LTS
# and as of today this package is not yet available in the Debian repos
# for this version, so I put this here at least to be user-friendly to
# the users
ERRMSG = """ERROR: Python module PyQt6 is not installed.
Please read TROUBLESHOOTING.txt
(bulls_and_cows_game_qt.py)
"""
if "PyQt6" not in sys.modules:
    print(ERRMSG, file=sys.stderr)
    sys.exit(1)

from PyQt6 import QtCore, QtGui, QtWidgets
from game_layout import Ui_MainWindow
from help_about import Ui_DialogHelpAboutBC


VERSION = "1.0"
DATE = "2024-02-09"


# I wrote these classes for the command-line version


class BCNumber:
    """Bulls and Cows Number class.

    REQUIREMENTS:
    1) Must contain exactly four digits
    2) All symbols must be digits
    3) All digits must be unique
    (no digit can repeat twice in the number)
    """

    def __init__(self, num: str) -> None:
        self._value: str = num

    def valid(self) -> bool:
        if len(str(self)) != 4 or not re.search(r"^[0-9]+$", str(self)):
            return False

        # After ensuring all symbols are digits,
        # we can convert them to a list of integers
        value_int = [int(x) for x in str(self)]
        if len(set(value_int)) != 4:
            return False

        return True

    def __repr__(self) -> str:
        return self._value


class NewNumberPicker:
    """Generates a new random four digit integer."""

    def __init__(self) -> None:
        self._value: int = self._pick()

    def _pick(self) -> int:
        """Picks and returns a random number."""
        return random.randint(101, 9999)

    def __repr__(self) -> str:
        return f"{self._value:04}"

    @property
    def value(self) -> str:
        return str(self)


class InputAnalyzer:
    def __init__(self, number: BCNumber, guess: BCNumber) -> None:
        self._value: str = self._analize(number, guess)

    def _analize(self, number: BCNumber, guess: BCNumber) -> str:
        bulls: int = 0
        cows: int = 0

        for i in range(4):
            if str(guess)[i] == str(number)[i]:
                bulls += 1
            elif str(guess)[i] in str(number):
                cows += 1

        return f"BULLS: {bulls}; COWS: {cows}"

    def __repr__(self) -> str:
        return self._value


class MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self._retries_count = 0
        self._secret_number = None
        self._game_end = False

    @property
    def gameEnd(self):
        return self._game_end

    @gameEnd.setter
    def gameEnd(self, x):
        if isinstance(x, bool):
            self._game_end = x
        else:
            raise ValueError("Not a boolean!")  # Just in case

    @property
    def secretNumber(self):
        return self.secret_number

    @secretNumber.setter
    def secretNumber(self, x):
        self.secret_number = x

    def pickASecretNumber(self):
        self.secretNumber = BCNumber(NewNumberPicker().value)

    @property
    def retries(self):
        return self._retries_count

    @retries.setter
    def retries(self, x):
        self._retries_count = x

    @property
    def errorTextStyle(self):
        return "style='color:red; font-size:12pt;'"

    @property
    def newgameTextStyle(self):
        return "style='color:blue; font-size:12pt;'"

    @property
    def msgTextStyle(self):
        return "style='font-size:12pt;'"

    def scrollAreaToBottom(self):
        self.resultsTextArea.verticalScrollBar().setValue(
            self.resultsTextArea.verticalScrollBar().maximum()
        )

    def appendToArea(self, message):
        self.scrollAreaToBottom()
        self.resultsTextArea.append(message)

    def clearUserGuess(self):
        self.userguessField.clear()
        self.buttonSubmit.setEnabled(False)

    def addToUserGuess(self, i):
        if (
            str(i) not in self.userguessField.text()
            and len(self.userguessField.text()) < 4
        ):
            self.userguessField.setText(f"{self.userguessField.text()}{i}")
            if len(self.userguessField.text()) == 4:
                self.buttonSubmit.setEnabled(True)
        elif len(self.userguessField.text()) == 4:
            self.appendToArea(f"<p {self.errorTextStyle}>Only 4 digits.</p>")
        elif str(i) in self.userguessField.text():
            self.appendToArea(f"<p {self.errorTextStyle}>No duplicates.</p>")

    def add0(self):
        self.addToUserGuess(0)

    def add1(self):
        self.addToUserGuess(1)

    def add2(self):
        self.addToUserGuess(2)

    def add3(self):
        self.addToUserGuess(3)

    def add4(self):
        self.addToUserGuess(4)

    def add5(self):
        self.addToUserGuess(5)

    def add6(self):
        self.addToUserGuess(6)

    def add7(self):
        self.addToUserGuess(7)

    def add8(self):
        self.addToUserGuess(8)

    def add9(self):
        self.addToUserGuess(9)

    def helpAboutDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_DialogHelpAboutBC()
        dialog.ui.setupUi(dialog)
        dialog.exec()
        dialog.show()
        dialog.move(0, 0)

    def endGame(self):
        self.gameEnd = True
        self.userguessField.clear()
        self.appendToArea(f"<p {self.newgameTextStyle}>YOU WON!</p>")
        self.appendToArea(f"<p {self.msgTextStyle}>Total retries: {self.retries}</p>")
        self.numbersFrame.setEnabled(False)
        self.buttonClear.setEnabled(False)
        self.buttonSubmit.setEnabled(False)

    def newGame(self):
        self.gameEnd = False
        self.userguessField.clear()
        self.appendToArea(
            f"<p {self.newgameTextStyle}>************ NEW GAME ************</p>"
        )
        self.retries = 0

        self.pickASecretNumber()
        while not self.secretNumber.valid():
            self.pickASecretNumber()
        self.appendToArea(f"<p {self.msgTextStyle}>Guess the new secret number!</p>")

        self.numbersFrame.setEnabled(True)
        self.buttonClear.setEnabled(True)
        self.buttonSubmit.setEnabled(False)

    def submitUserInput(self):
        self.buttonSubmit.setEnabled(False)
        self.retries += 1
        userInput = self.userguessField.text()
        userGuess = BCNumber(userInput)
        secretNumber = self.secretNumber

        self.userguessField.clear()

        analysis = str(InputAnalyzer(secretNumber, userGuess))

        self.appendToArea(
            f"<p {self.msgTextStyle}>[{self.retries}] {userGuess} -&gt; {analysis}</p>"
        )

        if str(secretNumber) == str(userGuess):
            self.endGame()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.button0.clicked.connect(self.add0)
        self.button1.clicked.connect(self.add1)
        self.button2.clicked.connect(self.add2)
        self.button3.clicked.connect(self.add3)
        self.button4.clicked.connect(self.add4)
        self.button5.clicked.connect(self.add5)
        self.button6.clicked.connect(self.add6)
        self.button7.clicked.connect(self.add7)
        self.button8.clicked.connect(self.add8)
        self.button9.clicked.connect(self.add9)

        self.buttonSubmit.clicked.connect(self.submitUserInput)
        self.buttonClear.clicked.connect(self.clearUserGuess)

        self.gameQuit.triggered.connect(sys.exit)
        self.helpAbout.triggered.connect(self.helpAboutDialog)
        self.gameNew.triggered.connect(self.newGame)

        self.appendToArea(f"<p style='font-size:10pt;'>Version {VERSION} ({DATE})</p>")

        self.newGame()


class Game:
    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        ui = MainWindow()
        ui.setupUi(mainWindow)
        mainWindow.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    game = Game()
    game.run()
