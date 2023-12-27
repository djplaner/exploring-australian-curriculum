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
acStrand.py

Implement (data) class for handling an Australian Curriculum strand

Each strand has sub-strands, which in turn have content descriptions

"""

from dataclasses import dataclass
from typing import Any

from datetime import datetime

from acNode import acNode

@dataclass
class acStrand(acNode):
    #-- tmp storage of the RDFLib node object
    node: Any = None
    #-- parsed out Oz curriculum values
    subjectId : str = None # the subjectId of the node in the graph
    title: str = None # the actual detail/description of the strand
    abbreviation: str = None
    dateModified : datetime = None
    nominalYearLevel : str = None

    #-- some learning areas don't have sub-strands, hence contentDescriptions
    #   get added here
    contendDescriptions : dict = None
    subStrands : dict = None # keyed on abbreviation of the subStrand node
    
    def __init__(self, subjectId, title, abbreviation, dateModified, nominalYearLevel):
        self.subjectId = subjectId
        self.title = title
        self.abbreviation = abbreviation
        self.dateModified = dateModified
        self.nominalYearLevel = nominalYearLevel

        self.subStrands = {}
        self.contentDescriptions = {}

    def __str__(self) -> str:
        representation = f"""- strand {self.abbreviation} - {self.title} modified {self.dateModified}"""

        for subStrand in self.subStrands.keys():
            representation += f"\n\t\t- subStrand {self.subStrands[subStrand]}"

        for cd in self.contentDescriptions.keys():
            representation += f"\n\t\t- content description {self.contentDescriptions[cd]}"

        return representation
