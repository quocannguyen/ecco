from typing import TextIO, List
import os

from ..utils.ecco_logging import EccoFileNotFound, EccoSyntaxError
from .ecco_token import Token, TokenType
from .character_type import CharacterType


class Scanner:
    def __init__(self, input_fn: str):
        """A class for scanning in Tokens

        Args:
            input_fn (str): Filename of the input program file
        """
        self.filename: str = input_fn
        self.file: TextIO

        self.put_back_buffer: str = ""

        self.line_number: int = 1

        self.initialized: bool = False
        self.current_token = Token()
        
        self.next_character_type: CharacterType

    # def __enter__(self: Scanner): -> Scanner:
    def __enter__(self):
        """Opens the program file for scanning

        Raises:
            EccoFileNotFound: If the program file does not exist
        """
        if os.path.exists(self.filename):
            self.file = open(self.filename, "r")
        else:
            raise EccoFileNotFound(self.filename)

        self.initialized = True

        return self

    def __exit__(self, _, __, ___):
        """Closes the program file"""
        self.file.close()

    def open(self) -> None:
        """Raises:
            EccoFileNotFound
        """
        self.__enter__()

    def close(self) -> None:
        self.__exit__(None, None, None)

    def get_next_character(self) -> str:
        """Get the next character from the input stream

        Returns:
            str: The next character from the input stream
        """
        next_character: str

        if self.put_back_buffer:
            # Read the putback buffer first
            next_character = self.put_back_buffer
            self.put_back_buffer = ""  # Empty the buffer
        else:
            # Otherwise, we read a single character from
            # the open input file, and conditionally
            # increment our rudimentary line counter
            next_character = self.file.read(1)
            if next_character == "\n":
                self.line_number += 1

        if next_character == '\0':
            self.next_character_type = CharacterType.END_OF_FILE
        elif next_character.isalpha():
            self.next_character_type = CharacterType.ALPHA
        elif next_character.isnumeric():
            self.next_character_type = CharacterType.NUMERIC
        else:
            self.next_character_type = CharacterType.NON_ALPHANUMERIC

        return next_character

    def skip(self) -> str:
        """Gets the next non-whitespace character from the input stream

        Returns:
            str: The next non-whitespace character from the input stream
        """
        c: str = self.get_next_character()
        while c.isspace():
            c = self.get_next_character()
        return c

    def put_back(self, c: str) -> None:
        """Put a character back into the input stream

        Args:
            c (str): Character to put back into the input stream
        """
        if len(c) != 1:
            raise TypeError(
                f"put_back() expected a character, but string of length {len(c)} found"
            )

        self.put_back_buffer = c

    def scan_integer_literal(self, c: str) -> int:
        """Scan integer literals into a buffer and parse them into int objects

        Args:
            c (str): Current character from input stream

        Returns:
            int: Scanned integer literal
        """
        in_string: str = ""

        while c.isdigit():
            in_string += c
            c = self.get_next_character()

        self.put_back(c)

        return int(in_string)

    def scan(self) -> Token:
        """Scan the next token

        Args:
            current_token (Token): Global Token object to scan data into

        Raises:
            EccoSyntaxError: If an unrecognized Token is reached

        Returns:
            Token:
        """
        next_character: str = self.skip()

        # # Check for EOF
        # if next_character == "":
        #     self.current_token.type = TokenType.EOF
        #     return self.current_token

        # possible_token_types: List[TokenType] = []
        # for token_type in TokenType:
        #     if str(token_type)[0] == next_character:
        #         possible_token_types.append(token_type)

        # if not len(possible_token_types):
        #     if next_character.isdigit():
        #         self.current_token.type = TokenType.INTEGER_LITERAL
        #         self.current_token.value = self.scan_integer_literal(next_character)
        #     else:
        #         raise EccoSyntaxError(f'Unrecognized token "{next_character}"')
        # else:
        #     if len(next_character) == 1:
        #         self.current_token.type = possible_token_types[0]
        #         return self.current_token
        #     else:
        #         # TODO: Implement multiple token with the same first character
        #         pass
        

        if self.next_character_type == CharacterType.END_OF_FILE:
            self.current_token.type = TokenType.EOF
        elif self.next_character_type == CharacterType.NUMERIC:
            self.current_token.type = TokenType.INTEGER_LITERAL
            self.current_token.value = self.scan_integer_literal(next_character)
        elif self.next_character_type == CharacterType.ALPHA:
            # self.lexeme += next_character
            # next_character = self.get_next_character()
            # while (
            #     self.next_character_type == CharacterType.ALPHA or
            #     self.next_character_type == CharacterType.NUMERIC or
            #     next_character == '_'
            # ):
            #     self.lexeme += next_character
            #     next_character = self.get_next_character()
            # #
            # self.put_back(next_character)
            # # TODO: Handle lexeme starting with alphabet
            # # self.current_token.type =
            # self.current_token.value = self.lexeme
            pass
        elif self.next_character_type == CharacterType.NON_ALPHANUMERIC:
            self.scan_non_alphanumeric(next_character)

        return self.current_token

    def scan_file(self) -> None:
        """Scans a file and prints out its Tokens"""
        while self.scan():
            print(self.current_token)

    def scan_non_alphanumeric(self, character: str) -> None:
        """Scans non-alphanumeric token into current_token"""
        next_character = self.get_next_character()
        lexeme = character + next_character

        token_values = [token_type.value for token_type in TokenType]
        while lexeme in token_values:
            next_character = self.get_next_character()
            lexeme += next_character
        # 
        self.put_back(next_character)
        self.current_token.type = TokenType(lexeme)
        