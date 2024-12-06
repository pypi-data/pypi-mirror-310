"""
Copyright (C) 2024 InkBridge Networks (legal@inkbridge.io)

This software may not be redistributed in any form without the prior
written consent of InkBridge Networks.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

Contains the base parser class that contains important parsing functions

Author: Patrick Guo
Date: 2024-08-13
"""
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


class ParseError(Exception):
    """
    An error that occurs when parsing goes unexpected
    """

    def __init__(self, text: str, pos: int, msg: str):
        """
        Args:
            text (str): Text attempted to be parsed
            pos (int): Position of text when parsing error occured
            msg (str): Message describing the error
        """
        self.pos = pos
        self.text = text
        self.msg = msg

    def __str__(self) -> str:
        return f'{self.msg} occured at position {self.pos} of text {self.text}'


class BaseParser:
    """
    Base parser class
    """

    def __init__(self):
        self.buffer = ''
        self.cursor_pos = 0

        self.tokens = []

    def parse(self, buffer: str) -> None:
        """
        Entry point for parsing

        To be overriden in child class

        Args:
            buffer (str): string to be parsed
        """
        raise NotImplementedError

    def remove_leading_whitespace(self) -> None:
        """
        Moves parser cursor to next non-whitespace character

        If already at a non-whitespace character, no movement occurs
        """
        logger.debug('Removing leading whitespace')
        whitespace_tokens = [' ']
        while True:
            # Stop if at last position
            if self.cursor_pos == len(self.buffer):
                break

            # Stop if encountered non-whitespace character
            if self.buffer[self.cursor_pos] not in whitespace_tokens:
                break

            self.cursor_pos += 1

    def keyword(self, *keywords: tuple[str, ...],
                remove_leading_whitespace: bool = True) -> str:
        """
        Looks for matching keywords at current cursor position

        Args:
            keywords (str): list of string to look for
        
        Return:
            String of the keyword that matched
        """
        # remove whitespace if desired
        if remove_leading_whitespace:
            self.remove_leading_whitespace()

        for keyword in keywords:
            logger.debug((f'Attempting to find keyword {keyword} for '
                          f'"{self.buffer}" at position {self.cursor_pos}')
                         )
            # Calculate starting and ending position of keyword if present at
            # current location
            start_pos = self.cursor_pos
            end_pos = start_pos + len(keyword)

            # Then check if the slice matches the keyword
            # Will NOT raise index-out-of-bounds errors
            if self.buffer[start_pos: end_pos] == keyword:
                self.cursor_pos += len(keyword)

                # returns the keyword that matched
                return keyword

        logger.error((f'Failed to find keywords: {", ".join(keywords)}, for '
                      f'"{self.buffer}" at position {self.cursor_pos}')
                     )
        # if none of the keywords were found, raise error
        raise ParseError(self.buffer, self.cursor_pos,
                         f"No keywords: [{','.join(keywords)}] found")

    def search_positive_number(self) -> int:
        """
        Looks for a number at current cursor position

        Stops at first non-numerical value (i.e., anything not [0-9]).

        Args:
            None
        
        Returns:
            int representing the number found
        
        Raises:
            ParseError if no number was detected
        """
        logger.debug((f'Looking for positive number for "{self.buffer}" at '
                      f'position {self.cursor_pos}')
                     )
        self.remove_leading_whitespace()

        init_pos = self.cursor_pos

        # Parse until end of text reached
        while self.cursor_pos < len(self.buffer):
            if not self.buffer[self.cursor_pos].isnumeric():
                break

            self.cursor_pos += 1

        # if no numbers were found (i.e., first char was non-numerical), we
        # raise error as this should be unexpected
        if init_pos == self.cursor_pos:
            logger.error((f'No positive number found for "{self.buffer}"at '
                          f'position {self.cursor_pos}')
                         )
            raise ParseError(self.buffer, self.cursor_pos, 'No number found')

        # Update cursor position and return the integer as an int (rather than
        # a list of chars)
        return int(self.buffer[init_pos:self.cursor_pos])

    def search_uint8(self) -> int:
        """
        Looks for a uint8 number at current cursor position

        Args:
            None

        Returns:
            int within range of a uint8
        
        Raises:
            ParseError if the integer parsed is larger than 256 (uint8)
        """
        logger.debug((f'Looking for uint8 number for "{self.buffer}" at '
                      f'position {self.cursor_pos}')
                     )
        start_pos = self.cursor_pos

        parsed_number = self.search_positive_number()
        if parsed_number >= 256:
            # reset staring pos and raise error if integer parsed is larger
            # than 256
            self.cursor_pos = start_pos
            logger.error((f'No uint8 number found for "{self.buffer}" at '
                          f'position {self.cursor_pos}')
                         )
            raise ParseError(self.buffer, start_pos,
                             'Parsed integer larger than a uint8')

        return parsed_number
