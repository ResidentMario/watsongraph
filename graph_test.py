# import networkx as nx
# from concept import Concept

# G = nx.Graph()
# ibm = Concept('IBM')
# microsoft = Concept('Microsoft')
# G.add_node(ibm)
# G.add_node(microsoft)
# G.add_edge(ibm, microsoft)
# print(G.nodes())
# print(G.edges())
# microsoft2 = Concept('Microsoft')
# G.add_edge(ibm, microsoft2)
# G.remove_node(microsoft)
# print(G.nodes())
# # print(G.edges())
# print(G[ibm].keys())

from conceptmodel import ConceptModel
from concept import Concept

A = ConceptModel([Concept('IBM'), Concept('Microsoft'), Concept('Apple')])
B = ConceptModel([Concept('Microsoft'), Concept('Apple')])
A.graph.add_edge(A.graph.nodes()[0], A.graph.nodes()[1])
A.graph.add_edge(A.graph.nodes()[1], A.graph.nodes()[2])
B.graph.add_edge(B.graph.nodes()[0], B.graph.nodes()[1])
# A.merge_with(B)
A.merge_with(B)
# print(A.concepts())
# print(A.graph.edges())
# # A.expand(Concept('Apple'))
# A.augment(Concept('Apple'))
# print(A.concepts())
# A.abridge(Concept('Apple'))
# print(A.concepts())
A.explode()
print(A.labels())