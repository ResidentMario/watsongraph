from conceptmodel import ConceptModel
import matplotlib.pyplot as plt

G = ConceptModel(['IBM'])

moma_graph = ConceptModel(['Museum of Modern Art'])
moma_graph.visualize()
plt.show()