"""
Line numbers inspired by:

https://stackoverflow.com/questions/50074155/how-to-add-line-number-in-this-texteditor
"""

from PyQt5 import Qt, QtGui, QtCore, QtWidgets

class Assembler(QtWidgets.QWidget):
    """
    Widget assemble and send machine code
    """
    def __init__(self, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        self.last_send = []

        self.editor = AssemblyEditor()
        self.assemble_and_send_button = QtWidgets.QPushButton("Assemble and send")
        self.only_changes_checkbox = QtWidgets.QCheckBox("Only send changes")
        self.status_label = QtWidgets.QLabel("Status:")
        self.status_line_edit = QtWidgets.QLineEdit()

        send_layout = QtWidgets.QHBoxLayout()
        send_layout.addStretch()
        send_layout.addWidget(self.only_changes_checkbox)
        send_layout.addWidget(self.assemble_and_send_button)

        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.status_line_edit)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.editor)
        main_layout.addLayout(send_layout)
        main_layout.addLayout(status_layout)
        main_layout.setStretch(0, 5)

        self.setLayout(main_layout)


class LineNumberArea(QtWidgets.QWidget):

    def __init__(self, editor, parent=None):
        super().__init__(parent=parent)
        self.editor_ref = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor_ref.get_line_no_width(), 0)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)

        painter.fillRect(event.rect(), QtGui.QColor("lightGray"))

        block = self.editor_ref.firstVisibleBlock()
        block_number = block.blockNumber()
        block_bounds = self.editor_ref.blockBoundingGeometry(block)
        top = block_bounds.translated(self.editor_ref.contentOffset()).top()
        bottom = top + self.editor_ref.blockBoundingRect(block).height()

        height = self.editor_ref.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                line_number = str(block_number + 1)
                painter.setPen(QtCore.Qt.black)
                painter.drawText(
                    0,
                    top,
                    self.width() - 3,
                    height,
                    QtCore.Qt.AlignRight,
                    line_number
                )

            block = block.next()
            top = bottom
            bottom = top + self.editor_ref.blockBoundingRect(block).height()
            block_number += 1


class AssemblyEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setFont(QtGui.QFont("Courier"))
        # self.setTabStopWidth(40)

        # In this instance - passing the parent seems necessary to
        # ensure a connection between the widgets. Maybe because they're
        # not in a layout together?
        self.line_number_area = LineNumberArea(self, parent=self)
        self.blockCountChanged.connect(self.update_left_margin_width)
        self.updateRequest.connect(self.update_line_number_area)


        self.update_left_margin_width(0)


    def get_line_no_width(self):
        num_digits = len(str(self.blockCount()))
        width = 6 + self.fontMetrics().width("9") * num_digits
        return width


    def update_left_margin_width(self, _):
        self.setViewportMargins(self.get_line_no_width(), 0, 0, 0)


    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
            
        else:
            self.line_number_area.update(
                0,
                rect.y(),
                self.line_number_area.width(),
                rect.height()
            )

        if rect.contains(self.viewport().rect()):
            self.update_left_margin_width(0)


    def resizeEvent(self, event):
        super().resizeEvent(event)

        content_rect = self.contentsRect();
        self.line_number_area.setGeometry(
            QtCore.QRect(
                content_rect.left(),
                content_rect.top(),
                self.get_line_no_width(),
                content_rect.height()
            )
        )

    def keyPressEvent(self, event):
        """
        https://stackoverflow.com/questions/45880941/replace-all-tab-operations-with-inserting-four-spaces-in-qplaintextedit-widget
        """
        if event.key() == QtCore.Qt.Key_Tab:
            event = QtGui.QKeyEvent(
                QtCore.QEvent.KeyPress,
                QtCore.Qt.Key_Space,
                QtCore.Qt.KeyboardModifiers(event.nativeModifiers()),
                "    "
            )
        super().keyPressEvent(event)