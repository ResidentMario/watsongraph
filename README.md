# watson-graph
`watson-graph` is a Pythonic concept graphing and recommendation library.
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

## Using the code

Note that in order to use the IBM Watson cognitive APIs you *must* register an account on Bluemix first.

Once you have forked and pulled the code onto your local development machine, you will need to create a
`concept_insight_credentials.json` file containing your [IBM Bluemix](https://console.ng.bluemix.net/) access
credentials. If you do not have an account already you may [register](https://console.ng.bluemix.net/registration/)
for a free trial account. Once you are logged in, enter the catalog, scroll down to the "IBM Watson" section, and
click through to create an instance of the "Concept Insights" service. Go back to the dashboard, click on the newly
populated service, and click through to "Service Credentials" on the sidebar to get your service credentials:
copy-paste this file and save it locally as the aforementioned `concept_insight_credentials.json`. Your credentials
should look something like this:

```
{
  "credentials": {
    "url": "https://gateway.watsonplatform.net/concept-insights/api",
    "username": "........-....-....-....-............",
    "password": "............"
  }
}
```

If you are a developer you may also be interested in reading the [Congitive Insight API documentation](https://watson-api-explorer.mybluemix.net/swagger.html?url=/listings/concept-insights-v2.json#!/graphs/graphLabelSearch).
Note that outside of the thirty-day trial, high-throughput queries to IBM Bluemix can quickly prove costly, but for
experimental purposes the free allotment is more than enough.

Aside from that you will need the `networkx`, `requests`, and `mwviews` packages, all of with are easy to `pip`.

## Examples

### Concept mapping

One way to explore Wikipedia articles (one that has been used pretty exhaustively in the research space) is to crawl
it for links, performing operations of interest on particular articles and then jumping along to the next batch of
links that that page turns up. This library allows for an interesting alternative possibility: exploring Wikipedia
based on topical connections between articles generated not by "dumb" links between pages, but instead by "smart"
learned relationships observed by IBM Watson, perhaps (probably?) the most powerful machine learning system in
development today.

For a peek at what we can do check out the [demo notebook](https://github.com/ResidentMario/watson-graph/blob/master/watson-graph%20-%20ConceptModel%20demo.ipynb)
in this repository.

### User modeling

`watson-graph` provides basic but durable recommendation engine bindings in the form of the `Item` and `User` classes.
The [Cultural Insight](https://github.com/ResidentMario/cultural-insight) repository provides an example of just such
 an application.

Hi, I'm Bob.
```
>>> from user import User
>>> Bob = User(user_id="Bob")
```
I'm kind of crazy about data technologies. Can't get enough of it, really!
```
>>> Bob.input_interests(["Data science", "Machine learning", "Big data", "Cognitive science"])
```
I hear IBM has been doing really cool things with Watson!
```
>>> Bob.input_interest("IBM Watson")
```
I am interested in quite a large number of things, really.
```
>>> Bob.concepts()

['Algorithm', 'Artificial intelligence', 'Association for Computing Machinery', 'Big data', 'Bioinformatics', 'Cloud
 'computing', 'Cognition', 'Cognitive science', 'Computer programming', 'Consciousness', 'Data science', 'Database',
 'Engineering', 'Epistemology', 'Game show', 'IBM', 'Index of psychology articles', 'Index of robotics articles',
 'Java (programming language)', 'List of statistics articles', 'Machine learning', 'Metadata', 'MySQL',
 'Neuroscience', 'Noam Chomsky', 'Normal distribution', 'Oracle Corporation', 'Perl', 'Probability', 'Probability
  distribution', 'Rensselaer Polytechnic Institute', 'SQL', 'Semantics', 'Software as a service', 'Statistics',
 'Supercomputer', 'Syntax', 'Watson (computer)', 'Web search engine', 'Wikipedia']

```

I heard that there is going to be a [NYC Data Wranglers](http://www.meetup.com/NYC-Data-Wranglers/) meet-up soon, I
wonder if I should go?

```
>>> from item import Item
>>> meetup = Item('Data Science in Practice: The New York Times, Greenhouse, Socure, Via, and YipitData',
               'Join us for a discussion panel with data scientists from Greenhouse, the New York Times, Socure, Via,
               and YipitData...[snipped for brevity]')
>>> Bob.interest_in(meetup)
<<< 0.728
```

I guess I'm going!

```
>>> Bob.express_interest(meetup)
```

**Important caveat**: Every concept is associated with the name of a Wikipedia article, so it's important to make sure
that any concepts
you attempt to plug into your model directly correspond exactly with the titles of their corresponding articles. For
example, Wikipedia has a page for `Bayes' theorem` - but not for `Bayes' Theorem` or for `Bayes' law`. Thus calling
`stochastic_topics.add("Bayes' law")` would work but would cause problems down the line. Instead if you are inputting
 a concept label that is reasonably close to the correct one you can explicitly run it through Watson to sanitize
 the input and make it safe for use:

```
>>> from node import conceptualize
>>> conceptualize("Bayes' theorem")
'Bayes' theorem'
>>> conceptualize("Bayes' law")
'Bayes' theorem'
>>> conceptualize("Bayes")
'Thomas Bayes'
>>> conceptualize("Met")
'Metropolitan Opera'
>>> conceptualize("Smithsonian Museum")
'Smithsonian Institution'
```

It is especially crucial that you run this on anything you are given which is user-defined!

## Documentation

This library is still in active development; more documentation is forthcoming.