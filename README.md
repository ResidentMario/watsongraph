[![Documentation Status](https://readthedocs.org/projects/watsongraph/badge/?version=latest)](http://watsongraph.readthedocs.org/en/latest/?badge=latest)
[![PyPi version](https://img.shields.io/pypi/v/watsongraph.svg)](https://pypi.python.org/pypi/watsongraph/)

# watsongraph
`watsongraph` is a concept discovery, graphing, and processing library written in `Python 3`. The library's
core facility is the `ConceptModel` object, a conceptual graph constructed out of the individual concept nodes
associated with labels from the IBM Watson `wikipedia/en-20120601` Wikipedia-derived conceptual graph. This graph is
queried using the [Concept Insights API](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/concept-insights.html)
and then reconstructed locally as a `networkx`-based weighted conceptual graph:

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

The `ConceptModel` can then be associated with any number of applications. Basic bindings are provided, in
particular, for a recommendation service using library-provided `Item` and `User` classes:

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

## Setup

`watsongraph` is [available on PyPi](https://pypi.python.org/pypi/watsongraph/) and can be downloaded locally with `pip
install watsongraph`.

However, in order to use IBM Watson cognitive APIs you **must** first register an account on
[IBM Bluemix](https://console.ng.bluemix.net/). If you do not
have an account already you may [register](https://console.ng.bluemix.net/registration/) for a free trial account.

Once you are logged in, enter the catalog, scroll down to the "IBM Watson" section, and click through to create an
instance of the
[Concept Insights](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/concept-insights.html) service. Go
 back to the dashboard, click on the newly populated service, and click through to "Service Credentials" on the
 sidebar to get your service credentials: copy-paste this `json` output and save it locally as
 `concept_insight_credentials.json`. Your credentials should look like this:

```
{
  "credentials": {
    "url": "https://gateway.watsonplatform.net/concept-insights/api",
    "username": "........-....-....-....-............",
    "password": "............"
  }
}
```

Account access is provided on a thirty-day free trial basis by default, however there is free monthly allotment
(25,000 queries), more than enough for experimental purposes.

## Documentation and examples

* "[Exploring the IBM Watson Concept Insights service using watsongraph](http://www.residentmar.io/2016/02/11/watsongraph-visualization.html)"
is a blog post on my personal website which explores the capacities and use cases for the `watsongraph` library. If
you are curious about how it works, the visualizations here are the best place to start!
* The [ConceptModel Jupyter notebook](http://nbviewer.jupyter.org/github/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Concept%20Modeling.ipynb)
provides a detailed walkthrough of basic `ConceptModel` operations. To learn how to use this library, start here,
then move on to the two notebooks below.
* The [Advanced Concept Modeling Jupyter notebook](http://nbviewer.jupyter.org/github/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Advanced%20Concept%20Modeling.ipynb)
provides a detailed walkthrough of advanced `ConceptModel` features as well as recommendations about how to use them
for modeling.
* The [Recommendations Modeling Jupyter notebook](http://nbviewer.jupyter.org/github/ResidentMario/watsongraph/blob/master/watsongraph%20-%20Recommendations.ipynb)
applies `watsongraph` to user recommendation modeling.
* The [Sphinx documentation](http://watsongraph.readthedocs.org/en/latest/) is the reference manual for all
`watsongraph` methods.
* For further inspiration you can also try out IBM's own
[example application](https://concept-insights-demo.mybluemix.net/) (which predates this library).

## Contributing

The `watsongraph` library is currently in its first stable release, so it is still in a fairly early state of
development: there are quite a large number of improvements and new features which could potentially be made. At the
moment I am waiting for work to finish on the [Watson Developer Cloud Python SDK](https://github.com/watson-developer-cloud/python-sdk)
so that  I can make a large volume of low-level architectural improvements (and add a few new features) for the next
planned stable release, `0.3.0`. You can see the milestone composite issues in this repository's
[issue tracker](https://github.com/ResidentMario/watsongraph/issues?q=is%3Aopen+is%3Aissue+milestone%3A0.3.0).

To pull the latest build onto your development machine, [clone](https://help.github.com/articles/cloning-a-repository/) this repository
(`git clone https://github.com/ResidentMario/cultural-insight.git`) and follow the instructions in [setup](#Setup) to
populate your access credentials.

To submit a minor fix just submit a [pull request](https://help.github.com/articles/using-pull-requests/). Be sure
to explain what problem your change addresses!

If you are interested in contributing new features or major enhancements, we should talk! You can submit an [issue](https://guides.github.com/features/issues/)
or [pull request](https://help.github.com/articles/using-pull-requests/) summarizing the work using the "Enhancement"
 label. You can also [filter](https://github.com/ResidentMario/watsongraph/labels/enhancement)
to enhancements to see what's already on the radar.

I am very receptive to feedback and would defintely like to see this code reviewed by others, you can reach out to me
at `aleksey@residentmar.io`.
