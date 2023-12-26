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

from pprint import pprint


@dataclass
class australianCurriculum:
    nodes : dict  # points to nodes in graph (learningArea and subjects)
    root : Any = None # root node of graph, feels kludgy
    graph: Any = None # the RDFLib graph object
    # Currently file being parsed TODO remove as we're going to handle multiple files
    fileName: str = None 
    #-- storage for the curriculum objects
    learningAreas: dict = None
    subjects: dict = None
    contentDescriptions: dict = None

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
            title = self.graph.value(subject=learningAreaNode, predicate=URIRef("http://purl.org/dc/terms/title"))
            dateModified = self.graph.value(subject=learningAreaNode, predicate=URIRef("http://purl.org/dc/terms/modified"))
            # abbreviation is in the statementNotation predicate
            abbreviation = self.graph.value(subject=learningAreaNode, predicate=self.statementNotation)
            learningArea = acLearningArea(learningAreaNode, title, dateModified, abbreviation) 
            self.learningAreas[title] = learningArea
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
            title = self.graph.value(subject=subject, predicate=URIRef("http://purl.org/dc/terms/title"))
            abbreviation = self.graph.value(subject=subject, predicate=self.statementNotation)
            dateModified = self.graph.value(subject=subject, predicate=URIRef("http://purl.org/dc/terms/modified"))

            self.subjects[title] = acSubject(subject, title, abbreviation, dateModified)

            #-- for each subject, start parsing the year levels
            # - pass in the node and the title (for the subjects dict) and
            #   recurse down the graph using date methods for the year level class
            #   to add new classes for achievement standards and content descriptions
            self.parseYearLevel(subject, title)

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
            #-- extract the title, dateModified, and abbreviation from the node
            title = self.graph.value(subject=yearLevelNode, predicate=URIRef("http://purl.org/dc/terms/title"))
            dateModified = self.graph.value(subject=yearLevelNode, predicate=URIRef("http://purl.org/dc/terms/modified"))
            # abbreviation is in the statementNotation predicate
            abbreviation = self.graph.value(subject=yearLevelNode, predicate=self.statementNotation)
            yearLevel = acYearLevel(yearLevelNode, title, abbreviation, dateModified) 
            self.subjects[titleOfSubject].yearLevels[title] = yearLevel

            #-- TODO add the achievement standard children for this year level

            
            #-- TODO add the content description children for this year level
            

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




