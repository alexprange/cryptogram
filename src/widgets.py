#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import string

from PyQt6.QtWidgets import (QComboBox, QLabel, QListWidgetItem,
                            QMenu, QListWidget, QListWidgetItem,
                            QPushButton, QTableWidget, QHeaderView,
                            QTableWidgetItem, QCheckBox, QSizePolicy)

from PyQt6.QtGui import QFont, QAction

from src.phrase import Phrase

ClassObject = None

# Sample Style Sheet
"""
    {
        background-color: #000000;
        background-repeat: repeat-y;
        background origin: content;
        border: 1px solid #000000;
        border-radius: 3px;
        color: #9FF;
        gridline-color: gray;  #QtableView Only
        font-style: bold;
        margin: 5px;
        padding: 5px;
        min-height: 100px;
        max-width: 100px;
        text-align: center;
        opacity: 223;
        selection-color: darkblue;
        selection-background-color: white;
    }
"""



class TableItem(QTableWidgetItem):

    def __init__(self,type=0):
        super().__init__(type=type)
        self.row = None
        self.column = None
        self._window = None

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def assign_location(self,row,column):
        self.row = row
        self.column = column

class Table(QTableWidget):
    styleSheet = "QTableWidget {background-color: white; gridline-color: #ddd; selection-color: #3bf}"

    def __init__(self,rows,columns,parent=None):
        super().__init__(rows,columns,parent=parent)
        self._window = None
        self.setObjectName("table")
        self.setHorizontalHeaderLabels(["OLD","NEW"])
        self.showGrid()
        self.setStyleSheet(self.styleSheet)
        self.setEditTriggers(QTableWidget.EditTriggers(0))
        headers = self.horizontalHeader()
        headers.setSectionResizeMode(0,QHeaderView.ResizeMode(1))
        headers.setSectionResizeMode(1,QHeaderView.ResizeMode(1))
        self.setSizePolicy(QSizePolicy.Policy(4),QSizePolicy.Policy(5))
        self.itemSelectionChanged.connect(self.select_row)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def get_contents(self):
        chars = {}
        for num in range(self.rowCount()):
            old = self.item(num,0).text()
            new = self.item(num,1).text()
            chars[old] = new
        return chars

    def select_row(self):
        row = self.currentRow()
        self.selectRow(row)

    def remove_row(self,row):
        self.removeRow(row)

    def remove_keys(self,chars):
        for num in list(range(0,self.rowCount()))[::-1]:
            if self.item(num,0).text() in chars:
                self.remove_row(num)

    def add_changes(self,changes):
        for k,v in changes.items():
            self.add_chars(k,v)

    def add_chars(self,old,new):
        row_num = self.rowCount()
        self.insertRow(row_num)
        for i,text in enumerate((old,new)):
            item = TableItem(type=0)
            item.setText(text)
            self.setItem(row_num,i,item)

class UpperComboBox(QComboBox):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("Upper_Combo_Box")
        self.addItems([i for i in string.ascii_uppercase])
        self.setEditable(False)
        self.setFont(BoldFont())

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

class BoldFont(QFont):

    def __init__(self):
        super().__init__()
        self.setBold(True)


class FileMenu(QMenu):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self._window = None
        self.setTitle("File")
        exit_action = QAction(parent=self)
        exit_action.setText("Exit")
        clear_action = QAction(parent=self)
        clear_action.setText("Clear")
        self.addAction(exit_action)
        self.addAction(clear_action)
        exit_action.triggered.connect(self.destroy)
        clear_action.triggered.connect(self.clear)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def destroy(self):
        sys.exit(self.parent.parent().app.exec)

    def clear(self):
        self.window().table.clear()
        self.window().word_list.clear()
        self.window().matches_list.clear()
        self.window().text_browser.clear()

class WordList(QListWidget):
    styleSheet = "QListWidget {background-color: white; selection-color: #17aee8; font-style: bold;}"

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setObjectName("Word_List")
        self._window = None
        self.currentItemChanged.connect(self.fill_matches)
        self.setStyleSheet(self.styleSheet)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def fill_matches(self):
        matches_list = self.window().matches_list
        if not matches_list:
            matches_list.clear()
        word = self.currentItem()
        matches = list(word.obj.matches)
        matches_list.add_items(matches)

    def add_items(self,items):
        for item in items:
            word = WordListItem(item,parent=self)
            self.addItem(word)

