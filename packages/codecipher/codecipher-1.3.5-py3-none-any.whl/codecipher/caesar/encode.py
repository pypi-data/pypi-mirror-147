# -*- coding: UTF-8 -*-

'''
 Module
     encode.py
 Copyright
     Copyright (C) 2021 Vladimir Roncevic <elektron.ronca@gmail.com>
     codecipher is free software: you can redistribute it and/or modify it
     under the terms of the GNU General Public License as published by the
     Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     codecipher is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
     See the GNU General Public License for more details.
     You should have received a copy of the GNU General Public License along
     with this program. If not, see <http://www.gnu.org/licenses/>.
 Info
     Defined class CaesarEncode with attribute(s) and method(s).
     Created encode class with backend API.
'''

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2021, https://electux.github.io/codecipher'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/electux/codecipher/blob/main/LICENSE'
__version__ = '1.3.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass
class CaesarEncode:
    """
        Defined class CaesarEncode with attribute(s) and method(s).
        Created encode class with backend API.
        It defines:

            :attributes:
                | __encode_data - data encode container.
            :methods:
                | encode_data - property methods for encode data.
                | encode - encode data to Caesar format.
    """

    __encode_data: str

    @property
    def encode_data(self) -> str:
        """
            Property method for getting encode data.

            :return: encoded data.
            :rtype: <str>
            :exceptions: None
        """
        return self.__encode_data

    @encode_data.setter
    def encode_data(self, encode_data: str) -> None:
        """
            Property method for setting encode data.

            :param encode_data: encode data.
            :type encode_data: <str>
            :return: None
            :exceptions: None
        """
        self.__encode_data = encode_data

    def encode(self, data: str, shift_counter: int) -> None:
        """
            Encoding data to Caesar format.

            :param data: data which should be encoded.
            :type data: <str>
            :param shift_counter: defining the shift count.
            :type shift_counter: <int>
            :return: None
            :exceptions: None
        """
        encode_list = []
        for data_char in data:
            if data_char.isspace() or data_char.isnumeric():
                encode_list.append(data_char)
                continue
            data_char_index, new_index = None, None
            new_unicode, new_character = None, None
            if data_char.isupper():
                data_char_index = ord(data_char) - ord("A")
                new_index = (data_char_index + shift_counter) % 26
                new_unicode = new_index + ord("A")
            else:
                data_char_index = ord(data_char) - ord("a")
                new_index = (data_char_index + shift_counter) % 26
                new_unicode = new_index + ord("a")
            new_character = chr(new_unicode)
            encode_list.append(new_character)
        self.__encode_data = "".join(encode_list)
