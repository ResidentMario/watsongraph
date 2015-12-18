from item import Item
from time import strftime, gmtime
import os
import json

from conceptmodel import ConceptModel

class Event(Item):
	"""
	The Event class extends the Item class, and is the container for the events this application is trying to recommend to its users.
	NOTE: Events that have been manipulated using ConceptModel() have a `maturity` entry associated with their dictionary representation.
	This piece of information is not yet used for anything, but may prove helpful in the future.
	"""
	starttime = []
	endtime = []
	location = ""
	picture = ""
	url = ""

	def __init__(self, description="", starttime=[], endtime=[], location="", picture="", name="", url=""):
		super().__init__(description=description, name=name)
		self.starttime = starttime
		self.endtime = endtime
		self.location = location
		self.url = url
		self.picture = picture

	def loadEvent(self, name, filename="events.json"):
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			raise IOError("The item definitions file" + filename + "  appears to be missing!")
		list_of_items = json.load(open(filename))['events']
		for item in list_of_items:
			# print(name + '\n' + item['name'])
			if item['name'] != name:
				continue
			else:
				self.name = name
				self.description = item['description']
				self.model = ConceptModel(model=item['model']['concepts'])
				self.start_time = item['starttime']
				self.end_time = item['endtime']
				self.location = item['location']
				self.url = item['url']
				self.picture = ['picture']
				return
		raise IOError("The item " + name + "was not found!")

	def saveEvent(self, filename="events.json"):
		event_schema = {
			"name": self.name,
			"model": {
				"concepts": self.model.graph,
				"maturity": self.model.maturity
			},
			"description": self.description,
			"starttime": self.starttime,
			"endtime": self.endtime,
			"location": self.location,
			"url": self.url,
			"picture": self.picture
		}
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			new_file_schema = {
				"events":
					[event_schema]
			}
			f = open(filename, 'w')
			f.write(json.dumps(content, indent=4))
			f.close()
		else:
			data = json.load(open(filename))
			names = [event['name'] for event in data['events']]
			if self.name not in names:
				data['events'].append(event_schema)
				with open(filename, 'w') as outfile:
					json.dump(data, outfile, indent=4)
			if self.name in names:
				user_index = 0
				for i in range(0, len(data['events'])):
					if data['events'][i]['name'] == self.name:
						user_index = i
						break
				data['events'][user_index] = event_schema
				with open(filename, 'w') as outfile:
					json.dump(data, outfile, indent=4)

	def deleteEvent(self, filename="events.json"):
		self.deleteItem(filename)