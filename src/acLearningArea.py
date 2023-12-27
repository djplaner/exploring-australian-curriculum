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
acLearningArea.py

Implement (data) class for handling an Australian Curriculum Learning Area

Constructor accepts an object from a RDFLib generator
"""

from dataclasses import dataclass
from typing import Any

from datetime import datetime

from acNode import acNode

from pprint import pprint

@dataclass
class acLearningArea(acNode):
    #-- parsed out Oz curriculum values
    subjectId : str = None # the subjectId of the node in the graph
    title: str = None
    dateModified: datetime = None
    abbreviation: str = None

    subjects : dict = None #-- dictionary of subjects keyed by subjectId
    
    def __init__(self, subjectId, title, dateModified, abbreviation):
        self.subjectId = subjectId
        self.title = title
        self.dateModified = dateModified
        self.abbreviation = abbreviation

        self.subjects = {}

    def __str__(self) -> str:
        #-- create a string representation of the dateModified date object
        representation = f"""\tLearning Area {self.title} ({self.abbreviation}) modified {self.dateModified}"""

        for subject in self.subjects.keys():
            representation += f"\n\t{self.subjects[subject]}"

        return representation
 