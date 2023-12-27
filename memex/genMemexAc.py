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
from acContentDescription import acContentDescription

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


    learningAreasMd = open(os.path.join(args.outputFolder, "v9-learning-areas.md"), "w")

    learningAreasMd.write("""
# Learning Areas

See also: [[australian-curriculum]], [[teaching]]

""")
    
    for learningArea in ac.learningAreas.values():
        ## convert learning area title into a safe folder name 
        learningAreaFolder = learningArea.title.replace(" ", "_")
        # create the folder if it doesn't exist
        os.makedirs(os.path.join(args.outputFolder, learningAreaFolder), exist_ok=True)

        learningAreasMd.write(f"## {learningArea.title}\n\n")    

        #-- subjects
        for subject in learningArea.subjects.values():
            learningAreasMd.write(f"### {subject.title}\n\n")

            #-- year levels
            for yearLevel in subject.yearLevels.values():
                learningAreasMd.write(f"#### {yearLevel.title}\n\n")

                #-- Achievement standard - need to do an accordion?
                asTitle = str(yearLevel.achievementStandard.title)
                #-- turn any \n in asTitle into double \n
                asTitle = asTitle.replace("\n", "\n\n")
                learningAreasMd.write(asTitle)
                learningAreasMd.write("\n\n")

                for component in yearLevel.achievementStandard.components.values():
                    learningAreasMd.write(f"- _{str(component.abbreviation)}_ - {str(component.title)}\n")

                learningAreasMd.write("\n")

                #-- strands and sub-strands
                folder = os.path.join(args.outputFolder, learningAreaFolder)

                for strand in yearLevel.strands.values():
                    learningAreasMd.write(f"##### {strand.title}\n\n")

                    for subStrand in strand.subStrands.values():
                        learningAreasMd.write(f"###### {subStrand.title}\n\n")

                        writeContentDescriptionMarkdown( subStrand, folder, learningAreasMd )

                    writeContentDescriptionMarkdown( strand, folder, learningAreasMd )

                        #-- content descriptions
#                        for contentDescription in subStrand.contentDescriptions.values():
#                            learningAreasMd.write(f"[[{contentDescription.code}]] {contentDescription.description}\n\n")
#

    #-- close the file
    learningAreasMd.close()

def writeContentDescriptionMarkdown( strand, folder, learningAreasMd ) -> None:
    """
    Write the content descriptions for a strand or sub-strand
    """

    learningAreasMd.write('\n<div class="grid cards" markdown>\n')

    for cd in strand.contentDescriptions.values():
        learningAreasMd.write(f"""
- __[[{cd.abbreviation}]]__ 

    {cd.title}

""")

    learningAreasMd.write('\n</div>\n')

    """contentDescriptions = list(strand.contentDescriptions.values())
    numCdRows = len(contentDescriptions) / 5
    row = 0

    while row < numCdRows:
        col = 0

        learningAreasMd.write("| ")
        while col < 5:
            cdIndex = int(row * 5 + col)
            if cdIndex < len(contentDescriptions):
                contentDescription = contentDescriptions[cdIndex]
                learningAreasMd.write(f"[[{contentDescription.abbreviation}]] | ")
                #-- create folder for content description
                writeContentDescriptionMdFile( contentDescription, folder )
            else:
                break
            col += 1

        learningAreasMd.write("\n")
        row+=1
    """
    
def writeContentDescriptionMdFile( contentDescription : acContentDescription, folder) -> None:
    """
    WRite the content description's markdown file in the given folder/abbreviation
    """

    mdFile = open(os.path.join(folder, f"{contentDescription.abbreviation}.md"), "w")

    mdFile.write(f"""
# {contentDescription.abbreviation} 

See also: [[v9-learning-areas]]

""")
    mdFile.write(f"> {contentDescription.title}\n\n")
    mdFile.write("Elaborations\n\n")

    for elaboration in contentDescription.elaborations.values():
        mdFile.write(f"\n- _{elaboration.abbreviation}_ - {elaboration.title}\n")

    mdFile.close()


if __name__ == "__main__":

    args = parseArgs()

    ac = generateAC(args)

    writeMarkdown( ac ) 

#    print(ac)

#    learningArea.walkTheGraph()
