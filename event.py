from item import Item
# import os
# import json


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
        super().__init__(name, description)
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.picture = picture
        self.url = url

    # def loadEvent(self, name, filename="events.json"):
    #     if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
    #         raise IOError("The item definitions file" + filename + "  appears to be missing!")
    #     list_of_items = json.load(open(filename))['events']
    #     for item in list_of_items:
    #         # print(name + '\n' + item['name'])
    #         if item['name'] != name:
    #             continue
    #         else:
    #             self.name = name
    #             self.description = item['description']
    #             self.model = ConceptModel(model=item['model']['concepts'])
    #             self.start_time = item['start_time']
    #             self.end_time = item['end_time']
    #             self.location = item['location']
    #             self.url = item['url']
    #             self.picture = ['picture']
    #             return
    #     raise IOError("The item " + name + "was not found!")
    #
    # def saveEvent(self, filename="events.json"):
    #     event_schema = {
    #         "name": self.name,
    #         "model": {
    #             "concepts": self.model.graph,
    #             "maturity": self.model.maturity
    #         },
    #         "description": self.description,
    #         "start_time": self.start_time,
    #         "end_time": self.end_time,
    #         "location": self.location,
    #         "url": self.url,
    #         "picture": self.picture
    #     }
    #     if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
    #         new_file_schema = {
    #             "events":
    #                 [event_schema]
    #         }
    #         f = open(filename, 'w')
    #         f.write(json.dumps(content, indent=4))
    #         f.close()
    #     else:
    #         data = json.load(open(filename))
    #         names = [event['name'] for event in data['events']]
    #         if self.name not in names:
    #             data['events'].append(event_schema)
    #             with open(filename, 'w') as outfile:
    #                 json.dump(data, outfile, indent=4)
    #         if self.name in names:
    #             user_index = 0
    #             for i in range(0, len(data['events'])):
    #                 if data['events'][i]['name'] == self.name:
    #                     user_index = i
    #                     break
    #             data['events'][user_index] = event_schema
    #             with open(filename, 'w') as outfile:
    #                 json.dump(data, outfile, indent=4)
    #
    # def deleteEvent(self, filename="events.json"):
    #     self.delete_item(filename)
