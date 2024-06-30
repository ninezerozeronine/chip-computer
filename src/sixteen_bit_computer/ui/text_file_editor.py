"""
QPlainTextEdit with line numbers
"""

from qtpy import QtGui, QtCore, QtWidgets


class TextFileEditor(QtWidgets.QWidget):
    """

    """

    def __init__(self, parent=None, file_filter="All (*)"):
        """

        """

        super().__init__(parent=parent)

        self.file_filter = file_filter
        self.current_file = None
        self.edited = False


        # File controls
        self.open_button = QtWidgets.QPushButton("Open")
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_as_button = QtWidgets.QPushButton("Save As")
        self.clear_button = QtWidgets.QPushButton("Clear")
        file_controls_layout = QtWidgets.QHBoxLayout()
        file_controls_layout.addWidget(self.open_button)
        file_controls_layout.addWidget(self.save_button)
        file_controls_layout.addWidget(self.save_as_button)
        file_controls_layout.addWidget(self.clear_button)
        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_editor)
        self.save_as_button.clicked.connect(self.save_editor_as)
        self.clear_button.clicked.connect( self.clear_editor)

        # File status
        self.current_file_label = QtWidgets.QLabel("File:")
        self.current_file_line_edit = QtWidgets.QLineEdit("<No file>")
        self.current_file_line_edit.setReadOnly(True)
        file_status_layout = QtWidgets.QHBoxLayout()
        file_status_layout.addWidget(self.current_file_label)
        file_status_layout.addWidget(self.current_file_line_edit)
        file_status_layout.setStretch(1, 5)

        # Editor
        self.line_number_text_edit = LineNumberTextEdit()
        self.line_number_text_edit.textChanged.connect(self.text_changed)

        # Line wrap and unsaved label
        self.line_wrap_checkbox = QtWidgets.QCheckBox("Line wrap")
        self.unsaved_label = QtWidgets.QLabel()
        unsaved_label_font = self.unsaved_label.font()
        unsaved_label_font.setItalic(True)
        self.unsaved_label.setFont(unsaved_label_font)
        line_wrap_layout = QtWidgets.QHBoxLayout()
        line_wrap_layout.addWidget(self.line_wrap_checkbox)
        line_wrap_layout.addStretch()
        line_wrap_layout.addWidget(self.unsaved_label)
        self.line_wrap_checkbox.clicked.connect(self.set_line_wrap)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        main_layout.addLayout(file_controls_layout)
        main_layout.addLayout(file_status_layout)
        main_layout.addWidget(self.line_number_text_edit)
        main_layout.addLayout(line_wrap_layout)
        main_layout.setStretch(2, 5)

        self.setLayout(main_layout)


    def text_changed(self):
        """
        React to the text being changed.
        """
        self.edited = True
        self.unsaved_label.setText("(Unsaved changes)")

    def set_line_wrap(self):
        """
        Set line wrap for editor based on checkbox state.
        """

        if self.line_wrap_checkbox.isChecked():
            self.line_number_text_edit.setLineWrapMode(
                self.line_number_text_edit.LineWrapMode.WidgetWidth
                # QtWidgets.QPlainTextEdit.LineWrapMode.WidgetWidth
            )
        else:
            self.line_number_text_edit.setLineWrapMode(
                self.line_number_text_edit.LineWrapMode.NoWrap
            )

    def clear_editor(self, force=False):
        """
        Clear the contents of the editor.
        """
        do_clear = False
        if not self.edited or force:
            do_clear = True
        else:
            res = QtWidgets.QMessageBox.question(
                self,
                "Clear editor",
                (
                    "The contents of the editor have not been saved, "
                    "are you sure you want to clear?"
                )
            )
            if res == QtWidgets.QMessageBox.Yes:
                do_clear = True

        if do_clear:
            self.line_number_text_edit.clear()
            self.edited = False
            self.current_file = None
            self.unsaved_label.setText("")
            self.current_file_line_edit.setText("<No file>")

    def open_file(self):
        """
        Open a file.
        """
        do_open = False
        if not self.edited:
            do_open = True
        else:
            res = QtWidgets.QMessageBox.question(
                self,
                "Confirm open",
                (
                    "The contents of the editor have not been saved, "
                    "are you sure you want to discard the contents and "
                    "open a file?"
                )
            )
            if res == QtWidgets.QMessageBox.Yes:
                do_open = True

        if do_open:
            filepath, file_filter = QtWidgets.QFileDialog.getOpenFileName(
                parent=self,
                caption="Open file",
                filter=self.file_filter
            )
            if filepath:
                with open(filepath, "r", encoding="utf-8") as file:
                    self.line_number_text_edit.setPlainText(file.read())
                self.current_file = filepath
                self.edited = False
                self.current_file_line_edit.setText(filepath)
                self.unsaved_label.setText("")

    def save_editor(self):
        """
        Save contents of the editor.

        If the current contents of the editor were the result of opening
        a file then the editor contents are saved into that file. Otherwise
        the user is dropped into a save as prompt.

        """
        if self.current_file is None:
            self.save_editor_as()
        else:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.line_number_text_edit.toPlainText())
            self.edited = False
            self.unsaved_label.setText("")


    def save_editor_as(self):
        """
        Save the content of the edirot as a new file.
        """
        filepath, file_filter = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Save as",
            filter=self.file_filter
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(self.line_number_text_edit.toPlainText())
            self.edited = False
            self.current_file = filepath
            self.current_file_line_edit.setText(filepath)
            self.unsaved_label.setText("")


