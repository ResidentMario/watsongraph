# watsongraph
`watsongraph` is a Pythonic concept graphing and recommendation library.
The library's core `ConceptModel` objects is constructed out of the individual concept nodes which are associated with
labels from the IBM Watson `wikipedia/en-20120601` cognitive graph, queried using the
[Concept Insights API](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/concept-insights.html) and
reconstructed locally as a [networkx](https://networkx.github.io/)-based weighted conceptual graph.

Nodes are defined by `Concept` objects, each mapped to a unique Wikipedia page, which are in turn
connected to one another by edges demarcating relevance (on a 0-to-1 probabilistic scale) within a
`ConceptMap` object.

This `ConceptMap` can then be associated with any number of applications. Basic bindings are provided, in particular,
 for a recommendation service based on `Item` and `User` classes.

An example of a web application using this code is provided in the [cultural-insight](https://github.com/ResidentMario/cultural-insight) repository.

## Setup

`watsongraph` is [available on PyPi](https://pypi.python.org/pypi/watsongraph/): to get it simply call `pip install
 watsongraph`.

In order to use the IBM Watson cognitive APIs you **must** register an account on Bluemix first.

Once you have the code locally, you will need to create a `concept_insight_credentials.json` file containing your
[IBM Bluemix](https://console.ng.bluemix.net/) access credentials. If you do not have an account already you may
[register](https://console.ng.bluemix.net/registration/) for a free trial account. Once you are logged in, enter the
catalog, scroll down to the "IBM Watson" section, and click through to create an instance of the "Concept Insights"
service. Go back to the dashboard, click on the newly populated service, and click through to "Service Credentials"
on the sidebar to get your service credentials: copy-paste this file and save it locally as the aforementioned
`concept_insight_credentials.json`. Your credentials should look something like this:

```
{
  "credentials": {
    "url": "https://gateway.watsonplatform.net/concept-insights/api",
    "username": "........-....-....-....-............",
    "password": "............"
  }
}
```

Note that outside of the thirty-day trial, high-throughput queries to IBM Bluemix can quickly prove costly, but for
experimental purposes the free allotment is more than enough.

## Examples

### Concept mapping

One way to explore Wikipedia articles (one that has been used pretty exhaustively in the research space) is to crawl
it for links, performing operations of interest on particular articles and then jumping along to the next batch of
links that that page turns up. This library allows for an interesting alternative possibility: exploring Wikipedia
based on topical connections between articles generated not by "dumb" links between pages, but instead by "smart"
learned relationships observed by IBM Watson, perhaps (probably?) the most powerful machine learning system in
development today.

For a peek at what you can do check out the [demo notebook](https://github.com/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Concept%20Mapping%20Demo.ipynb)
in this repository.

### User modeling

This library provides basic but durable and highly extendible facilities for constructing an IBM Watson Cognitive
Insights -based user recommendation service. The two classes of interest provided here are `User` and `Item`.
`ConceptModel` objects are implicit in both of these classes but have been elegantly abstracted away from.

For a peek at what you can do check out the [other demo notebook](https://github.com/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Recommendations%20Demo.ipynb)
in this repository.

Refer to the [Cultural Insight](https://github.com/ResidentMario/cultural-insight) repository for a complete web
application using this library in this manner.

For further inspiration you can also try out IBM's own
[example application](https://concept-insights-demo.mybluemix.net/) (which predates this library).