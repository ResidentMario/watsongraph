import os
import json
import statistics
from watsongraph.conceptmodel import ConceptModel
from watsongraph.node import conceptualize


class User:
    """
    The application's User has their preferences stored in their own ConceptModel().
    """
    id = ''
    password = ''
    model = None
    """The list of events that the user has already expressed interest or disinterest in is stored in their
    'exceptions' field, so as not to repeatedly return the same items to them."""
    exceptions = []

    def __init__(self, model=ConceptModel(), user_id='', exceptions=None, password=''):
        """
        :param model: The ConceptModel() initially associated with the user. An empty one by default.
        :param user_id: The id associated with the user. An empty string by default.
        :param exceptions: The exceptions (items already viewed and either acted upon or passed on) associated with the
        user.
        :param password: The password associated with the user. An empty string by default.
        """
        self.id = user_id
        self.model = model
        if exceptions:
            self.exceptions = exceptions
        self.password = password

    def nodes(self):
        """
        :return: The Concept() objects associated with the user's model.
        """
        return self.model.nodes()

    def concepts(self):
        """
        :return: The labels of the concepts associated with the user's model.
        """
        return self.model.concepts()

    def interests(self):
        """
        :return: Returns (interest, concept) pair tuples associated with the user.
        """
        return sorted([(node.get_relevance(), node.concept) for node in self.model.nodes()], reverse=True)

    def interest_in(self, item):
        """
        :param item: An Item object to be compared to.
        :return: Returns a float that rates this user's hypothesized interest in the given event, based on the
        intersection between their own ConceptModel and that of the examined Event.
        """
        intersection = self.model.intersection_with_by_nodes(item.model)
        if len(intersection) == 0:
            return 0
        else:
            return sum([concept_node.get_relevance() for concept_node in intersection])

    def get_best_item(self, item_list):
        """
        Retrieves the event within a list of events which is most relevant to the given user's interests.
        :param item_list: The list of Event objects to be examined.
        :return: The Event which best matches the user's interests.
        """
        best_item = None
        highest_relevance = 0.0
        for item in item_list:
            if self.interest_in(item) >= highest_relevance and item.name not in self.exceptions:
                best_item = item
        return best_item

    def express_interest(self, item):
        """
        Merges interest in an event into the user model. Adds the Item in which interest has been expressed to the
        exceptions.
        :param item: Event object the user is expressing interest in.
        """
        # Raise correlated relevancies.
        item_copy = item.model.copy()
        # self.model.merge_with(item.model)
        for concept in [concept for concept in item.concepts() if concept in self.concepts()]:
            new_relevance = min(1.0, statistics.mean([self.model.get_node(concept).get_relevance(),
                                                      item.model.get_node(concept).get_relevance()]) * 1.2)
            item_copy.get_node(concept).properties['relevance'] = new_relevance
        # Bump down uncorrelated relevancies.
        for concept in [concept for concept in self.concepts() if concept not in item_copy.concepts()]:
            self.model.get_node(concept).properties['relevance'] *= 0.9
        # Remove irrelevant concepts (to keep the model relatively clean).
        self.model.merge_with(item_copy)
        for concept in [concept for concept in self.concepts() if self.model.get_node(concept).get_relevance() <= 0.2]:
            self.model.remove(concept)
        self.exceptions.append(item.name)

    def express_disinterest(self, item):
        """
        Merges disinterest in an event into the user model. Adds the Item in which interest has been expressed to the
        exceptions.
        :param item: Event object the user is expressing disinterest in.
        """
        self.exceptions.append(item.name)
        # Scale down overlapping concepts.
        for concept in [concept for concept in item.concepts() if concept in self.concepts()]:
            self.model.get_node(concept).properties['relevance'] *= 0.75
        # Remove irrelevant concepts (to keep the model relatively clean).
        for concept in [concept for concept in self.concepts() if self.model.get_node(concept).get_relevance() <= 0.2]:
            self.model.remove(concept)

    def input_interest(self, interest, level=0, limit=20):
        """
        Resolves arbitrary user input to concepts, explodes the resultant nodes, and adds the resultant graph to the
        user's present one.
        :param interest: Arbitrary user input.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        mapped_concept = conceptualize(interest)
        if mapped_concept:
            mapped_model = ConceptModel([mapped_concept])
            mapped_model.get_node(mapped_concept).properties['relevance'] = 1.0
            mapped_model.explode(level=level, limit=limit)
            # Set relevancies based on edge weights.
            for node in list(mapped_model.graph[mapped_model.get_node(mapped_concept)].keys()):
                node.properties['relevance'] = mapped_model.graph[mapped_model.get_node(mapped_concept)][node]['weight']
            self.model.merge_with(mapped_model)

    def input_interests(self, interests, level=0, limit=20):
        """
        Resolves a series of arbitrary user inputs to concepts, explodes the resultant nodes, and adds the resultant
        graph to the user's present one.
        :param interests: Arbitrary user input.
        :param level -- The limit placed on the depth of the graph. A limit of 0 is highest, corresponding with the
        most popular articles; a limit of 5 is the broadest and graphs to the widest cachet of articles. This
        parameter is a parameter that is passed directly to the IBM Watson API call.
        :param limit -- a cutoff placed on the number of related concepts to be returned. This parameter is passed
        directly to the IBM Watson API call.
        """
        for interest in interests:
            self.input_interest(interest, level=level, limit=limit)

    #######################
    # Read/write methods. #
    #######################

    def save_user(self, filename='accounts.json'):
        """
        Saves a user to a JSON file.
        :param self: The user to be saved to JSON.
        :param filename: The filename for the account storage file; `accounts.json` is the default.
        """
        user_schema = {
            "password": self.password,
            "model": self.model.to_json(),
            "id": self.id,
            "exceptions": self.exceptions
        }
        if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
            new_file_schema = {
                "accounts":
                    [user_schema]
            }
            f = open(filename, 'w')
            f.write(json.dumps(new_file_schema, indent=4))
            f.close()
        else:
            data = json.load(open(filename))
            ids = [account['id'] for account in data['accounts']]
            if self.id not in ids:
                data['accounts'].append(user_schema)
                with open(filename, 'w') as outfile:
                    json.dump(data, outfile, indent=4)
            if self.id in ids:
                user_index = 0
                for i in range(0, len(data['accounts'])):
                    if data['accounts'][i]['id'] == self.id:
                        user_index = i
                        break
                data['accounts'][user_index] = user_schema
                with open(filename, 'w') as outfile:
                    json.dump(data, outfile, indent=4)

    def load_user(self, filename='accounts.json'):
        """
        Load a user from a JSON file.
        :param filename: The filename for the account storage file; `accounts.json` is the default.
        """
        if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
            raise IOError('Error: accounts file ' + filename + ' not found.')
        else:
            data = json.load(open(filename))
            user_ids = [account['id'] for account in data['accounts']]
            if self.id not in user_ids:
                raise IOError('Error: User with the ID ' + self.id + ' not found in accounts file ' + filename)
            else:
                user_index = 0
                for i in range(0, len(data['accounts'])):
                    if data['accounts'][i]['id'] == self.id:
                        user_index = i
                        break
                user_data = data['accounts'][user_index]
                self.id = user_data['id']
                self.model.load_from_json(user_data['model'])
                self.exceptions = user_data['exceptions']
                if not self.exceptions:
                    self.exceptions = []
                self.password = user_data['password']

    def update_user_credentials(self, filename='accounts.json'):
        """
        Updates User information in the JSON. This is a seperate method in order to account for password and id
        manipulation (otherwise `save_user()` alone works fine).
        :param filename: The filename for the account storage file; `accounts.json` is the default.
        """
        self.delete_user(filename)
        self.save_user(filename)

    def delete_user(self, filename='accounts.json'):
        """
        Deletes a User object from the JSON entirely.
        :param filename: The filename for the account storage file; `accounts.json` is the default.
        """
        if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
            raise IOError('Error: accounts file ' + filename + ' not found.')
        else:
            data = json.load(open(filename))
            user_index = 0
            for i in range(0, len(data['accounts'])):
                if data['accounts'][i]['id'] == self.id:
                    user_index = i
                    break
            data['accounts'].pop(user_index)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)
