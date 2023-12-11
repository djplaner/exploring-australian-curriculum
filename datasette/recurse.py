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
recurse.py --rdffile <pathToRdfFile>

- Simple test to recurse through the tree structure of an RDF file provided by the Australian Curriuclum v9
"""

from pprint import pprint 

import argparse

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF
from rdflib.plugin import register, Serializer, Parser


def generateGraphObject(filename):
    """
    Given the path to an RDF file, attempt to parse it using RDFLib and return the Graph object
    """

    g = Graph()
    g.parse(filename, format="xml")

    #-- did it work
#    print(f"Graph length {len(g)}")
    if len(g) == 0:
        print("No data in graph")
        quit(1)
    return g


def parseArgs():
    """
    Ensure we get the RDF file 
    """

    parser = argparse.ArgumentParser(description="Recurse through an Oz Curriculum RDF file")
    parser.add_argument("--rdffile", action="store", help="Path to the RDF file", required=True)

    return parser.parse_args()

def getRootId(g):
    """
    Given a graph extract the subjectId for the node where statementNotation predicate is "root"
    """

    asnNameSpace = Namespace("http://purl.org/ASN/schema/core/")
    statementNotation = asnNameSpace.statementNotation

    subjects = g.subjects(predicate=statementNotation, object=Literal("root", lang="en-au")) 

    #-- how many?
    count = 0
    subject = None
    for s in subjects:
        count += 1
        subject = s
#        print(f"Subject {s}")

    if count == 0:
        print("No root found")
        quit(1)
    if count > 1:
        print("More than one root found")
        quit(1)

    return subject

def parsePos(pos):
    """
    Given a generator of all predicate_objects split them into info to display and children

    (nodeInfo, nodeChilder)
    """

    nodeInfo = []
    nodeChildren = []

    for p, o in pos:
#        print(f"predicate {p} object {o}")
        if p == URIRef("http://purl.org/gem/qualifiers/hasChild"):
            nodeChildren.append(o)
        else:
            nodeInfo.append((p, o))

    return ( nodeInfo, nodeChildren)

def displayNode(subjectId, nodeInfo, depth=0):
    """
    Display information for the node with subjectId
    """

    ## remove http://vocabulary.curriculum.edu.au/MRAC/2023/07/ from subjectId
    id = subjectId.replace("http://vocabulary.curriculum.edu.au/MRAC/2023/07/", "")

    print(f"{'  ' * depth}Node {id}")
    for (p, o) in nodeInfo:
#        pprint(entry)
#        print(f"{' ' * depth} - {p} >>> {o}")
        if p == URIRef("http://purl.org/ASN/schema/core/statementNotation"):
            print(f"{'  ' * depth}- statementNotation {o}")
        if p == URIRef("http://purl.org/ASN/schema/core/statementLabel"):
            print(f"{'  ' * depth}- statementLabel {o}")
        if p == URIRef("http://purl.org/dc/terms/title"):
            print(f"{'  ' * depth}- title {o}")

def getChildren(pos):
    """
    Given a generator of predicate/objects for a node, return a list with the predicate hasChild
     xmlns="http://purl.org/gem/qualifiers/"
    """

    children = []
    for p, o in pos:
        print(f"predicate {p} object {o}")
        if p == "http://purl.org/gem/qualifiers/hasChild":
            children.append(o)

    return children

def recurseOzCurriculum(g, subjectId, depth=0):
    """
    Oz Curriuclum RDF files have a parent/child structure using <hasChild> and <isChildOf> predicates
    Recurse through the graph from the given subjectId, display some information about each node

    - g is the graph object
    - subjectId is the @id of the current node to display and recurse down
    - depth is the current depth of recursion/descent down the tree
    """

    #-- get the predicates/objects for this subjectId
    pos = g.predicate_objects(subject=URIRef(subjectId))

    #-- parse them out into information and children
    ( nodeInfo, nodeChildren) = parsePos(pos)
    #-- display the information
    displayNode(subjectId, nodeInfo, depth)

#    if depth==5:
#        print("-----------------")
#        quit(1)
    #-- recurse down
    for child in nodeChildren:
        childId = str(child)
        recurseOzCurriculum(g, childId, depth+1)



    

def startRecursion(g):
    """
    Main harness for recursing and display info about an Oz Curriculum RDF file
    """

    rootId = getRootId(g)
#    print(f"Root id {rootId}")

    recurseOzCurriculum(g, rootId)

if __name__ == "__main__":

    args = parseArgs()

    print(f"---------------------- {args.rdffile} ----------------------")
    g = generateGraphObject(args.rdffile)

    startRecursion( g)
   