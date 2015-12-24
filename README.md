# watson-graph
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

Here's a peek at what we can do.

```
>>> from conceptmodel import ConceptModel
```

Let's populate a simple conceptual graph.

```
>>> stochastic_topics = ConceptModel(['Markov chain', 'Random walk']
>>> stochastic_topics.add('Brownian motion')
>>> stochastic_topics.concepts()

['Brownian motion', 'Markov chain', 'Random walk']
```

To extrapolate forward from this we can `explode()` our graph. This expands every concept in the model.

```
>>> stochastic_topics.explode()
>>> stochastic_topics.concepts()

['Albert Einstein', 'Algorithm', 'Bioinformatics', 'Brownian motion', 'Complex number', 'Continuous function',
'Eigenvalues and eigenvectors', 'Fluid dynamics', 'Function (mathematics)', 'General relativity', 'Graph theory',
'Group (mathematics)', 'Index of physics articles', 'Integer', 'Integral', 'List of people by Erd\u0151s number',
'List of statistics articles', 'List of theorems', 'Markov chain', 'Matrix (mathematics)', 'Natural number', 'Normal
 distribution', 'Polynomial', 'Probability', 'Probability distribution', 'Quantum field theory', 'Quantum
 mechanics', 'Random walk', 'Real number', 'Statistics', 'Thermodynamics', 'Vector space', 'Viscosity']
```

We can also choose to `augment()` only a specific concept. This will explode only that concept and add it to the
graph. The concept we choose to `augment()` does not necessarily already have to be in the graph.

```
>>> stochastic_topics = ConceptModel(['Markov chain', 'Random walk', 'Brownian motion'])
>>> stochastic_topics.augment('Random walk')
>>> stochastic_topics.concepts()

['Brownian motion', 'Complex number', 'Continuous function', 'Eigenvalues and eigenvectors', 'Function (mathematics)
', 'Graph theory', 'Group (mathematics)', 'Integer', 'Integral', 'List of people by Erd\u0151s number', 'List of
statistics articles', 'List of theorems', 'Markov chain', 'Matrix (mathematics)', 'Normal distribution',
'Polynomial', 'Probability', 'Probability distribution', 'Quantum field theory', 'Random walk', 'Real number',
'Statistics', 'Vector space']
```

`edges()` presents us with a list of the `(concept, concept, correlation)` tuples associated with the model:

```
>>> stochastic_topics.edges()

[('Probability distribution', "Bayes' theorem", 0.9638752),
 ('Integral', "Bayes' theorem", 0.6774791),
 ("Bayes' theorem", 'Statistics', 0.8829379),
 ("Bayes' theorem", 'Artificial intelligence', 0.61295384),
 ("Bayes' theorem", 'Real number', 0.7393193),
 ...[snipped for brevity]...
]
```

Use the `model()` method to map entire strings to new `ConceptMap` objects.

```
>>> from conceptmodel import model
>>> new_model = model("When applied, the probabilities involved in Bayes' theorem may have different probability
interpretations. In one of these interpretations, the theorem is used directly as part of a particular approach to
statistical inference. With the Bayesian probability interpretation the theorem expresses how a subjective degree of
 belief should rationally change to account for evidence: this is Bayesian inference, which is fundamental to
 Bayesian statistics. However, Bayes' theorem has applications in a wide range of calculations involving pr
 obabilities, not just in Bayesian inference.")
>>> new_model.concepts()

["Bayes' theorem", 'Bayesian inference', 'Bayesian probability', 'Bayesian statistics', 'Interpretation (logic)',
'Probability', 'Probability interpretations', 'Rationality', 'Statistical inference', 'Theorem']
```


**Important caveat**: Every concept is associated with the name of a Wikipedia article, so it's important to make sure
that any concepts
you attempt to plug into your model directly correspond exactly with the titles of their corresponding articles. For
example, Wikipedia has a page for `Bayes' theorem` - but not for `Bayes' Theorem` or for `Bayes' law`. Thus calling
`stochastic_topics.add("Bayes' law")` would work but would cause problems down the line. Instead if you are inputting
 a concept label that is reasonably close to the correct one you can explicitly run it through Watson again to map
 it directly:

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