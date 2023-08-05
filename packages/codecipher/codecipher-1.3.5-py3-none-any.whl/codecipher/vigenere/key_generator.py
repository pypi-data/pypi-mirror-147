# -*- coding: UTF-8 -*-

'''
 Module
     key_generator.py
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
     Defined class KeyGenerator with attribute(s) and method(s).
     Create key generator class for Vigener encoding/decoding.
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
class KeyGenerator:
    """
        Defined class KeyGenerator with attribute(s) and method(s).
        Create key generator class for Vigener encoding/decoding.
        It defines:

            :attributes:
                | __data_len - data length.
                | __key - key for encoding/decoding.
            :methods:
                | data - property methods for data length.
                | key - property methods for key.
                | generate_key - generate key for encoding/decoding.
    """

    __data_len: int
    __key: str

    @property
    def data_len(self) -> int:
        """
            Property method for getting data length.

            :return: data length.
            :rtype: <int>
            :exceptions: None
        """
        return self.__data_len

    @data_len.setter
    def data_len(self, data_length: int) -> None:
        """
            Property method for setting data length.

            :param data: data length.
            :type data: <int>
            :return: None
            :exceptions: None
        """
        self.__data_len = data_length

    @property
    def key(self) -> str:
        """
            Property method for getting key.

            :return: key for encoding/decoding.
            :rtype: <str>
            :exceptions: None
        """
        return self.__key

    @key.setter
    def key(self, key: str) -> None:
        """
            Property method for setting key.

            :param key: key for encoding/decoding.
            :type key: <str>
            :return: None
            :exceptions: None
        """
        self.__key = key

    def generate_key(self) -> None:
        """
            Generate key for encoding/decoding.

            :return: None
            :exceptions: None
        """
        key_list = list(self.__key)
        if self.__data_len == len(key_list):
            pass
        else:
            for i in range(self.__data_len - len(key_list)):
                key_list.append(key_list[i % len(key_list)])
        self.__key = "". join(key_list)
