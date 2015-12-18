from concept import Concept
from conceptmodel import ConceptModel
import event_insight_lib

ibm = Concept('IBM')
# microsoft = ConceptModel(['Microsoft'])

ibm_graph = ConceptModel(['IBM', 'Microsoft'])
# ibm_graph.print_edges()
# ibm_graph.print_nodes()
ibm_graph.visualize()
# ibm_graph.graph = ibm.get_related_concepts_graph(simple=True)

# a = Concept('Pineapple')
# related_concepts_raw = event_insight_lib.get_related_concepts(a.label)
# print(related_concepts_raw)
# print(a)