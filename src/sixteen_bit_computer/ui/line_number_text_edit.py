"""
QPlainTextEdit with line numbers
"""

from PyQt5 import Qt, QtGui, QtCore, QtWidgets

class LineNumberArea(QtWidgets.QWidget):
    """
    Line number part of the text editor with line numbers.

    Inspired by https://stackoverflow.com/questions/50074155/how-to-add-line-number-in-this-texteditor    """

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