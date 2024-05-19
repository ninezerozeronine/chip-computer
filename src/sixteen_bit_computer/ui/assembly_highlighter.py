from PyQt5 import QtGui, QtCore

class AssemblyHighlighter(QtGui.QSyntaxHighlighter):
    """
    Syntax highlighter for assembly code.

    https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
    """

    def __init__(self, parent):
        """
        Initialise class

        Args:
            parent (QTextDocument): Text document to install the
                highlighter onto.
        """

        super().__init__(parent)

        # Note that comments are last
        self.rules = []

        # LOAD
        # didn't work
        # regexp = QtCore.QRegExp(r"(?!\S)LOAD(?!\S)")

        # Kind of works, but in -LOAD- the load is highlighted :(
        regexp = QtCore.QRegExp(r"\bLOAD\b")

        nth = 0
        _format = QtGui.QTextCharFormat()
        _format.setForeground(QtGui.QColor("blue"))
        _format.setFontWeight(QtGui.QFont.Bold)
        self.rules.append(
            [regexp, nth, _format]
        )

        # PC
        regexp = QtCore.QRegExp(r"\bPC\b")
        nth = 0
        _format = QtGui.QTextCharFormat()
        _format.setForeground(QtGui.QColor("red"))
        _format.setFontWeight(QtGui.QFont.Bold)
        self.rules.append(
            [regexp, nth, _format]
        )

        # Comment
        regexp = QtCore.QRegExp(r"//[^\n]*")
        nth = 0
        _format = QtGui.QTextCharFormat()
        _format.setForeground(QtGui.QColor("green"))
        _format.setFontItalic(True)
        self.rules.append(
            [regexp, nth, _format]
        )

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text
        """

        for regex, nth, _format in self.rules:
            index = regex.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = regex.pos(nth)
                length = len(regex.cap(nth))
                self.setFormat(index, length, _format)
                index = regex.indexIn(text, index + length)            