class LineNumberTextEdit(QtWidgets.QPlainTextEdit):
    """
    Text editor part of the text editor with line numbers.

    Inspired by https://stackoverflow.com/questions/50074155/how-to-add-line-number-in-this-texteditor
    """
    def __init__(self, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        self.setFont(QtGui.QFont("Courier"))
        # Background                dark grey       40  41  35  282923
        # Text                      off white       248 248 242 F8F8F2
        self.setStyleSheet("background-color: #282923; color: #F8F8F2")

        # In this instance - passing the parent seems necessary to
        # ensure a connection between the widgets. Maybe because they're
        # not in a layout together?
        self.line_number_area = LineNumberArea(self, parent=self)

        # Connect up signals
        self.blockCountChanged.connect(self.update_left_margin_width)
        self.updateRequest.connect(self.update_line_number_area)


        self.update_left_margin_width(0)


    def get_line_no_width(self):
        """
        Get the width of the line number area in pixels

        Returns:
            int: Width of line number area
        """

        num_digits = len(str(self.blockCount()))
        # Add the 6 pixels of padding so the numbers have a bit of
        # space on either side to breathe.
        width = 6 + self.fontMetrics().width("9") * num_digits
        return width


    def update_left_margin_width(self, _):
        """
        Update left margin width to make space for the line numbers.

        Args:
            _ (int): Needed because this method is connected to the
                block count change signal.
        """
        self.setViewportMargins(self.get_line_no_width(), 0, 0, 0)


    def update_line_number_area(self, rect, dy):
        """
        Update line number area when the main text area updates

        Args:
            rect (QRect): The area needing an update.
            dy (int): The number of pixels the text view was scrolled.
        """
        # If the text area was scrolled, scroll the line numbers too
        if dy:
            self.line_number_area.scroll(0, dy)
        # If just an area of the text view was updated, update (request
        # a redraw?) the part of the line number that corresponds to
        # what changed
        else:
            self.line_number_area.update(
                0,
                rect.y(),
                self.line_number_area.width(),
                rect.height()
            )

        # self.viweport is the viewport widget of the underlying
        # QAbstractScrollArea.
        # So if the viewport is entirely within the area being updated,
        # Update the line number area width.
        # Not entirely sure why this is needed... the line width is
        # determined only by the block count, which doesn't seem like
        # it's affected by the scroll position?
        # Maybe the signal this function is connected to fires when a
        # line is added or removed.
        # But we have a method connected to that signal already...
        if rect.contains(self.viewport().rect()):
            self.update_left_margin_width(0)


    def resizeEvent(self, event):
        """
        Intercept the resize event so we can rezise the line number area.
        """
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
        Intercept a tab keypress to turn it into spaces.

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


class LineNumberArea(QtWidgets.QWidget):
    """
    Line number part of the text editor with line numbers.

    Inspired by https://stackoverflow.com/questions/50074155/how-to-add-line-number-in-this-texteditor
    """

    def __init__(self, editor, parent=None):
        """
        Initialise class
        """
        super().__init__(parent=parent)
        self.editor_ref = editor

    def sizeHint(self):
        """
        Override the inherited sizeHint.

        This doesn't seem strictly necessary - it seemed to behave after
        removing this, but leaving it in as it was in the example.
        """
        return QtCore.QSize(self.editor_ref.get_line_no_width(), 0)

    def paintEvent(self, event):
        """
        Supplement the inherited paintEvent
        """
        super().paintEvent(event)


        painter = QtGui.QPainter(self)

        painter.fillRect(event.rect(), QtGui.QColor("lightGray"))

        block = self.editor_ref.firstVisibleBlock()
        block_number = block.blockNumber()
        block_bounds = self.editor_ref.blockBoundingGeometry(block)
        top = block_bounds.translated(self.editor_ref.contentOffset()).top()
        bottom = top + self.editor_ref.blockBoundingRect(block).height()
        height = self.editor_ref.fontMetrics().height()

        # Loop over the blocks and draw the line numbers
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                line_number = str(block_number + 1)
                painter.setPen(QtGui.QColor("black"))
                painter.drawText(
                    0,
                    top,
                    # This creates some padding on the right
                    self.width() - 3,
                    height,
                    QtCore.Qt.AlignRight,
                    line_number
                )

            block = block.next()
            top = bottom
            bottom = top + self.editor_ref.blockBoundingRect(block).height()
            block_number += 1
