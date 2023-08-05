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
     Defined class VernamDecode with attribute(s) and method(s).
     Created decode class with backend API.
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
class VernamDecode:
    """
        Defined class VernamDecode with attribute(s) and method(s).
        Created decode class with backend API.
        It defines:

            :attributes:
                | __decode_data - data decode container.
            :methods:
                | decode_data - property methods for decode data.
                | decode - decode data from Vernam format.
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
    def decode_data(self, decode_data: str) -> None:
        """
            Property method for setting decode data.

            :param decode_data: decoded data.
            :type decode_data: <str>
            :return: None
            :exceptions: None
        """
        self.__decode_data = decode_data

    def decode(self, data: str, key: str) -> None:
        """
            Decoding data from Vernam format.

            :param data: data which should be decoded.
            :type data: <str>
            :param key: key for decoding.
            :type key: <str>
            :return: None
            :exceptions: None
        """
        decode_list = []
        key = (key * (len(data) // len(key))) + key[:len(data) % len(key)]
        for i in range(len(data)):
            if data[i].isalpha() and key[i].isalpha():
                keyCode = ord(key[i].lower()) - 96
                codeCode = ord(data[i].lower()) - 96
                ans = codeCode - keyCode + 1
                if ans < 1:
                    ans += 26
                if data[i].isupper():
                    decode_list.append(chr(ans + 96).upper())
                else:
                    decode_list.append(chr(ans + 96))
            else:
                decode_list.append(data[i])
        self.__decode_data = "".join(decode_list)
