from concept import Concept
import networkx as nx
import matplotlib.pyplot as plt
import event_insight_lib

# TODO: Better visualize() method.


class ConceptModel:
    """The ConceptModel object is a container for the user's concept model."""

    """The maturity of the model, measure unknown."""
    maturity = 0

    """The model itself is stored in the form of a mathematical directed graph (using the networkx (nx)) package."""
    graph = None

    def __init__(self, list_of_concepts=None):
        """
        Initializes the ConceptModel using a list of concepts.
        :param list_of_concepts: A list of concepts (eg. Concept('IBM')) to initialize around. e.g. one might call
        ConceptModel([Concept('IBM'), Concept('Microsoft')])
        """
        # Initialize the model graph object.
        self.graph = nx.Graph()
        # Enter and associate the starting nodes.
        if list_of_concepts:
            for concept in list_of_concepts:
                # mixin_graph = Concept(label).expand()
                # mixin_concept_model = ConceptModel()
                # mixin_concept_model.graph = mixin_graph
                # self.merge_with(mixin_concept_model)
                self.graph.add_node(concept)
        # Set the maturity of the resultant model.
        self.set_maturity()

    ###################################
    # Setters, getters, and printers. #
    ###################################

    def set_maturity(self):
        """Simple wrapper for the model maturity recalculation used elsewhere throughout the application."""
        self.maturity = self.graph.number_of_nodes()

    def print_edges(self):
        """Edge pretty-printing method that's useful for debugging."""
        n = 1
        for edge in self.graph.edges():
            print(str(n) + ': ' + edge[0].label + ' <-> ' + edge[1].label)
            n += 1

    def print_nodes(self):
        """Node pretty-printing method that's useful for debugging."""
        n = 1
        for node in self.concepts():
            print(str(n) + ': ' + node.label)
            n += 1

    def get_concept(self, label):
        """
        :param label: Given the label of a Concept supposedly in the ConceptModel...
        :return: ...returns that Concept object.
        """
        for concept in self.concepts():
            if concept.label == label:
                return concept

    def concepts(self):
        """
        :return: Returns a list of all of the Concept objects in the ConceptModel.
        """
        return self.graph.nodes()

    def labels(self):
        """
        :return: Returns a sorted list of all labels in the ConceptModel.
        """
        return sorted([concept.label for concept in self.concepts()])

    def set_view_counts(self):
        """
        Initializes the view counts for all of the Concept objects in the ConceptModel. See Concept.py for a
        description of why this parameter is optional.
        """
        for concept in self.concepts():
            concept.set_view_count()

    def visualize(self):
        """
        Simple ConceptModel visualizer. Not very elegant! Should look into proper graph visualization libraries?
        """
        plt.axis('off')
        nx.draw_networkx(self.graph, with_labels=True, node_color='#A0CBE2', width=2, style='solid', linewidths=None,
                         alpha=0.8, edge_cmap=plt.cm.Blues, font_size=8)

    ##################
    # Graph methods. #
    ##################

    def add(self, concept):
        """
        Simple adder method.

        :param concept: Concept to be added to the model.
        """
        self.graph = nx.compose(self.graph, ConceptModel([concept]).graph)

    def merge_with(self, mixin_concept_model):
        """
        Merges the given graph into the current one. The nx.compose method used here compares the hashes of the
        Concept objects being merged, and hashes are overwritten to map to labels.
        e.g. A = Concept('IBM') and B = Concept('IBM') have the same __hash__(), even though the objects are
        different, so they will merge into one when composed.
        :param mixin_concept_model -- The ConceptModel object that is being folded into the current object.
        """
        self.graph = nx.compose(self.graph, mixin_concept_model.graph)

    def augment(self, concept, level=0, limit=10):
        """
        Expands a node within a ConceptModel by mining that concept and adding newly discovered nodes to the
        resultant graph. The action of mining a concept and then linking it to a pre-existing graph is known as
        "expanding" it, a terminology used throughout this library.

        :param concept -- The concept to be expanded. Note that this concept need not already be present in the graph.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        mixin = ConceptModel()
        related_concepts_raw = event_insight_lib.get_related_concepts(concept.label, level=level, limit=limit)
        for raw_concept in related_concepts_raw['concepts']:
            # Remove the `A-A` edge returned by the raw `get_related_concepts` class.
            if raw_concept['concept']['label'] != concept.label:
                new_node = Concept(raw_concept['concept']['label'])
                mixin.graph.add_edge(self.get_concept(concept.label), new_node, weight=raw_concept['score'])
        self.merge_with(mixin)

    def abridge(self, concept, level=0, limit=10):
        """
        Performs the inverse operation of augment by removing the expansion of the given concept from the graph.

        :param concept -- The concept to be abridged. Note that this concept need not already be present in the graph.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        inverse = ConceptModel()
        inverse.augment(concept, level=level, limit=limit)
        for concept_node in [node for node in self.concepts() if node in inverse.graph.nodes()]:
            self.graph.remove_node(concept_node)
        self.set_maturity()

    def explode(self, level=0, limit=10):
        """
        Explodes a graph by augmenting every concept already in it. Warning: for sufficiently large graphs this is a
        very slow operation! See also the expand() method for a more focused version of this operation.

        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        for concept_node in self.concepts():
            self.augment(concept_node, level=level, limit=limit)

    def expand(self, level=0, limit=10):
        """
        Expands a graph by augmenting concepts with only one (or no) edge. Warning: for sufficiently large graphs this
        is a slow operation! See also the expand() method for a less focused version of this operation.

        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        for concept_node in [node for node in self.concepts() if len(self.graph.neighbors(node)) <= 1]:
            self.augment(concept_node, level=level, limit=limit)

    def intersection_with(self, mixin_concept_model):
        """
        :param mixin_concept_model: Another ConceptModel to be compared to.
        :return: A list of overlapping concept nodes. with their relevance parameters set to average relevance.
        """
        overlapping_concept_nodes = [node for node in self.concepts() if node in mixin_concept_model.concepts()]
        for concept_node in overlapping_concept_nodes:
            concept_node.set_relevance((concept_node.relevance + mixin_concept_model.get_concept(
                    concept_node.label).relevance) / 2)
        return overlapping_concept_nodes


#######################
# Read/write methods. #
#######################

def convert_concept_model_to_data(concept_model):
    """
    Returns the JSON representation of a ConceptModel. Counter-operation to load_from_dict().
    :param concept_model: A ConceptModel.
    :return: The nx dictionary representation of the ConceptModel.
    """
    model_schema = []
    for concept_node in concept_model.concepts():
        model_schema.append({'label': concept_node.label,
                             'view_count': concept_node.view_count,
                             'relevance': concept_node.relevance})
    concept_model_schema = {'maturity': concept_model.maturity, 'graph': model_schema}
    return concept_model_schema


def load_concept_model_from_data(data):
    """
    Generates a ConceptModel out of a JSON representation. Counter-operation to convert_concept_to_dict().
    :param data: The dictionary being passed to the method.
    :return: The generated ConceptModel.
    """
    concept_model = ConceptModel()
    concept_model.maturity = data['maturity']
    for concept_data in data['graph']:
        new_concept = Concept(label=concept_data['label'])
        new_concept.view_count = concept_data['view_count']
        new_concept.relevance = concept_data['relevance']
        concept_model.add(new_concept)
    return concept_model