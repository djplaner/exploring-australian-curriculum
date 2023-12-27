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
genMemexAc.py --rdffile <pathToRdfFile>,<pathToRDFFile> --outputFolder <pathToOutputFolder>

Generate a collection markdown files containing information from one or more Australian Curriculum v9 learning area RDF files 

Format in --outputFolder

learningAreas.md
- displays information about all learning areas
- each learning area has a folder named after the learning area which will contain the content descriptors

    ## Learning Area: The Arts

    <achievementStandard and components>

    ### Strand <strand abbreviation> - <strand title>

    #### Sub-strand <sub-strand abbreviation> - <sub-strand title> (optional)

    Table of content descriptors linking (with tooltips)

    | [[<cd #1 code>]] | [[<cd #1 code>]] |


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
    parser.add_argument(
        "--rdffile", action="store", type=str, nargs="+", help="Path to the RDF file", required=True)
    parser.add_argument(
        "--outputFolder", action="store", help="Path to the output folder", required=True)

    return parser.parse_args()


def generateAC(args) -> australianCurriculum:
    """
    Return a complete australianCurriculum object based on the RDF files provided
    """

    ac = australianCurriculum()

    for file in args.rdffile:
        ac.addRdfFile(file)

    return ac

def writeMarkdown( ac ) -> None:
    """
    Create the markdown files based on the AC object
    """


    learningAreasMd = open(os.path.join(args.outputFolder, "learningAreas.md"), "w")

    learningAreasMd.write("# Learning Areas\n\n")
    
    for learningArea in ac.learningAreas.values():
        ## convert learning area title into a safe folder name 
        learningAreaFolder = learningArea.title.replace(" ", "_")
        # create the folder if it doesn't exist
        os.makedirs(os.path.join(args.outputFolder, learningAreaFolder), exist_ok=True)

        learningAreasMd.write(f"## Learning Area: {learningArea.title}\n\n")    

#        pprint(learningArea)
#        quit(1)

    #-- close the file
    learningAreasMd.close()

if __name__ == "__main__":

    args = parseArgs()

    ac = generateAC(args)

#    writeMarkdown( ac ) 

    print(ac)

#    learningArea.walkTheGraph()
