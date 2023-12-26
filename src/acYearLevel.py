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
acYearLevel.py

Implement (data) class for handling an Australian Curriculum year level

"""

from dataclasses import dataclass
from typing import Any

from datetime import datetime

@dataclass
class acYearLevel:
    #-- tmp storage of the RDFLib node object
    node: Any = None
    #-- parsed out Oz curriculum values
    subjectId : str = None # the subjectId of the node in the graph
    title: str = None
    abbreviation: str = None
    description: str = None
    dateModified : datetime = None

    achievementStandards : dict = None
    contentDescriptions: dict = None
    
    def __init__(self, subjectId, title, abbreviation, dateModified):
        self.subjectId = subjectId
        self.title = title
        self.abbreviation = abbreviation
        self.dateModified = dateModified

        self.achievementStandards = {}
        self.contentDescriptions = {}

    def __str__(self) -> str:
        representation = f"""{self.title} ({self.abbreviation}) modified {self.dateModified}"""

        return representation

    @property
    def dateModified(self):
        """
        Return the dateModified as a string
        """
        return self._dateModified.strftime("%Y-%m-%d %H:%M:%S")

    @dateModified.setter
    def dateModified(self, value):
        """
        Convert the string value (e.g. 2021-09-28T09:27:45+00:00) into a datetime object
        """
        self._dateModified = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z") 
 