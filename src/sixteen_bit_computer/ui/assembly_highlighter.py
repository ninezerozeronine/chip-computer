import re

from qtpy import QtGui

from .. import assembly_tokens

class AssemblyHighlighter(QtGui.QSyntaxHighlighter):
    """
    Syntax highlighter for assembly code.

    https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
    """

    OPCODES = assembly_tokens.OPCODE.all_opcode_strings()
    MODULES = assembly_tokens.MODULE.all_module_strings()

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
        Background                dark grey       40  41  35  282923
        Text                      off white       248 248 242 F8F8F2
        Opcode: LOAD, STORE       green           166 226 43  A6E22B
        Module: ACC, SP           orange          253 150 34  FD9622
        Anchor: @ #123            red             249 36  114 F92472
        Alias: !myalias           yellow          231 219 116 E7DB74
        Variable: $myvar          pink            248 119 189 F877BD
        Label: &mylabel           cyan            103 216 239 67D8EF
        Number: #123, #0xFF23     purple          172 128 255 AC80FF
        Comment: // A comment     light grey      116 112 93  74705D 
        """

        formats = {}

        # Green
        opcode_format = QtGui.QTextCharFormat()
        opcode_format.setForeground(QtGui.QColor(166, 226, 43))
        opcode_format.setFontWeight(QtGui.QFont.Bold)
        formats["opcode"] = opcode_format

        # Orange
        module_format = QtGui.QTextCharFormat()
        module_format.setForeground(QtGui.QColor(253, 150, 34))
        module_format.setFontWeight(QtGui.QFont.Bold)
        formats["module"] = module_format

        # Red
        anchor_format = QtGui.QTextCharFormat()
        anchor_format.setForeground(QtGui.QColor(249, 36, 114))
        anchor_format.setFontWeight(QtGui.QFont.Bold)
        formats["anchor"] = anchor_format

        # Yellow
        alias_format = QtGui.QTextCharFormat()
        alias_format.setForeground(QtGui.QColor(231, 219, 116))
        alias_format.setFontWeight(QtGui.QFont.Bold)
        formats["alias"] = alias_format

        # Pink
        variable_format = QtGui.QTextCharFormat()
        variable_format.setForeground(QtGui.QColor(248, 119, 189))
        variable_format.setFontWeight(QtGui.QFont.Bold)
        formats["variable"] = variable_format

        # Cyan
        label_format = QtGui.QTextCharFormat()
        label_format.setForeground(QtGui.QColor(103, 216, 239))
        label_format.setFontWeight(QtGui.QFont.Bold)
        formats["label"] = label_format

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

        # Opcodes
        for opcode in self.OPCODES:
            pattern = (
                # Start of the string or some whitespace
                r"((?<=^)|(?<=\s))"

                # The opcode
                "{opcode}"

                # Some whitespace or the end of the string 
                r"((?=\s)|(?=$))"
            ).format(opcode=opcode)
            rules.append((re.compile(pattern), self.formats["opcode"]))

        # Modules
        for module in self.MODULES:
            pattern = (
                # Start of the string, some whitespace or opening brakcet
                r"((?<=^)|(?<=\s)|(?<=\[))"

                # The module
                "{module}"

                # Closing bracket, some whitespace or the end of the string 
                r"((?=\])|(?=\s)|(?=$))"
            ).format(module=module)
            rules.append((re.compile(pattern), self.formats["module"]))


        # Anchor
        pattern = (
            # Start of the string or some whitespace
            r"((?<=^)|(?<=\s))"

            # @ symbol
            "@"

            # Some whitespace or the end of the string 
            r"((?=\s)|(?=$))"
        ).format(module=module)
        rules.append((re.compile(pattern), self.formats["anchor"]))

        # Alias
        pattern = (
            # Start of the string, some whitespace or opening brakcet
            r"((?<=^)|(?<=\s)|(?<=\[))"

            # ! or ! followed by identifier
            r"((!)|(![a-zA-Z_]+\w*))"

            # Closing bracket, some whitespace or the end of the string 
            r"((?=\])|(?=\s)|(?=$))"
        )
        rules.append((re.compile(pattern), self.formats["alias"]))

        # Variable:
        pattern = (
            # Start of the string, some whitespace or opening brakcet
            r"((?<=^)|(?<=\s)|(?<=\[))"

            # $ or $ followed by identifier
            r"((\$)|(\$[a-zA-Z_]+\w*))"

            # Closing bracket, some whitespace or the end of the string 
            r"((?=\])|(?=\s)|(?=$))"
        )
        rules.append((re.compile(pattern), self.formats["variable"]))

        # Label:
        pattern = (
            # Start of the string, some whitespace or opening brakcet
            r"((?<=^)|(?<=\s)|(?<=\[))"

            # & or & followed by identifier
            r"((&)|(&[a-zA-Z_]+\w*))"

            # Closing bracket, some whitespace or the end of the string 
            r"((?=\])|(?=\s)|(?=$))"
        )
        rules.append((re.compile(pattern), self.formats["label"]))

        # Number
        # Start of the string or some whitespace
        # A hash follow by a python number
        # Then some whitespace or the end of the string 
        pattern = (
            # Start of the string or some whitespace
            r"((?<=^)|(?<=\s)|(?<=\[))"

            # Start the matching group
            "("

                # Start the hash only group
                "("

                    # A hash
                    "#"

                # End the hash only group
                ")"

                # Or

                "|"

                # Start the hash and number group
                "("

                    # A hash
                    "#"

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

                # End the hash and number group
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