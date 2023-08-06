"""Custom raw checker to identify commented out code.
"""
from astroid import nodes
import astroid
import traceback
import re
import ast

from pylint.checkers import BaseChecker
from pylint.interfaces import IRawChecker


class CommentedCode(BaseChecker):
    """check for line continuations with '\' instead of using triple
    quoted string or parenthesis
    """

    __implements__ = IRawChecker

    name = "commented_code"
    msgs = {
        "W9901": (
            "remove commented code",
            "commented_code",
            (
                "Used when valid Python code is enclosed in"
                " single line comments, starting with #."
            ),
        )
    }
    options = ()

    def process_module(self, node: nodes.Module) -> None:
        """process a module

        the module's content is accessible via node.stream() function
        """
        with node.stream() as stream:

            for (lineno, line) in enumerate(stream):

                temp_line = (
                    line.decode("utf-8")
                    .strip()
                    .replace("\t", "")
                    .replace("  ", "")
                    .strip()
                )

                if temp_line.startswith("#") > 0:

                    # possible_code: str = line.strip()
                    possible_code = temp_line[1:].strip()

                    # If code is parseable as valid Python code, add message
                    try:
                        astroid.parse(possible_code)
                        if len(
                            possible_code
                        ) > 0 and not possible_code.lower().startswith("todo"):
                            self.add_message("commented_code", line=lineno + 1)
                    except astroid.AstroidSyntaxError:

                        if (
                            possible_code.startswith("if")
                            or possible_code.startswith("for")
                        ) and possible_code.endswith(":"):
                            try:
                                astroid.parse(possible_code + "pass")
                                self.add_message("commented_code", line=lineno + 1)
                            except astroid.AstroidSyntaxError:
                                pass


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(CommentedCode(linter))
