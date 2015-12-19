from item import Item

i = Item('Test', 'The Corpora endpoint allows users to upload their own set of documents into Concept Insights, while organizing them into collections. The raw documents are processed by our system, and automatically annotated and indexed. The analysis and indexing of documents becomes automatically accessible through query methods of this endpoint.')
i.model.print_nodes()
i2 = Item('Test2', 'Then, one of the guys from plotly reached out saying I should take a look. I took a brief glance '
                   'and realised that this was nothing like a new matplotlib and in fact looked pretty cool. So I dutifully put it on my to do list but very much near the bottom.')
print(i.compare_to(i2))