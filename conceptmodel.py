# import itertools
from concept import Concept
# noinspection PyUnresolvedReferences
import networkx as nx
import matplotlib.pyplot as plt

# TODO calculate_maturity(); visualize()


class ConceptModel:
    """The ConceptModel object is a container for the user's concept model."""

    """The maturity of the model, measure unknown."""
    maturity = 0

    """The model itself is stored in the form of a mathematical directed graph (using the networkx (nx)) package."""
    graph = None

    def __init__(self, list_of_concepts):
        # Initialize the model graph object.
        self.graph = nx.Graph()
        # self.model.add_node(new_vertex)
        # Enter and associate the starting nodes.
        for label in list_of_concepts:
            mixin_graph = Concept(label).get_related_concepts_graph()
            mixin_concept_model = ConceptModel([])
            mixin_concept_model.graph = mixin_graph
            self.merge_with(mixin_concept_model)
        # self.maturity = len(list_of_concepts) ???

    def merge_with(self, mixin_concept_model):
        """
        Merges the given graph into the current one.

        :param mixin_concept_model -- The ConceptModel object that is being folded into the current object.
        """
        self.graph = nx.union(self.graph, mixin_concept_model.graph)

    def print_edges(self):
        """Edge pretty-printing method that's useful for debugging."""
        n = 1
        for edge in self.graph.edges():
            print(str(n) + ': ' + edge[0].label + ' <-> ' + edge[1].label)
            n += 1

    def print_nodes(self):
        """Node pretty-printing method that's useful for debugging."""
        n = 1
        for node in self.graph.nodes():
            print(str(n) + ': ' + node.label)
            n += 1

    def visualize(self):
        """matplotlib visualization. Does not work because of limitations with matplotlib interactions with
        virtualenv (seriously?)."""
        pos=nx.get_node_attributes(self,'pos')
        plt.figure(figsize=(8,8))
        nx.draw_networkx_edges(self,pos,alpha=0.4)
        nx.draw_networkx_nodes(self,pos,
                       node_size=80,
                       cmap=plt.cm.Reds_r)
        plt.xlim(-0.05,1.05)
        plt.ylim(-0.05,1.05)
        plt.axis('off')
        plt.savefig('random_geometric_graph.png')
        plt.show()
