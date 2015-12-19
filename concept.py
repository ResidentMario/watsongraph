from mwviews.api import PageviewsClient
import event_insight_lib
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
        # Retrieve and parse article page views. Take the daily average of the number of views over the last 30 days.
        self.set_view_count()

    def __str__(self):
        """
        Morphs the string representation of the Concept into its label. Used by the conceptmodel.visualize() plotter.
        :return: The Concept's name string.
        """
        return self.name

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

    def expand(self, level=0, limit=10):
        """
        Returns a networkx (nx) directed graph (anchored tree) of concepts related to the current one, suitable for
        assignment to a ConceptModel object. Note that what this function returns is *not* a ConceptModel object
        itself! Just an nx graph that can be assigned to one!

        The action of mining a concept and then linking it to a pre-existing graph is known as "expanding" it,
        a terminology used throughout this library.

        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        :return: Returns a ConceptModel of related concepts (an anchored tree). Note that this is *not* a
        ConceptModel object itself! Just an nx graph that can be assigned to one!
        """
        rel_graph = nx.Graph()
        related_concepts_raw = event_insight_lib.get_related_concepts(self.label, level=level, limit=limit)
        for raw_concept in related_concepts_raw['concepts']:
            # Remove the `A-A` edge returned by the raw `get_related_concepts` class.
            if raw_concept['concept']['label'] != self.label:
                new_node = Concept(raw_concept['concept']['label'])
                rel_graph.add_edge(self, new_node, weight=raw_concept['score'])
        return rel_graph
