import os
import json
from item import Item
from conceptmodel import convert_concept_model_to_data, load_concept_model_from_data


class Event(Item):
    """
    The Event class extends the Item class, and is the container for the events this application is trying to
    recommend to its users.
    """
    start_time = None
    end_time = None
    location = ""
    picture = ""
    url = ""

    def __init__(self, name, description, start_time=None, end_time=None, location="", picture="", url=""):
        """
        :param name: The name of the event. Required.
        :param description: A textual description of the event. Required.
        :param start_time: Event start time. Defaults to None.
        :param end_time: Event end time. Default to None.
        :param location: Location. Defaults to an empty string.
        :param picture: A picture of or from the event, defaults to an empty string.
        :param url: The URL of the event, where you can go to learn more. Defaults to an empty string.
        """
        super().__init__(name, description)
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.picture = picture
        self.url = url

#######################
# Read/write methods. #
#######################


def save_event(event, filename='events.json'):
    """
    Saves the Event to a JSON representation.
    :param event: The name of the Event object to be loaded from JSON (corresponds with the `Item.name` parameter).
    :param filename: The filename for the events storage file; `events.json` is the default.
    """
    event_schema = {
        "name": event.name,
        "model": convert_concept_model_to_data(event.model),
        "description": event.description,
        "start_time": event.start_time,
        "end_time": event.end_time,
        "location": event.location,
        "url": event.url,
        "picture": event.picture
    }
    if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
        new_file_schema = {
            "events":
                [event_schema]
        }
        f = open(filename, 'w')
        f.write(json.dumps(new_file_schema, indent=4))
        f.close()
    else:
        data = json.load(open(filename))
        names = [event['name'] for event in data['events']]
        if event.name not in names:
            data['events'].append(event_schema)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        if event.name in names:
            user_index = 0
            for i in range(0, len(data['events'])):
                if data['events'][i]['name'] == event.name:
                    user_index = i
                    break
            data['events'][user_index] = event_schema
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)


def load_event(name, filename="events.json"):
    """
    Loads the Event from a JSON representation.
    :param name: The name of the Event object to be loaded from JSON (corresponds with the `Item.name` parameter).
    :param filename: The filename for the events storage file; `events.json` is the default.
    """
    if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
        raise IOError("The item definitions file" + filename + "  appears to be missing!")
    list_of_items = json.load(open(filename))['events']
    for item in list_of_items:
        if item['name'] != name:
            continue
        else:
            event = Event(name, item['description'])
            event.model = load_concept_model_from_data(item['model'])
            event.start_time = item['start_time']
            event.end_time = item['end_time']
            event.location = item['location']
            event.url = item['url']
            event.picture = ['picture']
            return event
    raise IOError("The item " + name + "was not found!")
