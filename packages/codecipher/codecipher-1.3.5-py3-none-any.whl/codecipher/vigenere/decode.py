# -*- coding: UTF-8 -*-

'''
 Module
     decode.py
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
     Defined class VigenereDecode with attribute(s) and method(s).
     Created decode class with backend API.
'''

import sys
from dataclasses import dataclass

try:
    from codecipher.vigenere.lookup_table import LookUpTable
except ImportError as ats_error_message:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error_message)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2021, https://electux.github.io/codecipher'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/electux/codecipher/blob/main/LICENSE'
__version__ = '1.3.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass
class VigenereDecode:
    """
        Defined class VigenereDecode with attribute(s) and method(s).
        Created decode class with backend API.
        It defines:

            :attributes:
                | __decode_data - data decode container.
            :methods:
                | decode_data - property methods for decode data.
                | __split_data - splitting data for decoding.
                | decode - decode data from Vigenere format.
    """

    __decode_data: str

    @property
    def decode_data(self) -> str:
        """
            Property method for getting decode data.

            :return: decode data in str format.
            :rtype: <str>
            :exceptions: None
        """
        return self.__decode_data

    @decode_data.setter
    def decode_data(self, decode_data_val: str) -> None:
        """
            Property method for setting decode data.

            :param decode_data_val: decoded data.
            :type decode_data_val: <str>
            :return: None
            :exceptions: None
        """
        self.__decode_data = decode_data_val

    def __split_data(self, data_to_decode: str, key: str) -> list:
        """
            Splitting data for decoding.

            :param data_to_decode: data which should be decoded.
            :type data_to_decode: <str>
            :param key: key for decoding.
            :type key: <str>
            :return: list with data for decoding.
            :rtype: <list>
            :exceptions: None
        """
        split_message = []
        for i in range(0, len(data_to_decode), len(key)):
            split_message.append(data_to_decode[i: i + len(key)])
        return split_message

    def decode(self, data_to_decode: str, key: str) -> None:
        """
            Decoding data from Vigenere format.

            :param data_to_decode: data which should be decoded.
            :type data_to_decode: <str>
            :param key: key for decoding.
            :type key: <str>
            :return: None
            :exceptions: None
        """
        decode_list = []
        for each_split in self.__split_data(data_to_decode, key):
            for index, letter in enumerate(each_split):
                process_index = (
                    LookUpTable.LETTER_TO_INDEX[letter] -
                    LookUpTable.LETTER_TO_INDEX[key[index]]
                ) % len(LookUpTable.ALPHANUM)
                decode_list.append(LookUpTable.INDEX_TO_LETTER[process_index])
        self.__decode_data = "".join(decode_list)
