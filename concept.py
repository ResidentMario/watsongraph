from mwviews.api import PageviewsClient
import hashlib
import event_insight_lib


class Concept:
    """
    The Concept class is an abstraction for IBM Watson Concept Insights API graph endpoints, plus additional
    Wikipedia-derived sugar.
    """

    """
    The IBM Watson API graph node associated with this concept,
    e.g. `"/graphs/wikipedia/en-20120601/concepts/IBM_Watson"`.
    """
    node = ""

    """
    The raw name of the concept associated with its Wikipedia article. e.g. Apple, Apple (company),
    Nirvana (band), as taken from the IBM Watson API. This is the title of the Wikipedia article associated with
    this concept.
    """
    label = ""

    """
    The parsed name of the concept. Apple stays Apple, but Apple (company) becomes just Apple. This parameter is
    a more readable display names than label, but are NOT unique. For comparative purposes the label should be used
    instead; for display purposes this parameter should be the first choice.
    """
    name = ""

    """
    A raw monthly view count of the Wikipedia article associated with the concept. This metric is used as a
    meter-stick of how relatively important this concept is. This is important for when we want to curate the
    concepts in our ConceptModel to more general ones.

    This parameter is left unset by default, and should be set by higher-level operations (using the
    Concept.set_view_count() method). This is done because a lot of potential applications of this library do not
    need a view count at all, without which initialization gains a significant speed bump (because retrieving the
    view count requires networking to the Wikimedia servers, by definition a slow operation).
    """
    view_count = 0

    """
    A measure of the strength of the concept. Used at the User level for tracking the evolution of a concept's
    relevance over time.
    """
    relevance = 0.0

    def __init__(self, label):
        """
        :param label: The node label used to initialize the concept.
        """
        self.node = "/graphs/wikipedia/en-20120601/concepts/" + label.replace(' ', '_')
        self.label = label
        if "(" in self.label:
            self.name = label[:label.find("(")]
        else:
            self.name = label
        # The view_count attribute is left unset by default.
        # self.set_view_count()

    def __str__(self):
        """
        Morphs the string representation of the Concept into its label. Used by the conceptmodel.visualize() plotter.
        :return: The Concept's name string.
        """
        return self.name

    def __eq__(self, other):
        """
        Two concepts are equal when their labels are equivalent.
        """
        if self and other:
            return self.label == other.label
        else:
            return False

    def __hash__(self):
        """
        Two concepts have an equivalent hash if their labels are equivalent.
        """
        return int(hashlib.md5(self.label.encode()).hexdigest(), 16)

    def set_view_count(self):
        """
        Sets the view_count parameter appropriately, using a 30-day average.
        """
        p = PageviewsClient().article_views("en.wikipedia", [self.label.replace(' ', '_')])
        p = [p[key][self.label.replace(' ', '_')] for key in p.keys()]
        p = int(sum([daily_view_count for daily_view_count in p if daily_view_count])/len(p))
        self.view_count = p

    def set_relevance(self, relevance):
        """
        :param relevance: Sets the concept's relevance parameter.
        """
        self.relevance = relevance


def map_user_input_to_concept(user_input):
    """
    Attempts to map arbitrary user input to a valid Concept. If the method is unsuccessful the Concept remains
    unchanged.
    :param user_input: Arbitrary user input, be it a name (e.g. Apple (company) -> Apple Inc.) or a text string (
    e.g. "the iPhone 5C, released this Thursday..." -> iPhone)
    """
    # Fetch the precise name of the node (article title) associated with the institution.
    raw_concepts = event_insight_lib.annotate_text(user_input)
    # If the correction call is successful, keep going.
    if 'annotations' in raw_concepts.keys() and len(raw_concepts['annotations']) != 0:
        matched_concept_node_label = raw_concepts['annotations'][0]['concept']['label']
        return Concept(matched_concept_node_label)
