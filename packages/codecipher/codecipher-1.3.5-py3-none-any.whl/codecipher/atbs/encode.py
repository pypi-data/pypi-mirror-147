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
     Defined class AlephTawBetShinEncode with attribute(s) and method(s).
     Created encode class with backend API.
'''

import sys
from dataclasses import dataclass

try:
    from codecipher.atbs.lookup_table import LOOKUP_TABLE
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
class AlephTawBetShinEncode:
    """
        Defined class AlephTawBetShinEncode with attribute(s) and method(s).
        Created encode class with backend API.
        It defines:

            :attributes:
                | __encode_data - data encode container.
            :methods:
                | encode_data - property methods for encode data.
                | encode - encode data to AlephTawBetShin format.
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

    def encode(self, data: str) -> None:
        """
            Encoding data to AlephTawBetShin format.

            :param data: data which should be encoded.
            :type data: <str>
            :return: None
            :exceptions: None
        """
        encode_list = []
        for i in data:
            encode_list.append(LOOKUP_TABLE[i])
        self.__encode_data = "".join(encode_list)
