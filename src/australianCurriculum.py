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

Define Python class - asLearningArea - that will parse an Australian Curriuclum (v9) RDF file for a learning area into an Python object

Current design assumptions
- all the RDF parsing work is done in this class
- it creates various AC specific objects based on related classes
- all are implemented as @dataclass
"""

from dataclasses import dataclass
from typing import Any

import os

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF
from rdflib.plugin import register, Serializer, Parser

from acLearningArea import acLearningArea
from acYearLevel import acYearLevel
from acSubject import acSubject
from acAchievementStandard import acAchievementStandard
from acAchievementStandardComponent import acAchievementStandardComponent
from acStrand import acStrand
from acSubStrand import acSubStrand
from acContentDescription import acContentDescription
from acElaboration import acElaboration

from pprint import pprint


@dataclass
class australianCurriculum:
    """ early processing type data structures
    - some of thse (e.g. nodes and root) may have to go away
    """
    nodes : dict  # points to nodes in graph (learningArea and subjects)
    root : Any = None # root node of graph, feels kludgy
    graph: Any = None # the RDFLib graph object
    # Currently file being parsed TODO remove as we're going to handle multiple files
    fileName: str = None 

    """ Storage for the curriculum objects
    - This class will parse the RDF file creating the following objects 

    australianCurriculum is made up of numerous learning areas. 
    TODO use a "parseFile" method to allow multiple RDF files to be parsed
    (because by default an AC RDF file only overs one learning area)"""
    learningAreas: dict = None
    """
    Each learning area can have multiple subjects, which in turn contain most/all of the
    data 
    - yearLevels 
        - achievement standards, 
            - achievement standard components  
        - strands 
            - sub-strands (sub-strands are optional)
                - content descriptions 

    TODO
    - need to figure out how to handle optional sub-strands
    """
    subjects: dict = None
    #-- Each subject is made up of strands/sub-strands/content descriptors
    # - store them in strands, but also update the content descriptions dict to point

    #-- direct access dicts TODO
    # - These are to make it easier to access specific AC components that are hidden away
    #   in the class hierarchy above. keyed on the AC ids/abbreviations and linking to those
    #   object components
    contentDescriptions: dict = None
    strands: dict = None 

    def __init__(self, fileName = None):

        #-- used to contain pointers to nodes in the graph for
        # - learningArea - should only be one
        # - subjects - within the learning area, may be 0 or more
        self.nodes = {
            "learningArea": None,
            "subjects": []
        }

        self.learningAreas = {}
        self.subjects = {}

        #-- Configure some namespace shortcuts
        self.asnNameSpace = Namespace("http://purl.org/ASN/schema/core/")
        self.statementNotation = self.asnNameSpace.statementNotation
        self.statementLabel = self.asnNameSpace.statementLabel

        if fileName is not None:
            self.loadFile(fileName)

    def loadFile(self, fileName):
        #-- test if fileName parameter is a valid, readable file
        if not os.path.isfile(fileName):
            raise ValueError(f"File {fileName} does not exist or is not readable")

        self.fileName = fileName
        self.generateGraphObject()

        #-- walk the graph and generate matching objects
        self.getRoot()
        self.parseGraph()

    def __str__(self):
        """
        Dump out a simple representation to stdout of the object
        """

        representation = f"""
