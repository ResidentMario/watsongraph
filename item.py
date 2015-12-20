from conceptmodel import ConceptModel
from concept import Concept
import os
import json
import event_insight_lib
from conceptmodel import convert_concept_model_to_data, load_concept_model_from_data

# Every augmentation is the ConceptModel of a new user-indicated Item of interest. I have to come up with some sort
# of mathematically justified way of merging this new Item into the old model: decaying the old nodes and reinforcing
# the overlap.
# Idea: every iteration the existing non-overlapping nodes lose 1/10 of their current relevance. Newly added nodes
# come in at high relevance (.9?). Overlapping elements gain half of the distance between their sum and 1.

# TODO: compare() method for measuring the overlap between two items.


class Item:
    """
    The Item object is a generic container for the objects that the application is trying to recommend to its users.
    In the example application this class is extended by Event; it could also be extended by a class like Recipe,
    Talk, etc. In case you want to use Item as a standalone class (for experimentation or whatever else),
    JSON saving and loading binds are also provided for this class.
    """
    description = ""
    name = ""
    model = None

    def __init__(self, name, description):
        """
        :param name: The Item's name.
        :param description: A textual description of what the Item is about or describes. This will be mined for the
        concepts which are associated with this Item's ConceptModel().
        :return:
        """
        self.name = name
        self.description = description
        self.model = ConceptModel()
        if description:
            # Create the associated ConceptModel.
            related_concepts_raw = event_insight_lib.annotate_text(self.description)
            new_labels = [raw_concept['concept']['label'] for raw_concept in related_concepts_raw['annotations']]
            for label in new_labels:
                self.model.add(Concept(label))
            # Set the relevance parameters of the underlying Concepts to 1.0 to start off with.
            for concept in self.model.concepts():
                concept.relevance = 1

    def concepts(self):
        """
        :return: The concepts in the Item model.
        """
        return self.model.concepts()

    def labels(self):
        """
        :return: The labels for the concepts in the Item model.
        """
        return self.model.labels()

#######################
# Read/write methods. #
#######################


def save_item(item, filename='items.json'):
    """
    Saves the Item to a JSON representation.
    :param item: The Item object to be saved to JSON.
    :param filename: The filename for the items storage file; `items.json` is the default.
    """
    item_schema = {
        "name": item.name,
        "model": convert_concept_model_to_data(item.model),
        "description": item.description,
    }
    if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
        new_file_schema = {
            "items":
                [item_schema]
        }
        f = open(filename, 'w')
        f.write(json.dumps(new_file_schema, indent=4))
        f.close()
    else:
        data = json.load(open(filename))
        names = [item['name'] for item in data['items']]
        if item.name not in names:
            data['items'].append(item_schema)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        if item.name in names:
            user_index = 0
            for i in range(0, len(data['items'])):
                if data['items'][i]['name'] == item.name:
                    user_index = i
                    break
            data['items'][user_index] = item_schema
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)


def load_item(name, filename="events.json"):
    """
    Loads the Item from a JSON representation.
    :param name: The name of the Item object to be loaded from JSON (corresponds with the `Item.name` parameter).
    :param filename: The filename for the items storage file; `items.json` is the default.
    """
    if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
        raise IOError("The item definitions file" + filename + "  appears to be missing!")
    list_of_items = json.load(open(filename))['events']
    for item in list_of_items:
        if item['name'] != name:
            continue
        else:
            ret_item = Item(name, "")
            ret_item.model = load_concept_model_from_data(item['model'])
            ret_item.description = item['description']
            return ret_item
    raise IOError("The item " + name + "was not found!")