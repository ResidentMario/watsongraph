import os
import json

import flask.ext.login as flask_login
from conceptmodel import ConceptModel
from event import Event
# Replace the above with whatever Class you yourself decide to implement.

# class User(flask_login.UserMixin):
# NOTE: If User stops working return to the generic above and hide the 
class User():
	"""
	The User class implemented for the purposes of Flask-Login.
	Throughout the application, `flask_login.current_user` is the current User() instance.
	"""
	email = ''
	password = ''
	model = ConceptModel()
	exceptions = []

	def __init__(self, model=ConceptModel(), email='', exceptions=[], password=''):
		self.email = email
		self.id = email
		self.model = model
		self.exceptions = exceptions
		self.password = password

	##########################
	# AUTHENTICATION METHODS #
	##########################
	# flask_login uses these methods for user authentication in the application.

	def is_authenticated(self):
		data = json.load(open(filename))
		return self.email in [account['email'] for account in data['accounts']]

	def is_active(self):
		True

	def is_anonymous(self):
		return self.email == ''

	def get_id(self):
		return self.email

	################
	# USER METHODS #
	################
	# These methods were written for the purposes of this script.

	def loadUser(self, email, filename='accounts.json'):
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			raise IOError('Error: accounts file ' + filename + ' not found.')
		else:
			data = json.load(open(filename))
			emails = [account['email'] for account in data['accounts']]
			if email not in emails:
				raise IOError('Error: User with the ID ' + email + ' not found in accounts file ' + filename)
			else:
				user_index = 0
				for i in range(0, len(data['accounts'])):
					if data['accounts'][i]['email'] == email:
						user_index = i
						break
				user_data = data['accounts'][user_index]
				user = User(email=email,
							model=ConceptModel(model=user_data['model']['concepts'],
												maturity = user_data['model']['maturity']),
							exceptions=user_data['exceptions'],
							password=user_data['password']
							)
				return user

	def updateUser(self, email='', exceptions=[], model=ConceptModel(), password='', maturity=0, filename='accounts.json'):
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			raise IOError('Error: accounts file ' + filename + ' not found.')
		else:
			if password:
				self.password = password
			if email:
				self.updateEmail(email)
				self.email = email
			if exceptions:
				self.exceptions = exceptions
			if model != ConceptModel():
				self.model = model
			if maturity:
				self.model.maturity = maturity
			self.saveUser(filename=filename)

	def saveUser(self, filename='accounts.json'):
		user_schema = {
			"password": self.password,
			"model": {
				"concepts": self.model.graph,
				"maturity": self.model.maturity
			},
			"email": self.email,
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
			emails = [account['email'] for account in data['accounts']]
			if self.email not in emails:
				data['accounts'].append(user_schema)
				with open(filename, 'w') as outfile:
					json.dump(data, outfile, indent=4)
			if self.email in emails:
				user_index = 0
				for i in range(0, len(data['accounts'])):
					if data['accounts'][i]['email'] == self.email:
						user_index = i
						break
				data['accounts'][user_index] = user_schema
				with open(filename, 'w') as outfile:
					json.dump(data, outfile, indent=4)

	def deleteUser(self, filename='accounts.json'):
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			raise IOError('Error: accounts file ' + filename + ' not found.')
		else:
			data = json.load(open(filename))
			user_index = 0
			for i in range(0, len(data['accounts'])):
				if data['accounts'][i]['email'] == self.email:
					user_index = i
					break
			data['accounts'].pop(user_index)
			with open(filename, 'w') as outfile:
				json.dump(data, outfile, indent=4)

	def getConceptModel(self):
		return self.model

	def getPassword(self, filename='accounts.json'):
		"""Retrieves the user's password from the data."""
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			raise IOError('Error: accounts file ' + filename + ' not found.')
		else:
			data = json.load(open(filename))
			emails = [account['email'] for account in data['accounts']]
			if self.email not in emails:
				raise IOError('Error: User with the ID ' + self.email + ' not found in accounts file ' + filename)
			else:
				user_index = 0
				for i in range(0, len(data['accounts'])):
					if data['accounts'][i]['email'] == self.email:
						user_index = i
						break
				return data['accounts'][user_index]['password']

	def getBestEvent(self, filename='events.json'):
		"""Returns the event most relevant to this user's interests."""
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			raise IOError('Error: events file ' + filename + ' not found.')
		data = json.load(open(filename))
		best_event = Event()
		best_score = 0
		for event in data['events']:
			iter_event = Event()
			# The declarations are split to keep the Item __init__ method for automatically calling the API to populate the model.
			iter_event.description = event['description']
			iter_event.name = event['name']
			iter_event.model = ConceptModel(model=event['model']['concepts'], maturity=1)
			iter_event.starttime = event['starttime']
			iter_event.endtime = event['endtime']
			iter_event.location = event['location']
			iter_event.picture = event['picture']
			iter_event.name = event['name']
			iter_event.url = event['url']
			score = best_event.compareTo(iter_event)
			if score >= best_score:
				# print(self.exceptions)
				if iter_event.name not in self.exceptions:
					best_event = iter_event
					best_score = score
		return best_event

	#########################
	# CONCEPTMODEL WRAPPERS #
	#########################
	# The following methods are wrapper methods that pass the call to a User object's ConceptModel object.
	# This unifies the front-end by focusing all front-end methods on the user, not on their associated ConceptModel.

	def addUserInputToConceptModel(self, user_input, cutoff=0.2):
		self.model.addUserInputToConceptModel(user_input, cutoff)

	def addEventToConceptModel(self, event_text, cutoff=0.2):
		self.model.addEventToConceptModel(event_text, cutoff)

	def addExplodedConceptToConceptModel(self, concept, cutoff=0.2):
		self.model.addExplodedConceptToConceptModel(concept, cutoff)