Number of subjects: {len(self.graph)}
Root subject {self.root}"""

        for learningAreaTitle in self.learningAreas.keys():
            representation += f"\nLearning Area: {self.learningAreas[learningAreaTitle].__str__()}"

        for subjectTitle in self.subjects.keys():
            representation += f"\n  - subject: {self.subjects[subjectTitle].__str__()}"

        return representation
            
        

    def generateGraphObject(self):
        """
        Attempt to create a RDFLib graph based on contents of fileName
        """

        self.graph = Graph()
        self.graph.parse(self.fileName, format="xml")

        #-- did it work
        if len(self.graph) == 0:
            raise ValueError(f"No data in graph {self.fileName}")

    def getRoot(self): 
        """ 
        Get the subject with property "root"
        """

        subjects = self.graph.subjects(
            predicate=self.statementNotation, object=Literal("root", lang="en-au")) 

        #-- check we have the right number
        count = 0
        self.root = None
        for s in subjects:
            count += 1
            self.root = s

        if count == 0:
            return ValueError("No root found")
        elif count > 1:
            return ValueError("More than one root found")

    def parseGraph( self ):
        """
        Walk the RDFLib graph from the given subjectId and attempt to popluate the
        class data structures

        1. Find all the learning area root nodes and start a recursion for each one

        TODO 
        2. add any top level stuff???? 
        """

        self.parseLearningAreas()
        self.parseSubjects()

    def parseLearningAreas(self):
        """
        Extract all nodes for with statementLabel == "Learning Area" and stick in the
        self.nodes["learningArea"] variable
        """

        learningAreaNodes = self.graph.subjects(
            predicate=self.statementLabel, object=Literal("Learning Area", lang="en-au"))

        found = 0
        for learningAreaNode in learningAreaNodes:
            #-- extract the title, dateModified, and abbreviation from the node
            info = self.extractNodeInfo(learningAreaNode) 

            learningArea = acLearningArea(
                learningAreaNode, info['title'], info['modified'], info['statementNotation']) 

            self.learningAreas[info['title']] = learningArea
            found+=1

        if (found == 0):
            raise ValueError("No learning areas found")
        if (found > 1):
            raise ValueError("More than one learning area found")


    def parseSubjects(self):
        """
        Grab and parse all the nodes with statementlabel "subject" into acSubject objects

        Attributes of interest
        - title (of subject) - dcterms:title 
        - abbreviation - statementNotation

        TODO
        - Eventually parse the levels and all those components
        """

        subjects = self.graph.subjects(
            predicate=self.statementLabel, object=Literal("Subject", lang="en-au"))
        
        for subject in subjects:
            info = self.extractNodeInfo(subject)
            self.subjects[info['title']] = acSubject(
                subject, info['title'], info['statementNotation'], info['modified'])

            #-- for each subject, start parsing the year levels
            # - pass in the node and the title (for the subjects dict) and
            #   recurse down the graph using date methods for the year level class
            #   to add new classes for achievement standards and content descriptions
            self.parseYearLevel(subject, info['title'])

    def parseYearLevel(self, subjectId, titleOfSubject):
        """
        Called by parseSubjects, given a particular subject id in the graph and the title for the
        Australian Curriculum subject, need to walk the graph hasChild etc from the subject

        """

        #-- get all the year level nodes
        #   predicate isChildOf and object is the subject
        yearLevelNodes = self.graph.subjects(
            predicate=URIRef("http://purl.org/gem/qualifiers/isChildOf"), object=subjectId)

        for yearLevelNode in yearLevelNodes:
            info = self.extractNodeInfo(yearLevelNode)

            yearLevel = acYearLevel(
                yearLevelNode, info['title'], info['statementNotation'], info['modified']) 

            self.subjects[titleOfSubject].yearLevels[info['title']] = yearLevel

            self.parseYearLevelAchievementStandards( yearLevel )
            self.parseYearLevelStrands( yearLevel ) 
            

    def parseYearLevelStrands(self, yearLevel):
        """
        Given an acYearLevel object parse the graph to get all the 
        - strands 
            - sub-strands
                - content descriptions for the year level
        """

        #-- get all the "Strands" nodes with isChildOf of yearLevel.subjectId
        # - start with the children
        strandNodes = self.graph.subjects(
            predicate=URIRef("http://purl.org/gem/qualifiers/isChildOf"), object=yearLevel.subjectId)

        for strandNode in strandNodes:
            info = self.extractNodeInfo(strandNode)
            #-- check the strandNode statementlabel is "Strand" skip if not
            if str(info['statementLabel']) != "Strand":
                continue

            strand = acStrand(
                strandNode, info['title'], info['statementNotation'], 
                info['modified'], info['nominalYearLevel']) 
            yearLevel.strands[str(info['title'])] = strand

            #-- grab the sub-strands
            self.parseStrandSubStrands(strand)

    def parseStrandSubStrands(self, strand):
        """
        Given a stand (from a particular year level) grab all 
        - sub-strands
            - content descriptions
        """

        #-- sub-strands are children of the strand with "Sub-Strand" as the statementLabel
        subStrandNodes = self.graph.subjects(
            predicate=URIRef("http://purl.org/gem/qualifiers/isChildOf"), object=strand.subjectId)

        for subStrandNode in subStrandNodes:
            info = self.extractNodeInfo(subStrandNode)
            #-- check the subStrandNode statementlabel is "Sub-Strand" skip if not
            if str(info['statementLabel']) != "Sub-Strand":
                continue

            subStrand = acSubStrand(
                subStrandNode, info['title'], info['statementNotation'], 
                str(info['modified']), info['nominalYearLevel']) 
            strand.subStrands[str(info['title'])] = subStrand

            #-- grab the content descriptions
            self.parseSubStrandContentDescriptions(subStrand)

    def parseSubStrandContentDescriptions(self, subStrand):
        """
        Given a subStrand (from a particular strand) grab all
        - content descriptions
        """

        #-- content descriptions are children of the subStrand with 
        # "Content Description" as the statementLabel
        cdNodes = self.graph.subjects(
            predicate=URIRef("http://purl.org/gem/qualifiers/isChildOf"), object=subStrand.subjectId)

        for cdNode in cdNodes:
            info = self.extractNodeInfo(cdNode)
            #-- check the cdNode statementlabel is "Content Description" skip if 
            if str(info['statementLabel']) != "Content Description":
                continue

            contentDescription = acContentDescription(
                cdNode, info['title'], info['statementNotation'], 
                str(info['modified']), info['nominalYearLevel'])

            subStrand.contentDescriptions[str(info['statementNotation'])] = contentDescription

            self.parseContentDescriptionExtras(contentDescription)

    def parseContentDescriptionExtras(self, contentDescription):
        """
        Given a acContentDescription object parse the graph to get all the CD extras, including
        - Elaborations
        - Achievement Standard Components
        """

        cdExtraNodes = self.graph.subjects(
            predicate=URIRef("http://purl.org/gem/qualifiers/isChildOf"), object=contentDescription.subjectId)

        for cdExtraNode in cdExtraNodes:
            info = self.extractNodeInfo(cdExtraNode)

            if str(info['statementLabel']) not in ["Elaboration", "Achievement Standard Component"]:
                continue

            if str(info['statementLabel']) == "Elaboration":
                elaboration = acElaboration(
                    cdExtraNode, info['title'], info['statementNotation'],
                    str(info['modified']), info['nominalYearLevel'])

                contentDescription.elaborations[str(info['statementNotation'])] = elaboration
            else:
                achievementStandardComponent = acAchievementStandardComponent(
                    cdExtraNode, info['title'], info['statementNotation'],
                    str(info['modified']), info['nominalYearLevel'])

                contentDescription.achievementStandardComponents[str(info['statementNotation'])] = achievementStandardComponent
            




    def parseYearLevelAchievementStandards(self, yearLevel):
        """
        Given an acYearLevel object, parse the graph to set the achievement standards object for all the "Achievement Standard" and "Achievement Standard Component" nodes

        "Achievement Standard" nodes will have isChildOf of yearLevel.subjectId
        Each one of those will have a child "Achievement Standard Component" node (maybe)
        """

        #-- get all the "Achievement Standard" nodes with isChildOf of yearLevel.subjectId
        achievementStandardNodes = self.graph.subjects(
            predicate=URIRef("http://purl.org/gem/qualifiers/isChildOf"), object=yearLevel.subjectId)

        for achievementStandardNode in achievementStandardNodes:
            info = self.extractNodeInfo(achievementStandardNode)
            #-- check the statementLabel is "Achievement Standard"
            if str(info['statementLabel']) != "Achievement Standard":
                continue

            achievementStandard = acAchievementStandard(
                achievementStandardNode, info['title'], info['statementNotation'], 
                info['modified'], info['nominalYearLevel']) 
            yearLevel.achievementStandard = achievementStandard

            #-- grab the achievement standard components
            # - statementLabel is "Achievement Standard Component" and 
            #   isChildOf is the achievementStandardNode
            components = self.graph.subjects(
                predicate=URIRef("http://purl.org/gem/qualifiers/isChildOf"), object=achievementStandardNode)

            for component in components:
                info = self.extractNodeInfo(component)
                #-- check the statementLabel is "Achievement Standard Component"
                if str(info['statementLabel']) != "Achievement Standard Component":
                    continue

                acComponent = acAchievementStandardComponent(
                    component, info['title'], info['statementNotation'], 
                    info['modified'], info['nominalYearLevel']) 

                achievementStandard.components[str(info['statementNotation'])] = acComponent
            

    def walkTheGraph(self, subjectId=None, depth=0):
        """
        Walk (sort of recursively) the RDFLib graph from the given subjectId

        Oz Curriuclum RDF files have a 
        - parent/child structure using <hasChild> and <isChildOf> predicates
        - but some also via <hasLevel> and <isLevelOf> predicates

        For now, display some information about each node

        TODO - actually generate data structures

        - g is the graph object
        - subjectId is the @id of the current node to display and recurse down
        - depth is the current depth of recursion/descent down the tree
        """

        if subjectId is None:
            subjectId = self.root

        #-- get the predicates/objects for this subjectId
        pos = self.graph.predicate_objects(subject=URIRef(subjectId))

        #-- split them out into information and children
        ( nodeInfo, nodeChildren, nodeLevels) = self.splitPos(pos)
        #-- display the information
        self.displayNode(subjectId, nodeInfo, depth)

        #-- recurse down
        # - first the levels and then the children

        for level in nodeLevels:
            levelId = str(level)
            self.walkTheGraph(levelId, depth+1)
        for child in nodeChildren:
            childId = str(child)
            self.walkTheGraph(childId, depth+1)

    def splitPos(self,pos):
        """
        Given a generator of all predicate_objects split them into info to display and children

        Some of the predicates/objects for the current node are information and some are children of the subject. Split them into two separate arrays returned as a tuple

        (nodeInfo, nodeChilder)
        """

        nodeInfo = []
        nodeChildren = []
        nodeLevels = []

        for p, o in pos:
            """
            An object has children if 
            - it's predicate is hasChild, or
            - it's predicate is `hasLevel`
            """
            if p == URIRef("http://purl.org/gem/qualifiers/hasChild"):
                nodeChildren.append(o)
            elif p == URIRef("http://purl.org/ASN/schema/core/hasLevel"):
                nodeLevels.append(o)
            else:
                nodeInfo.append((p, o))

        return ( nodeInfo, nodeChildren, nodeLevels)


    def displayNode(self, subjectId, nodeInfo, depth=0):
        """
        Dump some info about the current node to stdout

        - Indent it based on the depth
        - Display statementNotation, statementLabel, title predicates first
        - Display other predicates after that
        """

        ## remove http://vocabulary.curriculum.edu.au/MRAC/2023/07/ from subjectId
        ##### id = subjectId.replace("http://vocabulary.curriculum.edu.au/MRAC/2023/07/", "")

        print(f"{'  ' * depth}Node {id}")
        for (p, o) in nodeInfo:
            if p == URIRef("http://purl.org/ASN/schema/core/statementNotation"):
                print(f"{'   ' * depth}- statementNotation {o}")
            elif p == URIRef("http://purl.org/ASN/schema/core/statementLabel"):
                print(f"{'   ' * depth}- statementLabel {o}")
            elif p == URIRef("http://purl.org/dc/terms/title"):
                print(f"{'   ' * depth}- title {o}")

        exclude = [URIRef("http://purl.org/ASN/schema/core/statementNotation"), 
               URIRef("http://purl.org/ASN/schema/core/statementLabel"),
               URIRef("http://purl.org/dc/terms/title") ]
        #-- show the other info nodes
        for (p, o) in nodeInfo:
            if p not in exclude:
                print(f"{'   ' * depth} - other predicate {p} >>> {o}")


    def extractNodeInfo(self, subjectId) -> dict:
        """
        Given a subjectId return a dict that contains common information from an AC node
        """

        info = {}

        info['title'] = self.graph.value(
            subject=subjectId, predicate=URIRef("http://purl.org/dc/terms/title"))
        info['statementLabel'] = self.graph.value(
            subject=subjectId, predicate=self.statementLabel)
        info['statementNotation'] = self.graph.value(
            subject=subjectId, predicate=self.statementNotation)

        info['description'] = self.graph.value(
            subject=subjectId, predicate=URIRef("http://purl.org/dc/terms/description"))
        info['modified'] = self.graph.value(
            subject=subjectId, predicate=URIRef("http://purl.org/dc/terms/modified"))
        # abbreviation is in the statementNotation predicate
        info['nominalYearLevel'] = self.graph.value(
            subject=subjectId, predicate=URIRef("http://www.esa.edu.au/nominalYearLevel"))

        return info



