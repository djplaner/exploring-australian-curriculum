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
Experiment in using rdflib to parse the v9 Oz curriculum files
- very ugly early experiments, unfinished
"""

from pprint import pprint 

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF
from rdflib.plugin import register, Serializer, Parser

def dumpGraph():
    """
    Simple text dump of graph
    """

    print(g.serialize( format="json-ld", indent=4))

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
    


g = Graph()
#g.parse("../data/v9/MAT.rdf", format="xml", bind_namespaces="rdflib")
g.parse("../data/v9/MAT.rdf", format="xml")

print("one")
getAllValuesForContentDescription(g, "http://vocabulary.curriculum.edu.au/MRAC/2023/07/LA/MAT/5dc85a9b-a071-409d-a543-a79f6d0da403" )
#print("two")
#getAllValuesForContentDescription(g, "http://vocabulary.curriculum.edu.au/MRAC/2023/07/LA/MAT/c643289b-9771-4d9f-9a33-836b6ec52335")
#dumpGraphTriples(g)
quit(0)
#dumpContentDescriptions(g)

getYearLevelContentDescriptionIds(g, 10)

#sparqlDump(g)

dumpGraphTriples(g)
quit(0)




#print(len(g))

#pprint.pprint(g.subjects)

subjects = {}

for s, p, o in g:
    if (s, p, o) not in g:
        raise Exception("It better be!")

    print("----- subject")
    pprint(s)
    print("----- predicate")
    pprint(p)
    print("----- object")
    pprint(o)

    #-- if the subject is not in the dictionary, add it
    if s not in subjects:
        subjects[s] = {}

    subjects[s][p] = o

for s in subjects:
    print(f"Subject {s} ")
#    print( f"  title {subjects[s][RDF.title]}")
    for p in subjects[s]:
        if "statementLabel" in str(p) or "title" in str(p):
            print(f"  {p} = {subjects[s][p]}")

    print()



#for stmt in g:
#    pprint.pprint(stmt)

#data = g.serialize(format='nt')
#print(data)

#predicateQuery = g.query("""
#                         select ?s 
#                         where {?s ?predicates ?o}
#                         """)
#
#for row in predicateQuery:
#    print('%s' % row)