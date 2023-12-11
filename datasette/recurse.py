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

def printMyNameSpace(g):
    """
    Display the namespaces used in the graph
    """
    for ns_prefix, namespace in g.namespaces():
        print(f"ns_prefix {ns_prefix} namespace {namespace}")

def getAllValuesForContentDescription(g, subjectId):
    """
    Given a graph and an subjectId for a content description
    display details of a specific subset of values

    - Graph.vaue( subject=subjectId, predicate="Content Description") 
    - Get all the specific values via value method
      http://vocabulary.curriculum.edu.au/MRAC/2023/07/LA/MAT/5dc85a9b-a071-409d-a543-a79f6d0da403"
    """
    
    valuesGraph = Graph()
    
    #-- create a literal search for subjectId
    id = URIRef(subjectId)
    pprint(id)
    print(id)

    cdLiteral = Literal("Content Description", lang="en-au")
    # - namespace
    asnNameSpace = Namespace("http://purl.org/ASN/schema/core/")
    cdPredicate = asnNameSpace.statementLabel

    print(f"Trying to get values for {id} --- {cdLiteral}")
#    ylLiteral = Literal(f"Year 8", lang='en-au')
#    ylPredicate = URIRef('https://www.esa.edu.au/nominalYearLevel')

    #-- perhaps use triples
#    valuesGraph = g.value((id, cdLiteral, None), default="fred")
    #-- triples gets a long list of all sorts of things
#    valuesGraph = g.triples((id, None, None))
    valuesGraph = g.predicate_objects(subject=id)

    for tuple in valuesGraph:
        print(f"tuple {tuple}")

    quit(1)

    if valuesGraph=="fred":
        print("No values found")
        return
    #dumpGraphTriples(valuesGraph)
    for s, p, o in g:
        print(f"-- {s} --- predict {p} object {o}")
    quit(1)
    pprint(valuesGraph)
    #valuesGraph = g.triples((None, cdPredicate, None))
#    valuesGraph += g.triples((None, ylPredicate, ylLiteral))
#    pprint(valuesGraph)
#    quit(1)
    #dumpGraph(valuesGraph)




def dumpContentDescriptions(g):
    """
    Given a graph for a Oz Curriculum RDF file extract out all the content descriptions and display their code and title

    Content descriptions are identified by the 
    - predicate http://purl.org/ASN/schema/core/statementLabel
    - object 'Content Description'
    """

    cdGraph = extractContentDescriptions(g)
    dumpGraph(cdGraph)

def extractContentDescriptions(g):
    """
    Return a graph of all the content descriptions in the given graph
    """
    cdGraph = Graph()

    #-- form the literal search
    # - the language is important
    cdLiteral = Literal("Content Description", lang="en-au")
    # - namespace
    asnNameSpace = Namespace("http://purl.org/ASN/schema/core/")
    cdPredicate = asnNameSpace.statementLabel

    cdGraph += g.triples((None, cdPredicate, cdLiteral))

    return cdGraph

def extractYearLevel(graph, yearLevel):
    """
    Return a graph of all statements associated with a given year level
    - predicate URIRef('https://www.esa.edu.au/nominalYearLevel')
    - object Literal(f"Year {yearLevel}", lang='en-au')
    """

    ylGraph = Graph()
    
    ylLiteral = Literal(f"Year {yearLevel}", lang='en-au')
    ylPredicate = URIRef('https://www.esa.edu.au/nominalYearLevel')
    
    ylGraph += graph.triples((None, ylPredicate, ylLiteral))
    
    return ylGraph

def getYearLevelContentDescriptionIds(graph, yearLevel):
    """
    Return a list of @ids into the graph for all the content descriptions that match the given yearLevel
    """

    #-- generate a graph for a given year level
    yearLevelGraph = extractYearLevel(graph, yearLevel)

    #-- get a list of subjects in that graph
    subjects = [str(s) for s in yearLevelGraph.subjects()]
    pprint(subjects)

#    dumpGraph(yearLevelGraph)

    #-- generate a graph of the content descriptions from that year level graph
    cdGraph = extractContentDescriptions(yearLevelGraph)

#    ylCdGraph = yearLevelGraph + cdGraph

    dumpGraph(cdGraph)
#    dumpGraphTriples(cdGraph)

    #-- return a list of the @ids of the content descriptions 
    #return [str(cd) for cd in cdGraph.subjects()]

def dumpGraph(g):
    """
    Simple text dump of graph
    """

    print(g.serialize( format="json-ld", indent=4))

def dumpGraphTriples(g):
    """
    Simple text dump of graph
    """

    for s, p, o in g:
        print("----- subject")
        pprint(s)
        print("----- predicate")
        pprint(p)
        print("----- object")
        pprint(o)

def sparqlDump(g):
    """
    Experiment with using SPARQL to query the graph
    Just do a simple dump
    """

    query = """
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o .
    }
    LIMIT 3 
    """

    results = g.query(query)
    for row in results:
        pprint(row)
    


def generateGraphObject(filename):
    """
    Given the path to an RDF file, attempt to parse it using RDFLib and return the Graph object
    """

    g = Graph()
    g.parse(filename, format="xml")

    #-- did it work
    print(f"Graph length {len(g)}")
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
        print(f"Subject {s}")

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

def displayNode(nodeInfo, depth=0):

    for (p, o) in nodeInfo:
#        pprint(entry)
        print(f"{' ' * depth} - {p} >>> {o}")
#        if p == URIRef("http://purl.org/ASN/schema/core/statementNotation"):
#            print(f"- statementNotation {o}")
#        if p == URIRef("http://purl.org/dc/terms/title"):
#            print(f"- title {o}")

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

    ( nodeInfo, nodeChildren) = parsePos(pos)

#    pprint(nodeChildren)

    displayNode(nodeInfo, depth)

#    children = getChildren(pos)
#    pprint(children)
    

def startRecursion(g):
    """
    Main harness for recursing and display info about an Oz Curriculum RDF file
    """

    rootId = getRootId(g)
    print(f"Root id {rootId}")

    recurseOzCurriculum(g, rootId)

if __name__ == "__main__":

    args = parseArgs()

    g = generateGraphObject(args.rdffile)

    startRecursion( g)
   