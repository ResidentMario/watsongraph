# noinspection PyUnresolvedReferences
from mwviews.api import PageviewsClient
import event_insight_lib
# noinspection PyUnresolvedReferences
import networkx as nx


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
    """
    view_count = 0

    def __init__(self, label, simple=False):
        """
        :param label: The node label used to initialize the concept.
        :param simple: Set to "False" by default, which causes this method to populate the view_count parameter.
        Set this flag to True for a speed bump if you don't need view counting.
        """
        self.node = "/graphs/wikipedia/en-20120601/concepts/" + label.replace(' ', '_')
        self.label = label
        self.name = label[:label.find("(") - 1]
        # Retrieve and parse article page views. Take the daily average of the number of views over the last 30 days.
        if not simple:
            self.get_view_count()

    def __str__(self):
        return "<Concept: '" + self.label + "'>"

    def get_view_count(self):
        """
        Sets the view_count parameter appropriately, using a 30-day average.
        """
        p = PageviewsClient().article_views("en.wikipedia", [self.label.replace(' ', '_')])
        p = [p[key][self.label.replace(' ', '_')] for key in p.keys()]
        p = int(sum([daily_view_count for daily_view_count in p if daily_view_count])/len(p))
        self.view_count = p

    def get_related_concepts_graph(self, level=0, limit=10, simple=False):
        """
        Returns a networkx (nx) directed graph (anchored tree) of concepts related to the current one, suitable for
        assignment to a ConceptModel object.

        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        :param simple -- Set to "False" by default, which causes this method to populate the view_count parameters
        of all of the discovered related Concept objects. This procedure is very slow, however, because it
        requires making up to `limit` sequential calls against the Wikipedia API. So set this flag to True for a
        significant speed bump if you don't need view counting.
        :return: Returns a ConceptModel of related concepts (an anchored tree).
        """
        rel_graph = nx.Graph(simple=simple)
        related_concepts_raw = event_insight_lib.get_related_concepts(self.label)
        for raw_concept in related_concepts_raw['concepts']:
            # Remove the `A-A` edge returned by the raw `get_related_concepts` class.
            if raw_concept['concept']['label'] != self.label:
                new_node = Concept(raw_concept['concept']['label'], simple=simple)
                rel_graph.add_edge(self, new_node, weight=raw_concept['score'])
        return rel_graph
