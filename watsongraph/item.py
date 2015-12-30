import os
import json
from watsongraph.conceptmodel import ConceptModel
from watsongraph.conceptmodel import model as model_input

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

    def __init__(self, name="", description=""):
        """
        Loads an `Item` object from its description and an associated name.
        :param name: The Item's name.
        :param description: A textual description of what the Item is about or describes. This is mined at
        initialization for the concepts which are associated with this Item's ConceptModel().
        """
        self.name = name
        self.description = description
        if len(description) > 0:
            self.model = model_input(description)
        else:
            self.model = ConceptModel()
        # Item relevancies are instantiated to 0.0 in order to support operations on it in the `User` class.
        for concept in self.model.concepts():
            self.model.set_property(concept, 'relevance', 0.0)

    def nodes(self):
        """
        :return: The nodes in the Item model.
        """
        return self.model.nodes()

    def concepts(self):
        """
        :return: The concepts in the Item model.
        """
        return self.model.concepts()

    def relevancies(self):
        """
        :return: Sorted (relevance, concept) pairs associated with the Item.
        """
        return sorted([(node.properties['relevance'], node.concept) for node in self.nodes()], reverse=True)

    def to_json(self):
        """
        Returns a JSON of the Item object suitable for storage. Counter-operation to `load_from_json()`.
        :return: A JSON serialization of the Item object which is suitable for storage.
        """
        return {
            "name": self.name,
            "model": self.model.to_json(),
            "description": self.description,
        }

    def load_from_json(self, data):
        """
        Loads an Item from its JSON serialization. Counter-operation to `to_json()`.
        :param data: The JSON data being loaded into an Item object.
        """
        self.model.load_from_json(data['model'])
        self.description = data['description']

    def save(self, filename='items.json'):
        """
        Saves the Item to a JSON representation.
        :param filename: The filename for the items storage file; `items.json` is the default.
        """
        item_schema = self.to_json()
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
            if self.name not in names:
                data['items'].append(item_schema)
                with open(filename, 'w') as outfile:
                    json.dump(data, outfile, indent=4)
            if self.name in names:
                user_index = 0
                for i in range(0, len(data['items'])):
                    if data['items'][i]['name'] == self.name:
                        user_index = i
                        break
                data['items'][user_index] = item_schema
                with open(filename, 'w') as outfile:
                    json.dump(data, outfile, indent=4)

    def load(self, filename="items.json"):
        """
        Loads the Item from a JSON representation.
        :param filename: The filename for the items storage file; `items.json` is the default.
        """
        if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
            raise IOError("The item definitions file" + filename + "  appears to be missing!")
        list_of_items = json.load(open(filename))['items']
        for item in list_of_items:
            if item['name'] != self:
                continue
            else:
                self.load_from_json(item)
