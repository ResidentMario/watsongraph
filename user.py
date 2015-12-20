# Standard libraries.
import os
import json
# import flask.ext.login as flask_login
# Own libraries.
from conceptmodel import ConceptModel
from concept import map_user_input_to_concept
from conceptmodel import convert_concept_model_to_data, load_concept_model_from_data


# class User(flask_login.UserMixin):
class User:
    """
    The User class implemented for the purposes of Flask-Login.
    Throughout the application, `flask_login.current_user` is the current User() instance.
    """
    id = ''
    password = ''
    model = ConceptModel()
    """The list of events that the user has already expressed interest or disinterest in is stored in their
    'exceptions' field, so as not to repeatedly return the same items to them."""
    exceptions = None

    def __init__(self, model=ConceptModel(), user_id='', exceptions=None, password=''):
        self.id = user_id
        self.model = model
        self.exceptions = exceptions
        self.password = password

    def concepts(self):
        return self.model.concepts()

    def labels(self):
        return self.model.labels()

    def interest_in(self, event):
        """
        :param event: An Event object to be compared to.
        :return: Returns a [0, 1] rating of this user's hypothesized interest in the given event.
        """
        intersection = self.model.intersection_with(event.model)
        if len(intersection) == 0:
            return 0
        else:
            # TODO: Improve the mathematics of this model.
            return sum([concept_node.relevance for concept_node in intersection]) / len(intersection)

    def get_best_event(self, event_list):
        """
        Retrieves the event within a list of events which is most relevant to the given user's interests.
        :param event_list: The list of events to be examined.
        :return:
        """
        best_event = None
        highest_relevance = 0.0
        for event in event_list:
            if self.interest_in(event) >= highest_relevance and event.label not in self.exceptions:
                best_event = event
        return best_event

    def express_interest(self, event):
        # TODO: Model math.
        """
        Merges interest in an event into the user model.
        :param event: Event object the user is expressing interest in.
        """
        self.model.merge_with(event.model)
        self.exceptions.append(event.name)

    def express_disinterest(self, event):
        # TODO: Model math.
        """
        Merges disinterest in an event into the user model.
        :param event: Event object the user is expressing disinterest in.
        """
        self.exceptions.append(event.name)

    def input_interest(self, interest):
        """
        Resolves arbitrary user input to a Concept (using the name-imported Concept.map_user_input_to_concept
        method), explodes that concept, and adds it to the user's present graph.
        :param interest:
        :return:
        """
        # TODO: Model math.
        mapped_concept = map_user_input_to_concept(interest)
        mapped_model = ConceptModel([mapped_concept]).explode()
        self.model.merge_with(mapped_model)

    # ##########################
    # # AUTHENTICATION METHODS #
    # ##########################
    # # flask_login uses these methods for user authentication in the application.
    #
    # def is_authenticated(self):
    #     data = json.load(open(filename))
    #     return self.email in [account['email'] for account in data['accounts']]
    #
    # def is_active(self):
    #     True
    #
    # def is_anonymous(self):
    #     return self.email == ''
    #
    # def get_id(self):
    #     return self.email

#######################
# Read/write methods. #
#######################


def save_user(user, filename='accounts.json'):
    """
    Saves a user to a JSON file.
    :param user: The user to be saved to JSON.
    :param filename: The filename for the account storage file; `accounts.json` is the default.
    """
    user_schema = {
        "password": user.password,
        "model": convert_concept_model_to_data(user.model),
        "id": user.id,
        "exceptions": user.exceptions
    }
    print(str(user_schema))
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
        if user.id not in ids:
            data['accounts'].append(user_schema)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        if user.id in ids:
            user_index = 0
            for i in range(0, len(data['accounts'])):
                if data['accounts'][i]['id'] == user.id:
                    user_index = i
                    break
            data['accounts'][user_index] = user_schema
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)


def load_user(user_id, filename='accounts.json'):
    """
    Saves a user to a JSON file.
    :param user_id: The id (username, email, etc.) of the user to be loaded from the JSON.
    :param filename: The filename for the account storage file; `accounts.json` is the default.
    """
    if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
        raise IOError('Error: accounts file ' + filename + ' not found.')
    else:
        data = json.load(open(filename))
        user_ids = [account['id'] for account in data['accounts']]
        if user_id not in user_ids:
            raise IOError('Error: User with the ID ' + user_id + ' not found in accounts file ' + filename)
        else:
            user_index = 0
            for i in range(0, len(data['accounts'])):
                if data['accounts'][i]['id'] == user_id:
                    user_index = i
                    break
            user_data = data['accounts'][user_index]
            user = User(user_id=user_id,
                        model=load_concept_model_from_data(user_data['model']),
                        exceptions=user_data['exceptions'],
                        password=user_data['password']
                        )
            return user


def update_user_credentials(user, filename='accounts.json'):
    """
    Updates User information in the JSON. This is a seperate method in order to account for password and id
    manipulation (otherwise `save_user()` alone works fine).
    :param user: The User whose data is being manipulated.
    :param filename: The filename for the account storage file; `accounts.json` is the default.
    """
    delete_user(user, filename)
    save_user(user, filename)


def delete_user(user, filename='accounts.json'):
    """
    Deletes a User object from the JSON entirely.
    :param user:
    :param filename: The filename for the account storage file; `accounts.json` is the default.
    """
    if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
        raise IOError('Error: accounts file ' + filename + ' not found.')
    else:
        data = json.load(open(filename))
        user_index = 0
        for i in range(0, len(data['accounts'])):
            if data['accounts'][i]['id'] == user.id:
                user_index = i
                break
        data['accounts'].pop(user_index)
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)
