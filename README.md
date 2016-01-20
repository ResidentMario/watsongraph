# watsongraph
`watsongraph` is a Pythonic concept graphing and recommendation library.
The library's core `ConceptModel` objects is constructed out of the individual concept nodes which are associated with
labels from the IBM Watson `wikipedia/en-20120601` cognitive graph, queried using the
[Concept Insights API](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/concept-insights.html) and
reconstructed locally as a [networkx](https://networkx.github.io/)-based weighted conceptual graph.

Each node in the `ConceptModel` is mapped to a corresponding unique Wikipedia page, and nodes are in turn connected
to another by "relevance edges" (in range the range 0 to 1, a probabilistic scale). This `ConceptModel` can then be
associated with any number of applications. Basic bindings are provided, in particular, for a recommendation service
using library-provided `Item` and `User` classes.

This code is `Python 3`-only for the moment.

## Setup

`watsongraph` is [available on PyPi](https://pypi.python.org/pypi/watsongraph/): to get it simply call `pip install
 watsongraph`.

However, in order to use the IBM Watson cognitive APIs you **must** register for it on Bluemix first. In particular,
once you have the code locally, you will need to create a `concept_insight_credentials.json` file
containing your [IBM Bluemix](https://console.ng.bluemix.net/) access credentials. If you do not have an account
already you may [register](https://console.ng.bluemix.net/registration/) for a free trial account. Once you are
logged in, enter the catalog, scroll down to the "IBM Watson" section, and click through to create an instance of the
"Concept Insights" service. Go back to the dashboard, click on the newly populated service, and click through to
"Service Credentials" on the sidebar to get your service credentials: copy-paste this file and save it locally as
the aforementioned `concept_insight_credentials.json`. Your credentials should look something like this:

```
{
  "credentials": {
    "url": "https://gateway.watsonplatform.net/concept-insights/api",
    "username": "........-....-....-....-............",
    "password": "............"
  }
}
```

Note that outside of the thirty-day trial IBM Watson is a paid service, but for experimental purposes the monthly free
allotment (25,000 queries) is more than enough.

## Documentation

This library's Sphinx documentation is available on [Read The Docs](http://watsongraph.readthedocs.org/en/latest/).

## Examples

### Concept mapping

One way to explore Wikipedia articles (one that has been used pretty exhaustively in the research space) is to crawl
it for links, performing operations of interest on particular articles and then jumping along to the next batch of
links that that page turns up. This library allows for an interesting alternative possibility: exploring Wikipedia
based on topical connections between articles generated not by "dumb" links between pages, but instead by "smart"
learned relationships observed by IBM Watson, perhaps (probably?) the most powerful machine learning system in
development today.

For example:

```
>>> from watsongraph.conceptmodel import ConceptModel
>>> ibm = ConceptModel(['IBM'])
>>> ibm.explode()
>>> ibm.concepts()
['.NET Framework', 'ARM architecture', 'Advanced Micro Devices', ...]
>>> len(ibm.concepts())
37
>>> 'Server (computing)' in ibm.concepts()
True
>>> ibm.augment('Server (computing)')
>>> len(ibm.concepts())
58
>>> ibm.edges()
[(0.89564085, 'IBM', 'Digital Equipment Corporation'),
 (0.8793883, 'Solaris (operating system)', 'Server (computing)'),
 ...
]

```

The [ConceptModel demo notebook](https://github.com/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Concept%20Mapping%20Demo.ipynb)
provides a detailed walkthrough of basic `ConceptModel` operations. To learn how to use this library, start here.


The [Advanced Concept Modeling demo notebook](https://github.com/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Advanced%20Concept%20Modeling.ipynb)
provides a detailed walkthrough of advanced `ConceptModel` features as well as recommendations about how to use them
for modelling. To learn more about how best to apply this library, go here (but read the above first!).

### User modeling

This library provides basic but durable and highly extendible facilities for constructing an IBM Watson Cognitive
Insights -based user recommendation service. The two classes of interest provided here are `User` and `Item`.
`ConceptModel` objects are implicit in both of these classes but have been abstracted away from.

For example:

```
>>> from watsongraph.user import User
>>> from watsongraph.item import Item
>>> Bob = User(user_id="Bob")
>>> Bob.input_interests(["Data science", "Machine learning", "Big data", "Cognitive science"])
>>> meetup = Item("Meetup", "This is a description of a pretty awesome event...")
>>> relay = Item("Relay", "This is a description of another pretty awesome event...")
>>> Bob.interest_in(meetup)
1.633861635
>>> Bob.interest_in(relay)
1.54593405
# Update the "Bob" model to account for our new information on Bob's preferences.
>>> Bob.express_interest(meetup)
```

To learn how to apply this library to user modeling see the [Recommendations Modeling demo notebook](https://github.com/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Recommendations.ipynb)
in this repository.

For further inspiration you can also try out IBM's own
[example application](https://concept-insights-demo.mybluemix.net/) (which predates this library).