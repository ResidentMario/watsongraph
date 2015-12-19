from conceptmodel import ConceptModel
import matplotlib.pyplot as plt

G = ConceptModel(['IBM'])
print(G.to_dict())

moma_graph = ConceptModel(['Museum of Modern Art'])
moma_graph.visualize()
plt.show()