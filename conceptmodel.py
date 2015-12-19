from concept import Concept
import networkx as nx
import matplotlib.pyplot as plt

# TODO: Better visualize() method.


class ConceptModel:
    """The ConceptModel object is a container for the user's concept model."""

    """The maturity of the model, measure unknown."""
    maturity = 0

    """The model itself is stored in the form of a mathematical directed graph (using the networkx (nx)) package."""
    graph = None

    def __init__(self, list_of_labels=None):
        """
        Initializes the ConceptModel using a list of labels. Initializing a ConceptModel point-expands each of these
        concepts and links together the resultant graphs.
        :param list_of_labels: A list of labels (eg. 'IBM') to initialize around. For example, one might call
        ConceptModel(['IBM', 'Go (programming language)', 'Microsoft']).
        """
        # Initialize the model graph object.
        self.graph = nx.Graph()
        # Enter and associate the starting nodes.
        if list_of_labels:
            for label in list_of_labels:
                mixin_graph = Concept(label).expand()
                mixin_concept_model = ConceptModel()
                mixin_concept_model.graph = mixin_graph
                self.merge_with(mixin_concept_model)
        # Set the maturity of the resultant model.
        self.set_maturity()

    def __iter__(self):
        for node in self.graph.nodes():
            yield node

    def merge_with(self, mixin_concept_model):
        """
        Merges the given graph into the current one. Simple wrapper for an nx method.
        :param mixin_concept_model -- The ConceptModel object that is being folded into the current object.
        """
        self.graph = nx.union(self.graph, mixin_concept_model.graph)
        self.set_maturity()

    def set_maturity(self):
        """Simple wrapper for the model maturity recalculation used elsewhere throughout the application."""
        self.maturity = len(self.graph.nodes())

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

    def augment(self, concept):
        """
        Expands and adds a single concept to the ConceptModel.

        :param concept: The concept to be added to the present ConceptModel.
        """
        self.merge_with(ConceptModel([concept]))
        self.set_maturity()

    # TODO abridge()
    def abridge(self, concept):
        """
        Performs the inverse operation of the above, expanding a concept and removing intersections between the two.
        :param concept:
        """
        # inverse = ConceptModel([concept])
        self.set_maturity()

    def get_concept(self, label):
        """
        :param label: Given the label of a Concept supposedly in the ConceptModel...
        :return: ...returns that Concept object.
        """
        for concept in self.graph.nodes():
            if concept.label == label:
                return concept

    def get_labels(self):
        """
        :return: Returns a sorted list of all labels in the ConceptModel.
        """
        return sorted([concept.label for concept in self.graph.nodes()])

    def visualize(self):
        """
        Simple ConceptModel visualizer. Not very elegant! Should look into proper graph visualization libraries?
        :return:
        """
        plt.axis('off')
        nx.draw_networkx(self.graph, with_labels=True, node_color='#A0CBE2', width=2, style='solid', linewidths=None,
                         alpha=0.8, edge_cmap=plt.cm.Blues, font_size=8)