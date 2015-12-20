# watson-recommend
This repository defines a concept graphing and recommendation construction engine. Individual concept "nodes" are
associated with labels from the IBM Watson `en-20120601` cognitive graph, which is queried using the [Concept Insights API](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/concept-insights.html)
and reconstructed locally as a [networkx](https://networkx.github.io/)-based weighted conceptual graph.

Vertices (nodes) are defined by `Concept` objects, each mapped to a unique Wikipedia page, which are in turn
connected to one another by edges demarcating relevance (on a 0-to-1 probabilistic scale) within a
`ConceptMap` object.

This `ConceptMap` can then be associated with any number of applications. The one provided here is a recommendation
system: graphs are constructed mapping the conceptual content of sets of `Item` and `User` objects. Each `User` may
then use their map to find `Item` recommendations which best fit their own conceptual interests.

An example of a web application using this code is provided in the [cultural-insight](https://github.com/ResidentMario/cultural-insight) repository.

## Using the code

Note that in order to use the IBM Watson cognitive APIs you *must* register an account on Bluemix first.

Once you have forked and pulled the code onto your local development machine, you will need to create a `token.json`
file containing your [IBM Bluemix](https://console.ng.bluemix.net/) access credentials. If you do not have an
account already you may [register](https://console.ng.bluemix.net/registration/) for a free trial account. Once you
are logged in, enter the catalog, scroll down to the "IBM Watson" section, and click through to create an instance
of the "Concept Insights" service. Go back to the dashboard, click on the newly populated service, and click through
 to "Service Credentials" on the sidebar to get your service credentials: copy-paste this file and save it locally
 as the aforementioned `token.json`. Your credentials should look something like this:

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

Here's a peek at what we can do.

```
>>> from conceptmodel import ConceptModel
```

Let's populate a simple conceptual graph.

```
>>> stochastic_topics = ConceptModel(['Markov chain', 'Random walk', 'Brownian motion'])
```

Note that this only adds exactly those nodes to the graphs.

```
>>> stochastic_topics.labels()
['Brownian motion', 'Markov chain', 'Random walk']
```

To extrapolate forward from this we can `explode()` our graph.

```
>>> stochastic_topics.explode()
>>> stochastic_topics.labels()

['Brownian motion', 'Continuous function', 'Eigenvalues and eigenvectors', 'Function (mathematics)', 'Graph theory',
 'Integral', 'List of statistics articles', 'Markov chain', 'Matrix (mathematics)', 'Normal distribution',
 'Probability', 'Probability distribution', 'Quantum field theory', 'Random walk', 'Real number', 'Statistics']
```

We can also use `expand` to focus-expand only those nodes that have less than some number `n` existing edges.

Speaking of edges...

```
>>> stochastic_topics.print_edges()

1: Probability distribution <-> Brownian motion
2: Probability distribution <-> Markov chain
3: Probability distribution <-> Random walk
4: Integral <-> Brownian motion
5: Matrix (mathematics) <-> Markov chain
6: Matrix (mathematics) <-> Random walk
...[snipped for brevity]...
```

Analysis tools are in continued development.

### User modeling

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
>>> Bob.labels()

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
>>> from event import Event
>>> meetup = Event('Data Science in Practice: The New York Times, Greenhouse, Socure, Via, and YipitData',
               'Join us for a discussion panel with data scientists from Greenhouse, the New York Times, Socure, Via,
               and YipitData...[snipped for brevity]')
>>> Bob.interest_in(meetup)
<<< 0.728
```

Guess I'm going!


## Documentation

This library is still in active development. Lot more documentation will be written up once it's in a more polished
state!