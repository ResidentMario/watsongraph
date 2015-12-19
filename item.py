from conceptmodel import ConceptModel
import os
import json
import event_insight_lib

# Every augmentation is the ConceptModel of a new user-indicated Item of interest. I have to come up with some sort
# of mathematically justified way of merging this new Item into the old model: decaying the old nodes and reinforcing
# the overlap.
# Idea: every iteration the existing non-overlapping nodes lose 1/10 of their current relevance. Newly added nodes
# come in at high relevance (.9?). Overlapping elements gain half of the distance between their sum and 1.


class Item:
    """
    The Item object is a generic container for the objects that the application is trying to recommend to its users.
    In this application, Item is extended by Event. In other scenarios it would be extended by e.g. Talk, Recipe, etc.
    It contains two parts: a string textual description of the event, `description` (what is mined for the Item's
    concepts); And the model produced by mining these concepts.
    """
    description = ""
    name = ""
    model = None

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.model = ConceptModel()
        # Create the associated ConceptModel.
        related_concepts_raw = event_insight_lib.annotate_text(self.description)
        new_labels = [raw_concept['concept']['label'] for raw_concept in related_concepts_raw['annotations']]
        for label in new_labels:
            self.model.augment(label)

    # TODO: Rewrite.
    def delete_item(self, filename="items.json"):
        if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
            raise IOError('Error: events file ' + filename + ' not found.')
        else:
            data = json.load(open(filename))
            event_index = 0
            for i in range(0, len(data['events'])):
                if data['events'][i]['name'] == self.name:
                    events_index = i
                    break
            data['events'].pop(event_index)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)

    # TODO: Rewrite.
    def compare_to(self, other_item):
        """
        Compares two Items and returns a measure of average overlap (a mock correlation).
        :param other_item: The other Item to be merged into the current one.
        """
        pass