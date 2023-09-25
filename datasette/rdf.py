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
"""

from rdflib import Graph
from rdflib.namespace import RDF

g = Graph()
g.parse("../data/v9/MAT.rdf", format="xml")

#print(len(g))

import pprint 
#pprint.pprint(g.subjects)

for s, p, o in g:
    if (s, p, o) not in g:
        raise Exception("It better be!")

    print(f"\nSubject: {s}")
    print(f"Predicate: {p}")
    print(f"Object: {o}")

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