from watsongraph.node import Node
import networkx as nx
import watsongraph.event_insight_lib
from networkx.readwrite import json_graph
from mwviews.api import PageviewsClient


# import graphistry


# TODO: Advanced concept modeling notebook.
# 1. Remove the basic modeling examples from the existing notebook---let it lie as an introduction to methodology.
#    In particular that Microsoft related companies methodology, I am now realizing, is pretty bunk.
# 2. Start a new notebook based around Model Construction (provisional title?). Topics to cover:
#    - Parameters
#    --- View count. Port all of the "kinda random" code directly out of the existing notebook.
#    --- Relevancy. Talk about how this property is applied for user modeling.
#    --- Arbitrary parameterization, and how both of the above are examples thereof. Introduce `set_property()` and
#        `give_property()`.
#    - Model Construction
#    --- Introduce `add_edge()` and `add_edges()`.
#    --- Recommended methodology for constructing models. Introduce Wikidata. No specific bindings are provided by
#        default but you get the best mileage out of it using `wdq`: http://wdq.wmflabs.org/api_documentation.html.
#    --- Construct the Microsoft graph the old way, show how long it takes!
#    --- Construct the Microsoft graph using `add_edge()` and `wdq`.
#    - Serialization.
#    --- Serializing ConceptModel objects with JSON. Cut out that last bit of the existing notebook and elaborate.
# TODO: Graphistry-based visualize() method.
# Come back to this task in a while, they're working through Unicode errors at the moment, nothing to be done just yet.


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
        # TODO: Assert that a list is passed, otherwise it will decompile the string into letters. Common error!
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
        sorted_edge_tuples = sorted([(self.graph.edge[edge[0]][edge[1]]['weight'], edge[0], edge[1]) for edge in
                                     self.graph.edges()], reverse=True)
        for index, edge_repr in enumerate(sorted_edge_tuples):
            print(str(index), edge_repr[1].concept + ' <- ' + str(edge_repr[0]) + ' -> ' + edge_repr[2].concept)

    def print_concepts(self):
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
        return sorted([(self.graph[edge[0]][edge[1]]['weight'], edge[0].concept, edge[1].concept) for edge in
                       self.graph.edges()], reverse=True)

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

    def remove(self, concept):
        """
        Removes the given concept from the ConceptModel.
        :param concept: The concept being removed from the model.
        """
        self.graph.remove_node(self.get_node(concept))

    def neighborhood(self, concept):
        """
        Returns the "neighborhood" of a concept: a list of (correlation, concept) tuples pointing to/from it,
        plus itself (a concept has a self-correlation of 1!).
        :param concept: The concept to focus in on.
        :return: The neighborhood, represented by a list of edge much like the one returned by `edges()`.
        """
        return sorted([(1, concept)] + [(self.graph[self.get_node(concept)][node]['weight'], node.concept) for node in
                                        self.graph.neighbors(self.get_node(concept))], reverse=True)

    ######################
    # Parameter methods. #
    ######################

    def concepts_by_property(self, prop):
        """
        :param prop: The property to sort the returned output by.
        :return: Returns a list of `(prop, concept)` tuples sorted by prop.
        """
        return sorted([(node.get_property(prop), node.concept) for node in self.nodes()], reverse=True)

    def concepts_by_view_count(self):
        """
        Wrapper for `concepts_by_property(prop)` for the `view_count` case.
        :return: Returns a list of `(view_count, concept)` tuples sorted by `view_count`.
        """
        return self.concepts_by_property('view_count')

    def set_view_counts(self):
        """
        Initializes the view counts for all of the Concept objects in the ConceptModel. See Concept for a
        description of why this parameter is optional.
        """
        for node in self.nodes():
            p = PageviewsClient().article_views("en.wikipedia", [node.concept.replace(' ', '_')])
            p = [p[key][node.concept.replace(' ', '_')] for key in p.keys()]
            p = int(sum([daily_view_count for daily_view_count in p if daily_view_count]) / len(p))
            node.set_property('view_count', p)

    def get_view_count(self, concept):
        """
        Returns the `view_count` of a concept in the `ConceptModel`.
        :param concept: The concept supposedly in the `ConceptModel`.
        :return: The `view_count` int parameter of the concept, if it is found. Throws an error if it is not.
        """
        return self.get_node(concept).get_property('view_count')

    def set_property(self, concept, param, value):
        """
        Sets the `param` property of `concept` to `value`.
        :param concept: Concept being given a parameter.
        :param param: The parameter being given.
        :param value: The value the parameter being given takes on.
        """
        self.get_node(concept).set_property(param, value)

    def map_property(self, prop, func):
        """
        Maps the `param` property of all of the concepts in the ConceptModel object by way of the user-provided `func`.
        :param prop: The parameter being given.
        :param func: The function that is called on the concept in order to determine the value of `prop`.
        """
        for node in self.nodes():
            node.set_property(prop, func(node.concept))

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

    def augment_by_node(self, node, level=0, limit=50):
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
        related_concepts_raw = watsongraph.event_insight_lib.get_related_concepts(node.concept, level=level,
                                                                                  limit=limit)
        if node not in self.nodes():
            self.graph.add_node(node)
        for raw_concept in related_concepts_raw['concepts']:
            # Avoid adding the `A-A` multi-edge returned by the raw `get_related_concepts`.
            if raw_concept['concept']['label'] != node.concept:
                new_node = Node(raw_concept['concept']['label'])
                mixin.graph.add_edge(self.get_node(node.concept), new_node, weight=raw_concept['score'])
        self.merge_with(mixin)

    def augment(self, concept, level=0, limit=50):
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

    def abridge_by_node(self, node, level=0, limit=50):
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

    def abridge(self, concept, level=0, limit=50):
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

    def explode(self, level=0, limit=50):
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

    def expand(self, level=0, limit=50, n=1):
        """
        Expands a graph by augmenting concepts with only one (or no) edge. Warning: for sufficiently large graphs this
        is a slow operation! See also the expand() method for a less focused version of this operation.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        :param n -- The cutoff for the number of neighbors a node can have.
        """
        for concept_node in [node for node in self.nodes() if len(self.graph.neighbors(node)) <= n]:
            self.augment_by_node(concept_node, level=level, limit=limit)

    def intersection_with_by_nodes(self, mixin_concept_model):
        """
        :param mixin_concept_model: Another ConceptModel object to be compared to.
        :return: A list of overlapping concept nodes with their relevance parameters set to average relevance.
        """
        overlapping_concept_nodes = [node for node in self.nodes() if node in mixin_concept_model.nodes()]
        for concept_node in overlapping_concept_nodes:
            if 'relevance' in concept_node.properties.keys():
                concept_node.set_relevance((concept_node.properties['relevance'] + mixin_concept_model.get_node(
                        concept_node.concept).properties['relevance']) / 2)
        return overlapping_concept_nodes

    def add_edges(self, source_concept, list_of_target_concepts, prune=False):
        """
        Given a source concept and a list of target concepts, creates relevance edges between the source and the
        targets and adds them to the graph.
        :param source_concept: The source concept edges are being added from.
        :param list_of_target_concepts: The target concepts edges are being added to.
        :param prune: Watson returns correlations for edges which it does not know enough about as 0.5,
        a lack of extensibility which can cause sizable issues: for example you might have both (0.5, IBM, Apple Inc.)
        and (0.5, IBM, Apple). We as humans know that these are totally not equal comparisons, but the system does not!
        When this parameter is set to True (it is set to False by default) only edges with a correlation higher than
        0.5 are added.
        """
        raw_scores = watsongraph.event_insight_lib.get_relation_scores(source_concept, list_of_target_concepts)
        mixin_graph = nx.Graph()
        mixin_source_node = Node(source_concept)
        for raw_concept in raw_scores['scores']:
            raw_concept['concept'] = raw_concept['concept'].replace('_', ' ')
            if not prune or (prune and raw_concept['score'] > 0.5):
                mixin_concept = raw_concept['concept'][raw_concept['concept'].rfind('/') + 1:]
                if mixin_concept != source_concept:
                    mixin_target_node = Node(mixin_concept)
                    mixin_graph.add_edge(mixin_source_node, mixin_target_node, weight=raw_concept['score'])
        self.graph = nx.compose(self.graph, mixin_graph)

    def add_edge(self, source_concept, target_concept, prune=False):
        """
        Wrapper for `add_edges()` for the single-concept case, so that you don't have to call a list explicitly.
        :param source_concept: The source concept edges are being added from.
        :param target_concept: The target concept an edge is being added to.
        :param prune: Watson returns correlations for edges which it does not know enough about as 0.5,
        a lack of extensibility which can cause sizable issues: for example you might have both (0.5, IBM, Apple Inc.)
        and (0.5, IBM, Apple). We as humans know that these are totally not equal comparisons, but the system does not!
        When this parameter is set to True (it is set to False by default) only edges with a correlation higher than
        0.5 are added.
        """
        self.add_edges(source_concept, [target_concept], prune=prune)

    def explode_edges(self, prune=False):
        """
        Calls `add_edges()` on everything in the model, all at once. Like `explode()` but for concept edges!
        :param prune: Watson returns correlations for edges which it does not know enough about as 0.5,
        a lack of extensibility which can cause sizable issues: for example you might have both (0.5, IBM, Apple Inc.)
        and (0.5, IBM, Apple). We as humans know that these are totally not equal comparisons, but the system does not!
        When this parameter is set to True (it is set to False by default) only edges with a correlation higher than
        0.5 are added.
        """
        c_list = self.concepts()
        for concept in self.concepts():
            c_list.remove(concept)
            if c_list:
                self.add_edges(concept, c_list, prune=prune)

    ###############
    # IO methods. #
    ###############

    def to_json(self):
        """
        Returns the JSON representation of a ConceptModel. Counter-operation to `load_from_dict()`.
        :param self: A ConceptModel.
        :return: The nx dictionary representation of the ConceptModel.
        """
        flattened_model = nx.relabel_nodes(self.graph, {node: node.concept for node in self.nodes()})
        data_repr = json_graph.node_link_data(flattened_model)
        for node in data_repr['nodes']:
            for prop in self.get_node(node['id']).properties.keys():
                node[prop] = self.get_node(node['id']).properties[prop]
        return data_repr

    def load_from_json(self, data_repr):
        """
        Generates a ConceptModel out of a JSON representation. Counter-operation to `to_dict()`.
        :param data_repr: The dictionary being passed to the method.
        :return: The generated ConceptModel.
        """
        flattened_graph = json_graph.node_link_graph(data_repr)
        m = {concept: Node(concept) for concept in flattened_graph.nodes()}
        self.graph = nx.relabel_nodes(flattened_graph, m)
        for node in data_repr['nodes']:
            for key in [key for key in node.keys() if key != 'id']:
                self.set_property(node['id'], key, node[key])

    # def visualize(self, filename='graphistry_credentials.json'):
    #     """
    #     Generates a ConceptModel visualization. WIP. Need to get a graphistry key first...
    #     :param filename -- The filename at which Graphistry service credentials are stored. Defaults to
    #     `graphistry_credentials.json`.
    #     :return: The generated visualization.
    #     """
    #     graphistry_token = import_graphistry_credentials(filename=filename)
    #     graphistry.register(key=graphistry_token)
    #     flattened_model = nx.relabel_nodes(self.graph, {node: node.concept for node in self.nodes()})
    #     flattened_model_dataframe = nx.convert_matrix.to_pandas_dataframe(flattened_model)
    #     for key in flattened_model_dataframe.keys():
    #         flattened_model_dataframe[key] = flattened_model_dataframe[key].astype(str)
    #     g = graphistry.bind(source='source', destination='target')
    #     g.plot(flattened_model_dataframe)


