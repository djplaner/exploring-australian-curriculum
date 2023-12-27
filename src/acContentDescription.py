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
acContentDescription.py

Implement (data) class for handling an Australian Curriculum content description

Each content description may have

- Achivement Standard Components (???)
- Elaborations
- (Related Content) might be expected, but isn't there (at least in MAT and TEC RDFs)

"""

from dataclasses import dataclass
from typing import Any

from datetime import datetime

from acNode import acNode

@dataclass
class acContentDescription(acNode):
    #-- parsed out Oz curriculum values
    # the subjectId of the node in the graph/actually the RDFlib node
    subjectId : str = None 
    title: str = None # the actual detail/description of the content descriptor
    abbreviation: str = None
    #description: str = None
    dateModified : datetime = None
    nominalYearLevel : str = None

    elaborations : dict = None # keyed on abbreviation of the contentDescription node
    achievementStandardComponents : dict = None # keyed on abbreviation of the contentDescription node
    
    def __init__(self, subjectId, title, abbreviation, dateModified, nominalYearLevel):

        self.subjectId = subjectId
        self.title = title
        self.abbreviation = abbreviation
        self.dateModified = dateModified
        self.nominalYearLevel = nominalYearLevel

        self.elaborations = {}
        self.achievementStandardComponents = {}

    def __str__(self) -> str:
        representation = f"""- content descriptor {self.abbreviation} - {self.title} modified {self.dateModified}"""

        for elaboration in self.elaborations.keys():
            representation += f"\n\t\t\t - elaboration {self.elaborations[elaboration]}"

        return representation
