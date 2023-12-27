# Copyright (C) 2023 David Jones
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
acNode.py

Base class for all the other classes used to encapsulate information about particular types of AC nodes
"""

from dataclasses import dataclass
from typing import Any

from datetime import datetime

@dataclass
class acNode:
    dateModified : datetime 

    @property
    def dateModified(self):
        """
        Return the dateModified as a string
        """
        print("called here")
        return self._dateModified.strftime("%Y-%m-%d %H:%M:%S")

    @dateModified.setter
    def dateModified(self, value):
        """
        Convert the string value (e.g. 2021-09-28T09:27:45+00:00) into a datetime object
        """
        try:
            self._dateModified = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z") 
        except: 
            # there's a bit of variety in the AC rdf files
            self._dateModified = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")

