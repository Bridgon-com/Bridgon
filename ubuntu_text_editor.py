import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QTabWidget, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import Qt, QRegularExpression


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        self.highlight_rules = [
            (QRegularExpression("\\bclass\\b"), keyword_format),
            (QRegularExpression("\\bdef\\b"), keyword_format),
            (QRegularExpression("\\bimport\\b"), keyword_format),
            (QRegularExpression("\\bfrom\\b"), keyword_format),
            (QRegularExpression("\\breturn\\b"), keyword_format),
        ]

    def highlightBlock(self, text):
        for pattern, fmt in self.highlight_rules:
            expression = pattern.match(text)
            index = expression.capturedStart()
            while index >= 0:
                length = expression.capturedLength()
                self.setFormat(index, length, fmt)
                index = pattern.match(text, index + length).capturedStart()


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Monospace", 12))
        self.highlighter = SyntaxHighlighter(self.document())

    def resolve_cli_variables(self):
        text = self.toPlainText()
        resolved_text = os.path.expandvars(text)
        self.setPlainText(resolved_text)


class UbuntuTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ubuntu Text Editor")
        self.setGeometry(200, 200, 900, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_menu()
        self.new_tab()

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        resolve_vars_action = QAction("Resolve CLI Variables", self)
        resolve_vars_action.triggered.connect(self.resolve_cli_variables)
        file_menu.addAction(resolve_vars_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def new_tab(self):
        editor = CodeEditor()
        index = self.tabs.addTab(editor, "Untitled")
        self.tabs.setCurrentIndex(index)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Text Files (*.txt *.py *.cpp *.java);;All Files (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            editor = CodeEditor()
            editor.setText(text)
            index = self.tabs.addTab(editor, file_path.split("/")[-1])
            self.tabs.setCurrentIndex(index)

    def save_file(self):
        editor = self.tabs.currentWidget()
        if editor:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                       "Text Files (*.txt *.py *.cpp *.java);;All Files (*)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(editor.toPlainText())

    def save_file_as(self):
        self.save_file()

    def resolve_cli_variables(self):
        editor = self.tabs.currentWidget()
        if isinstance(editor, CodeEditor):
            editor.resolve_cli_variables()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = UbuntuTextEditor()
    editor.show()
    sys.exit(app.exec())
