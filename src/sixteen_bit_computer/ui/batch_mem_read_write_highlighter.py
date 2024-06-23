import re

from qtpy import QtGui

class BatchMemReadWriteHighlighter(QtGui.QSyntaxHighlighter):
    """
    Syntax highlighter for batch read write commands.

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

        self.formats = self.gen_formats()
        self.highlight_rules = self.gen_highlight_rules()

    def gen_formats(self):
        """

        """

        formats = {}

        # Green
        opcode_format = QtGui.QTextCharFormat()
        opcode_format.setForeground(QtGui.QColor(166, 226, 43))
        opcode_format.setFontWeight(QtGui.QFont.Bold)
        formats["read"] = opcode_format

        # Orange
        module_format = QtGui.QTextCharFormat()
        module_format.setForeground(QtGui.QColor(253, 150, 34))
        module_format.setFontWeight(QtGui.QFont.Bold)
        formats["write"] = module_format

        # Purple
        number_format = QtGui.QTextCharFormat()
        number_format.setForeground(QtGui.QColor(172, 128, 255))
        number_format.setFontWeight(QtGui.QFont.Bold)
        formats["number"] = number_format

        # Light grey
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor(116, 112, 93))
        comment_format.setFontItalic(True)
        formats["comment"] = comment_format

        return formats

    def gen_highlight_rules(self):
        """

        """
        rules = []

        # Read
        pattern = (
            # Start of the string or some whitespace
            r"((?<=^)|(?<=\s))"

            # R
            "R"

            # Some whitespace or the end of the string 
            r"((?=\s)|(?=$))"
        )
        rules.append((re.compile(pattern), self.formats["read"]))

        # Write
        pattern = (
            # Start of the string or some whitespace
            r"((?<=^)|(?<=\s))"

            # W
            "W"

            # Some whitespace or the end of the string 
            r"((?=\s)|(?=$))"
        )
        rules.append((re.compile(pattern), self.formats["write"]))

        # Number
        # Start of the string or some whitespace
        # A hash follow by a python number
        # Then some whitespace or the end of the string 
        pattern = (
            # Start of the string or some whitespace
            r"((?<=^)|(?<=\s)|(?<=\[))"

            # Start the matching group
            "("

                # Optional plus or minus
                r"[+-]{0,1}"

                # Number group
                "("

                    # Binary
                    r"(0b[01_]+)"

                    # Or
                    "|"

                    # Octal
                    r"(0o[0-7_]+)"

                    # Or
                    "|"

                    # Decimal
                    r"([0-9_]+)"

                    # Or
                    "|"

                    # Hex
                    r"(0x[0-9A-F_]+)"

                # End number group
                ")"

            # End the matching group
            ")"

            # Some whitespace or the end of the string 
            r"((?=\])|(?=\s)|(?=$))"
        )
        rules.append((re.compile(pattern), self.formats["number"]))

        return rules


    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text
        """

        # Highlight any comments, then pass what's left to be highlighted
        comment_index = text.find("//")
        if comment_index >= 0:
            self.setFormat(
                comment_index,
                (len(text) - comment_index),
                self.formats["comment"]
            )
            text = text[:comment_index]

        # Highlight all the other types
        for regex, _format in self.highlight_rules:
            for match in re.finditer(regex, text):
                start_index, end_index_plus_1 = match.span()
                length = end_index_plus_1 - start_index
                self.setFormat(
                    start_index,
                    length,
                    _format
                )