class WordListItem(QListWidgetItem):

    def __init__(self,obj,parent=None):
        super().__init__(parent=parent)
        self._word = None
        self.obj = obj
        self.setText(str(obj))
        self._window = None

    def setWord(self,word):
        self._word = word

    def getWord(self):
        return self._word

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def get_matches(self):
        if self.obj.matches:
            return list(self.object.matches)

class ChosenList(QListWidget):
    styleSheet = "QListWidget {background-color: white; selection-color: #17aee8; font-style: bold;}"

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setObjectName("Chosen_List")
        self._window = None
        self.internal = []
        self.setStyleSheet(self.styleSheet)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def add_item(self,match):
        if match not in self.internal:
            word = WordListItem(match,parent=self)
            self.internal.append(match)
            self.addItem(word)

    def remove_word(self):
        for item in self.selectedItems():
            self.internal.remove(item.text())
            row = self.indexFromItem(item).row()
            self.window().driver.undo_changes(item.text())
            self.takeItem(row)

    def remove_match(self,match):
        self.internal.remove(match)
        for row in range(self.count()):
            if self.item(row).text() == match:
                self.takeItem(row)
                self.window().driver.undo_changes(match)


class MatchesList(QListWidget):
    styleSheet = "QListWidget {background-color: white; selection-color: #17aee8; font-style: bold;}"

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setObjectName("Matches_List")
        self._window = None
        self.doubleClicked.connect(self.match_selected)

    def match_selected(self):
        match = self.currentItem()
        word = self.window().word_list.currentItem()
        self.window().driver.match_selected(word.text(),match.text())
        self.window().driver.decrypt()
        self.window().word_list.fill_matches()

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def add_items(self,items):
        self.clear()
        for item in items:
            self.addItem(item)


class SubmitPhraseButton(QPushButton):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("submit_phrase")
        self.setText("Submit Phrase")
        self.pressed.connect(self.submit)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def submit(self):
        text = self.window().line_edit.text()
        table = self.window().table.get_contents()
        phrase = Phrase(text,table=table)
        self.window().setPhrase(phrase)
        wordlist = self.window().word_list
        wordlist.add_items(phrase.words)

class RemoveCharButton(QPushButton):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("remove_char")
        self.setText("Remove Row")
        self.pressed.connect(self.remove)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def remove(self):
        row = self.window().table.currentRow()
        self.window().table.remove_row(row)
        self.window().driver.decrypt()

class RemoveWordButton(QPushButton):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("remove_word")
        self.setText("Remove Word")
        self.pressed.connect(self.remove_selected)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def remove_selected(self):
        self.window().chosen_list.remove_word()
        self.window().driver.decrypt()

class SolveButton(QPushButton):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("solve")
        self.setText("Auto Solve")
        self.pressed.connect(self.solve)

    def solve(self):
        table = self.window().table.get_contents()
        self.window().driver.solve(table)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

class SubmitCharButton(QPushButton):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("submit_char")
        self.setText("Add Row")
        self.pressed.connect(self.submit)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

    def submit(self):
        old_txt = self.window().old_combo.currentText()
        new_txt = self.window().new_combo.currentText()
        self.window().table.add_chars(old_txt,new_txt)
        self.window().driver.decrypt()

class AutoCheck(QCheckBox):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("AutoCheck")
        self.setText("Auto")

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

class WordLabel(QLabel):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("word_label")
        self.setText("Words")
        self.setFont(BoldFont())
        self.setIndent(8)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

class MatchesLabel(QLabel):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("matches_label")
        self.setText("Matches")
        self.setFont(BoldFont())
        self.setIndent(8)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window

class TranslationLabel(QLabel):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self._window = None
        self.setObjectName("translation_label")
        self.setText("Character Translation Table")
        self.setFont(BoldFont())
        self.setIndent(8)

    def window(self):
        return self._window

    def setWindow(self,window):
        self._window = window
