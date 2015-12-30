from mwviews.api import PageviewsClient
import hashlib
import watsongraph.event_insight_lib


class Node:
    """
    The IBM Watson Concept Insights API is based on a weighted graph of Wikipedia pages. Each vertex in the graph
    corresponds to an individual article, referred to as a "node". This "Node" object class abstracts these nodes.
    """

    """
    The name of the Wikipedia article associated with the node, e.g. Apple, Apple Inc., Nirvana (band), etc.
    "Label" is the terminology used by the IBM Watson API for this attribute; "Concept" is the terminology used
    instead by this library (we are building a `ConceptModel()` not a `LabelModel()`!).
    """
    concept = ""

    """
    A dictionary of arbitrary parameter:value tuples. `view_count` and `relevance` are two such parameters which
    have baked-in support, but the point of this abstraction is that the user ought to be able to extend the data saved
    in the ConceptModel object however they want to.
    """
    properties = None

    # TODO: Refactor view_count and relevance as two examples of user-definable arbitrary properties.
    # 1. Create a `props` parameter, an initially empty dict of property:value tuples.
    # 2. In `conceptmodel` create a `set_property(concept, property, value)` method for writing to it.
    # 3. In `conceptmodel` create a `give_property(map)` method for writing to it via a function.
    # 4. Rewrite the `conceptmodel` methods which set relevance directly to do so via `set_relevance()`.
    # 5. Re-frame `view_count` and `relevance` as two use-cases of `props` which are supported by default.
    #    e.g. rewrite `set_view_count()` and `set_relevance()`.
    # 6. Rewrite `conceptmodel` `to_json()` and `from_json()` methods to pass `props` materials around.

    def __init__(self, concept, **kwargs):
        """
        :param concept: The raw concept used to initialize the node.
        :param kwargs: A list of property:value tuples to be passed to the `properties` parameter.
        """
        self.concept = concept
        self.properties = kwargs
        if not self.properties:
            self.properties = dict()

    def __eq__(self, other):
        """
        Two `Node` objects are equal when their `concept` attributes are the same string.
        """
        if self and other:
            return self.concept == other.concept
        else:
            return False

    def __hash__(self):
        """
        Two concepts have an equivalent hash if their labels are equivalent. Comparison-by-hash is overwritten this
        way to support `nx.compose()` as used in `conceptmodel.merge_with()`.
        """
        return int(hashlib.md5(self.concept.encode()).hexdigest(), 16)

    def set_view_count(self):
        """
        Sets the view_count parameter appropriately, using a 30-day average.
        """
        p = PageviewsClient().article_views("en.wikipedia", [self.concept.replace(' ', '_')])
        p = [p[key][self.concept.replace(' ', '_')] for key in p.keys()]
        p = int(sum([daily_view_count for daily_view_count in p if daily_view_count])/len(p))
        # self.view_count = p
        self.properties['view_count'] = p
        print(self.properties['view_count'])

    def set_relevance(self, relevance):
        """
        :param relevance: Sets the concept's relevance parameter.
        """
        # self.relevance = relevance
        self.set_property('relevance', relevance)

    def get_relevance(self):
        """
        :return: The concept's relevance parameter.
        """
        return self.get_property('relevance')

    def set_property(self, prop, value):
        """
        :param prop: The property to be stored.
        :param value: The value being stored.
        """
        self.properties.update({prop: value})

    def get_property(self, prop):
        """
        :param prop: The property to be retrieved.
        """
        return self.properties[prop]


def conceptualize(user_input):
    """
    Attempts to map arbitrary textual input to a valid Concept. If the method is unsuccessful no Concept is
    returned. See also the similar `conceptmodel.model` static method, which binds arbitrary input to an entire
    ConceptModel instead.
    :param user_input: Arbitrary input, be it a name (e.g. Apple (company) -> Apple Inc.) or a text string (e.g.
    "the iPhone 5C, released this Thursday..." -> iPhone).
    """
    # Fetch the precise name of the node (article title) associated with the institution.
    raw_concepts = watsongraph.event_insight_lib.annotate_text(user_input)
    # If the correction call is successful, keep going.
    if 'annotations' in raw_concepts.keys() and len(raw_concepts['annotations']) != 0:
        matched_concept_node_label = raw_concepts['annotations'][0]['concept']['label']
        return matched_concept_node_label
