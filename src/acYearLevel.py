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

from acNode import acNode
from acSubject import acSubject

@dataclass
class acYearLevel(acNode):
    subjectId : str = None # the subjectId of the node in the graph
    title: str = None
    abbreviation: str = None
    description: str = None
    dateModified : datetime = None
    subject : acSubject = None # subject to which the year level belongs

    achievementStandard : Any = None # single acAchievementStandard object for year level
    # dict of acStrand objects keyed on the abbreviation of the strand
    # - will contain sub-strands, which in turn contain content descriptions
    strands : dict = None
    
    def __init__(self, subjectId, title, abbreviation, dateModified, description, subject=None):
        self.subjectId = subjectId
        self.title = title
        self.abbreviation = abbreviation
        self.dateModified = dateModified
        self.description = description
        self.subject = subject

        self.strands = {}

    def __str__(self) -> str:
        representation = f"""\tYearLevel - {self.title} ({self.abbreviation}) modified {self.dateModified}"""

        representation += "\n\t\t--------- Description ---------"
        representation += f"""\n\t\t{self.description}"""


        representation += "\n\t\t--------- achievementStandard ---------"

        representation += f"""\n\t\t{self.achievementStandard}"""

        representation += "\n\t\t --------- Strands ---------"

        for strand in self.strands.keys():
            representation += f"\n\t\t{self.strands[strand]}"


        return representation
 