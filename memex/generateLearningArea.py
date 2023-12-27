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
generateLearningArea.py --rdffile <pathToRdfFile>,<pathToRDFFile> --outputFolder <pathToOutputFolder>

Generate a collection markdown files containing information from one or more Australian Curriculum v9 RDF file for a specific learning area
"""

import os
import argparse
import logging

from pprint import pprint

##-- add the ../src folder into include path 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from australianCurriculum import australianCurriculum 

def parseArgs():
    """
    Ensure we get the RDF file  and outputFolder
    """

    parser = argparse.ArgumentParser(description="Recurse through an Oz Curriculum RDF file")
    parser.add_argument("--rdffile", action="store", type=str, nargs="+", help="Path to the RDF file", required=True)
    parser.add_argument("--outputFolder", action="store", help="Path to the output folder", required=False)

    return parser.parse_args()



if __name__ == "__main__":

    args = parseArgs()

    learningArea = australianCurriculum()

    for file in args.rdffile:
        learningArea.addRdfFile(file)

    print(learningArea)

#    learningArea.walkTheGraph()
