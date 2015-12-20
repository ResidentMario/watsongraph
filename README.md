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

Aside from that you will need the `networkx`, `requests`, and `mwviews` packages, all of with are easy to `pip`.

## Examples

Hi, I'm Bob.
```
Bob = User(user_id="Bob")
```
I'm kind of crazy about data technologies. Can't get enough of it, really!
```
Bob.input_interests(["Data science", "Machine learning", "Big data", "Cognitive science"])
```
I hear IBM has been doing really cool things with Watson!
```
Bob.input_interest("IBM Watson")
```

...