# def import_graphistry_credentials(filename='graphistry_credentials.json'):
#     """
#     Internal method which finds the credentials file describing the token that's needed to access Graphistry
#     services. Graphistry is an alpha-level in-development backend that is used here for visualizing the
#     ConceptModel, so keys are given out on a per-user basis; see https://github.com/graphistry/pygraphistry for more
#     information.
#
#     See also `watsongraph.event_insight_lib.import_credentials()`, which replicates this operation for the (
# required) Concept Insights API service key.
#
#     :param filename -- The filename at which Graphistry service credentials are stored. Defaults to
#     `graphistry_credentials.json`.
#     """
#     if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
#         return json.load(open(filename))['credentials']['key']
#     else:
#         raise IOError(
#                 'The visualization methods that come with the watsongraph library require a Graphistry credentials '
#                 'token to work. Did you forget to define one? For more information refer '
#                 'to:\n\nhttps://github.com/graphistry/pygraphistry#api-key')


def model(user_input):
    """
    Models arbitrary user input and returns an associated ConceptModel. See also the similar `concept.conceptualize`
    static method, which binds arbitrary input to a single concept label instead.

    :param user_input: Arbitrary input, be it a name (e.g. Apple (company) -> Apple Inc.) or a text string (e.g.
    "the iPhone 5C, released this Thursday..." -> iPhone).
    :return: The constructed `ConceptModel` object. Might be empty!
    """
    new_model = ConceptModel()
    if user_input:
        related_concepts_raw = watsongraph.event_insight_lib.annotate_text(user_input)
        new_data = [(raw_concept['concept']['label'], raw_concept['score']) for raw_concept in
                    related_concepts_raw['annotations']]
        for data in new_data:
            new_model.graph.add_node(Node(data[0], relevance=data[1]))
    return new_model
