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


"""

import os
import argparse

from markdownify import markdownify

from pprint import pprint

##-- add the ../src folder into include path 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from australianCurriculum import australianCurriculum 
from acContentDescription import acContentDescription
from acYearLevel import acYearLevel

##-- if True only include year 7 up
global SECONDARY 
SECONDARY = True
##-- specify names of subjects to exclude
global EXCLUDE_SUBJECTS
EXCLUDE_SUBJECTS = [ "Design and Technologies"]

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

def includeYearLevel( yearLevel: acYearLevel ) -> bool:
    """
    Return true iff the given year level should be included
    if SECONDARY is true, then include years from 7 onward
    if SECONDARY is false, then no check
    """

    if not SECONDARY:
        return True

    #-- extract a list of any numbers included in yearLevel.title
    years = [int(s) for s in yearLevel.title.split() if s.isdigit()]

    #-- if no numbers, must be foundation - not secondary
    if len(years)==0:
        return False

    #-- return true iff all years are equal to or greater than 7
    return all(year >= 7 for year in years)

def writeMarkdown( ac ) -> None:
    """
    Create the markdown files based on the AC object
    """


    learningAreasMd = open(os.path.join(args.outputFolder, "v9-learning-areas.md"), "w")

    learningAreasMd.write("""
# Learning Areas

See also: [[australian-curriculum]], [[teaching]]

??? info "About this page"

    The base information on this page is generated automatically from [machine-readable versions](https://v9.australiancurriculum.edu.au/machine-readable-australian-curriculum) of [version 9 of the Australian Curriculum](https://v9.australiancurriculum.edu.au/) using [this project](https://github.com/djplaner/exploring-australian-curriculum#exploring-the-australian-curriculum)    

    In particular, it's an example of leveraging the reprogrammability of digital technologies to orchestrate (gather, weave and augment) a range of technologies (the Australian Curriculum, RDF, Python, Foam etc) for a very specific purpose. In this case specific to an individual teacher. Rather than make do with the generic Australian Curriculum site the same data as been woven into something more useful (for me).

""")
    
    for learningArea in ac.learningAreas.values():
        ## convert learning area title into a safe folder name 
        learningAreaFolder = learningArea.title.replace(" ", "_")
        # create the folder if it doesn't exist
        os.makedirs(os.path.join(args.outputFolder, learningAreaFolder), exist_ok=True)

        learningAreasMd.write(f"## {learningArea.title}\n\n")    

        #-- subjects
        for subject in learningArea.subjects.values():
            if str(subject.title) in EXCLUDE_SUBJECTS:
                continue
            learningAreasMd.write(f"### {subject.title}\n\n")

            #-- year levels
            for yearLevel in subject.yearLevels.values():
                #-- only include year levels if chosen by globals
                if not includeYearLevel( yearLevel):
                    continue

                learningAreasMd.write(f"#### {yearLevel.title}\n\n")

                #-- Achievement standard - need to do an accordion?
                asTitle = str(yearLevel.achievementStandard.title)
                #-- turn any \n in asTitle into double \n
                asTitle = asTitle.replace("\n", "\n\n\t")
                # add a \t to the beginning of each line in asTitle
                description = markdownify(yearLevel.description).replace("\n", "\n\t")
                
                learningAreasMd.write(f""" 

??? info "Year level description"

\t{description}


??? info "Achievement Standard"

\t{asTitle}

""")

                for component in yearLevel.achievementStandard.components.values():
                    learningAreasMd.write(f"\t - _{str(component.abbreviation)}_: {str(component.title)}\n")

                #-- strands and sub-strands
                # Create a folder object for an existing folder for the learning area
                folder = os.path.join(args.outputFolder, learningAreaFolder)

                for strand in yearLevel.strands.values():
                    learningAreasMd.write(f"##### {strand.title}\n\n")

                    #-- if there are substrands, write CDs for them
                    for subStrand in strand.subStrands.values():
                        learningAreasMd.write(f"###### _{subStrand.title}_\n\n")

                        writeContentDescriptionMarkdown( subStrand, folder, learningAreasMd )

                    #-- write any content descriptions for the strand
                    writeContentDescriptionMarkdown( strand, folder, learningAreasMd )

    #-- add wikilink definitions
    learningAreasMd.write("""
[//begin]: # "Autogenerated link references for markdown compatibility"
[australian-curriculum]: ..%2Faustralian-curriculum "Australian Curriculum"
[teaching]: ..%2F..%2Fteaching "Teaching"
[//end]: # "Autogenerated link references"   """)

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

        writeContentDescriptionMdFile( cd, folder )

    learningAreasMd.write('\n</div>\n')

def writeContentDescriptionMdFile( contentDescription : acContentDescription, folder) -> None:
    """
    WRite the content description's markdown file in the given folder/abbreviation
    """

    mdFile = open(os.path.join(folder, f"{contentDescription.abbreviation}.md"), "w")
    #-- raise error if file doesn't open for writing
    if not mdFile:
        raise Exception(f"Unable to open {contentDescription.abbreviation}.md for writing")

    #-- get a string representation of where the CD resides in the hierarchy
    place = contentDescription.placeInHierarchy()

    seeString = "[[v9-learning-areas|Learning Areas]]"
    for level in ["learningArea", "subject", "strand", "sub-strand", "yearLevel"]:
        if place[level] is not None:
            if level in ["learningArea", "subject"]:
                #-- these are the only levels that will be unique links on the learning area level
                seeString += f" / [[v9-learning-areas#{place[level]}|{place[level]}]]"
            else:
                seeString += f" / {place[level]}"

    mdFile.write(f"""
---
title: "{contentDescription.abbreviation}"
type: "note"
tags: australian-curriculum
---

See also: {seeString}

""")
    mdFile.write(f"> {contentDescription.title}\n\n")

    elaborations = contentDescription.elaborations.values()
    if len(elaborations)>0:
        mdFile.write('??? note "Elaborations"\n\n')

        for elaboration in elaborations:
            mdFile.write(f"\t- _{elaboration.abbreviation}_ - {elaboration.title}\n")

    asComponents = contentDescription.achievementStandardComponents.values()
    
    if len(asComponents)>0:
        mdFile.write('??? note "Achievement Standard Components"\n\n')
        for asComponent in asComponents:
            mdFile.write(f"\t- _{asComponent.abbreviation}_ - {asComponent.title}\n")

        
    mdFile.write("""
[//begin]: # "Autogenerated link references for markdown compatibility"
[v9-learning-areas]: ..%2Fv9-learning-areas "Learning Areas"
[//end]: # "Autogenerated link references" 
""")

    mdFile.close()


if __name__ == "__main__":

    args = parseArgs()

    ac = generateAC(args)

    writeMarkdown( ac ) 

#    print(ac)

#    learningArea.walkTheGraph()
