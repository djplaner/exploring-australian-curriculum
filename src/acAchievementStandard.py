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
acAchievementStandard.py

Implement (data) class for handling an Australian Curriculum achievement standard

"""

from dataclasses import dataclass
from typing import Any

from datetime import datetime

from acNode import acNode

@dataclass
class acAchievementStandard(acNode):
    #-- tmp storage of the RDFLib node object
    node: Any = None
    #-- parsed out Oz curriculum values
    subjectId : str = None # the subjectId of the node in the graph
    title: str = None # the actual detail/description of the achievement standard
    abbreviation: str = None
    #description: str = None
    dateModified : datetime = None
    nominalYearLevel : str = None

    components : dict = None # keyed on abbreviation of the AchievementStandardComponent
    
    def __init__(self, subjectId, title, abbreviation, dateModified, nominalYearLevel):
        self.subjectId = subjectId
        self.title = title
        self.abbreviation = abbreviation
        self.dateModified = dateModified
        self.nominalYearLevel = nominalYearLevel

        self.components = {}

    def __str__(self) -> str:
        representation = f"""{self.abbreviation} - {self.title} modified {self.dateModified}"""

        for component in self.components.keys():
            representation += f"\n\t\t{self.components[component]}"

        return representation
 