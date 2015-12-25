from node import Node
import networkx as nx
import event_insight_lib
from networkx.readwrite import json_graph


class ConceptModel:
    """
    The ConceptModel object wraps a `nx.Graph` object. Nodes (vertices) are `Node` objects and edges are the
    correlation scores (just "scores" in IBM Watson API terminology).
    """

    """
    The model itself is stored in the form of a `networkx.Graph` directed graph.
    """
    graph = None

    def __init__(self, list_of_concepts=None):
        """
        Initializes the ConceptModel using a list of raw concepts.
        :param list_of_concepts: A list of concept labels (eg. ['Microsoft', 'IBM']) to initialize the model around.
        """
        # Initialize the model graph object.
        self.graph = nx.Graph()
        # Enter and associate the starting nodes.
        if list_of_concepts:
            for concept_label in list_of_concepts:
                mixin_concept = Node(concept_label)
                self.graph.add_node(mixin_concept)
        # Set the maturity of the resultant model.

    ###################################
    # Setters, getters, and printers. #
    ###################################

    def print_edges(self):
        """
        Edge pretty-printing method that's useful for debugging.
        """
        for index, edge in enumerate(self.graph.edges()):
            print(index, edge[0].concept + ' <- ' + str(self.graph.edge[edge[0]][edge[1]]['weight']) + ' -> ' + edge[
                1].concept)

    def print_nodes(self):
        """
        Node pretty-printing method that's useful for debugging.
        """
        for index, node in enumerate(self.nodes()):
            print(index, node.concept)

    def nodes(self):
        """
        :return: Returns a list of all of the Concept objects in the ConceptModel.
        """
        return self.graph.nodes()

    def concepts(self):
        """
        :return: Returns a sorted list of all concepts in the ConceptModel.
        """
        return sorted([concept.concept for concept in self.nodes()])

    def edges(self):
        """
        :return: Returns a list of all of the (concept, other concept, strength) tuples in the ConceptModel. See
        also `print_edges()` and `self.graph.edges()`.
        """
        return [(edge[0].concept, edge[1].concept, self.graph[edge[0]][edge[1]]['weight']) for edge in
                self.graph.edges()]

    def set_view_counts(self):
        """
        Initializes the view counts for all of the Concept objects in the ConceptModel. See Concept for a
        description of why this parameter is optional.
        """
        for node in self.nodes():
            node.set_view_count()

    def get_node(self, concept):
        """
        Returns the Node object associated with a concept in the `ConceptModel`.
        :param concept: The concept of a Concept supposedly in the ConceptModel.
        :return: The `Node` object in the ConceptModel, if it is found. Throws an error if it is not.
        """
        for node in self.nodes():
            if node.concept == concept:
                return node
        raise RuntimeError('Concept ' + concept + ' not found in ' + str(self))

    def get_view_count(self, concept):
        """
        Returns the `view_count` of a concept in the `ConceptModel`.
        :param concept: The concept supposedly in the `ConceptModel`.
        :return: The `view_count` int parameter of the concept, if it is found. Throws an error if it is not.
        """
        return self.get_node(concept).view_count

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

    def augment_by_node(self, node, level=0, limit=20):
        """
        Augments the ConceptModel by mining the given node and adding newly discovered nodes to the resultant graph.
        :param node -- The node to be expanded. Note that this node need not already be present in the graph.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        mixin = ConceptModel()
        related_concepts_raw = event_insight_lib.get_related_concepts(node.concept, level=level, limit=limit)
        if node not in self.nodes():
            self.graph.add_node(node)
        for raw_concept in related_concepts_raw['concepts']:
            # Avoid adding the `A-A` multi-edge returned by the raw `get_related_concepts`.
            if raw_concept['concept']['label'] != node.concept:
                new_node = Node(raw_concept['concept']['label'])
                mixin.graph.add_edge(self.get_node(node.concept), new_node, weight=raw_concept['score'])
        self.merge_with(mixin)

    def augment(self, concept, level=0, limit=20):
        """
        Augments the ConceptModel by assigning the given node to a concept and adding newly discovered nodes to the
        resultant graph. This method is an externally-facing wrapper for the internal `augment_by_node()` method:
        the difference is that this method maps a concept while that method maps a node.
        :param concept -- The concept to be expanded. Note that this concept need not already be present in the graph.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        self.augment_by_node(Node(concept), level=level, limit=limit)

    def abridge_by_node(self, node, level=0, limit=20):
        """
        Performs the inverse operation of augment by removing the expansion of the given node from the graph.
        :param node -- The node to be abridged. Note that this node need not already be present in the graph.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        inverse = ConceptModel()
        inverse.augment_by_node(node, level=level, limit=limit)
        for concept_node in [node for node in self.nodes() if node in inverse.graph.nodes()]:
            self.graph.remove_node(concept_node)

    def abridge(self, concept, level=0, limit=20):
        """
        Performs the inverse operation of augment by removing the expansion of the given concept from the graph.
        This method is an externally-facing wrapper for the internal `abridge_by_node()` method: the difference is
        that this method maps a concept while that method maps a node.
        :param concept -- The concept to be expanded. Note that this concept need not already be present in the graph.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        self.abridge_by_node(Node(concept), level=level, limit=limit)

    def explode(self, level=0, limit=20):
        """
        Explodes a graph by augmenting every concept already in it. Warning: for sufficiently large graphs this is a
        very slow operation! See also the expand() method for a more focused version of this operation.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        for concept_node in self.nodes():
            self.augment_by_node(concept_node, level=level, limit=limit)

    def expand(self, level=0, limit=20):
        """
        Expands a graph by augmenting concepts with only one (or no) edge. Warning: for sufficiently large graphs this
        is a slow operation! See also the expand() method for a less focused version of this operation.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        for concept_node in [node for node in self.nodes() if len(self.graph.neighbors(node)) <= 1]:
            self.augment_by_node(concept_node, level=level, limit=limit)

    def intersection_with(self, mixin_concept_model):
        """
        :param mixin_concept_model: Another ConceptModel to be compared to.
        :return: A list of overlapping concept nodes. with their relevance parameters set to average relevance.
        """
        overlapping_concept_nodes = [node for node in self.nodes() if node in mixin_concept_model.nodes()]
        for concept_node in overlapping_concept_nodes:
            concept_node.set_relevance((concept_node.relevance + mixin_concept_model.get_node(
                    concept_node.concept).relevance) / 2)
        return overlapping_concept_nodes

    def to_data(self):
        # TODO: This method works by mapping to e.g. IBM_0.981_1982 concatenations. Super hack. Redo this properly.
        """
        Returns the JSON representation of a ConceptModel. Counter-operation to `load_from_dict()`.
        :param self: A ConceptModel.
        :return: The nx dictionary representation of the ConceptModel.
        """
        # Generate the flattening map.
        tuple_map = [(node, node.hacky_str_rpr()) for node in self.nodes()]
        dict_map = {map_tuple[0]: map_tuple[1] for map_tuple in tuple_map}
        # Flatten the graph.
        flattened_model = nx.relabel_nodes(self.graph, dict_map)
        return json_graph.node_link_data(flattened_model)

    def load_from_data(self, data):
        # TODO: As above, but backwards. Need to redo this properly.
        """
        Generates a ConceptModel out of a JSON representation. Counter-operation to `convert_concept_to_dict()`.
        :param data: The dictionary being passed to the method.
        :return: The generated ConceptModel.
        """
        # Generate the un-flattening map.
        self.graph = json_graph.node_link_graph(data)
        dict_map = {node: Node(node.split("_")[0], relevance=node.split("_")[1], view_count=node.split("_")[2]) for
                    node in self.nodes()}
        # Un-flatten the graph and return it.
        self.graph = nx.relabel_nodes(self.graph, dict_map)


#######################
# Read/write methods. #
#######################

def model(user_input):
    """
    Models arbitrary user input and returns an associated ConceptModel.
    :param user_input: Arbitrary input, be it a name (e.g. Apple (company) -> Apple Inc.) or a text string (e.g.
    "the iPhone 5C, released this Thursday..." -> iPhone).
    :return: The constructed `ConceptModel` object. Might be empty!
    """
    new_model = ConceptModel()
    if user_input:
        related_concepts_raw = event_insight_lib.annotate_text(user_input)
        new_labels = [raw_concept['concept']['label'] for raw_concept in related_concepts_raw['annotations']]
        for label in new_labels:
            new_model.add(label)
    return new_model
