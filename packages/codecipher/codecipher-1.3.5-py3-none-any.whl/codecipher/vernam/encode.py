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
     Defined class VernamEncode with attribute(s) and method(s).
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
class VernamEncode:
    """
        Defined class VernamEncode with attribute(s) and method(s).
        Created encode class with backend API.
        It defines:

            :attributes:
                | __encode_data - data encode container.
            :methods:
                | encode_data - property methods for encode data.
                | encode - encode data to Vernam format.
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

    def encode(self, data: str, key: str) -> None:
        """
            Encoding data to Vernam format.

            :param data: data which should be encoded.
            :type data: <str>
            :param key: key for encoding.
            :type key: <str>
            :return: None
            :exceptions: None
        """
        encode_list = []
        key = (key * (len(data) // len(key))) + key[:len(data) % len(key)]
        for i in range(len(data)):
            if data[i].isalpha() and key[i].isalpha():
                keyCode = ord(key[i].lower()) - 96
                textCode = ord(data[i].lower()) - 96
                ans = textCode + keyCode - 1
                if ans > 26:
                    ans -= 26
                if data[i].isupper():
                    encode_list.append(chr(ans + 96).upper())
                else:
                    encode_list.append(chr(ans + 96))
            else:
                encode_list.append(data[i])
        self.__encode_data = "".join(encode_list)
