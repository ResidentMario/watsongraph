import itertools
import event_insight_lib
import backend

class ConceptModel:
	"""The ConceptModel object is a container for the user's concept model."""
	maturity = 1
	model = dict()

	def __init__(self, model=dict(), maturity=1):
		self.model = model
		self.maturity = maturity

	def loadModel(self, email, filename='accounts.json'):
		"""Given the email of a registered user, loads a single user's model out of the accounts list."""
		list_of_users = json.load(open(filename))['accounts']
		for user in list_of_users:
			if user['email'] == email:
				self.model = user['model']['concepts']
				break

	def saveModel(self, filename='accounts.json'):
		"""Given the concept model and email of a registered user, saves their model to the accounts list."""
		data = json.load(open(filename))
		for i in range(0, len(data['accounts'])):
			if data['accounts'][i]['email'] == self.email:
				data['accounts'][i]['model']['concepts'] = self.model
				break
		# Re-encode and save the modified file.
		with open(filename, 'w') as outfile:
			json.dump(data, outfile, indent=4)

	def iterateModel(self, merger_concept_model, cutoff=0.2, mean=0.5):
		"""
		This method merges a second ConceptModel object into the current one, using a running average.
		This method implements a cutoff (lower relevancies fall of the edge) and a mean (the model is continuously rebalanced).
		Returns the merged ConceptModel object.
		"""
		# Rank the concepts in each set into two ordered lists.
		bK = sorted(self.model.keys())
		mK = sorted(merger_concept_model.model.keys())
		# Create a placeholder model and iterate its maturity.
		new_concept_model = ConceptModel(maturity=self.maturity + merger_concept_model.maturity)
		# Zip them into longest-match tuple pairs and iterate through, merging them as we go along.
		for pair in itertools.zip_longest(bK, mK, fillvalue=None):
			if pair[0] == pair[1]:
				left_relevance = self.model[pair[0]]
				right_relevance = merger_concept_model.model[pair[0]]
				new_model_relevance_raw = (left_relevance * self.maturity + right_relevance * merger_concept_model.maturity) / self.maturity
				new_model_relevance = round(new_model_relevance_raw, 3)
				new_concept_model.model[pair[0]] = new_model_relevance
			else:
				if pair[0] != None:
					relevance = self.model[pair[0]]
					new_model_relevance = round((relevance * self.maturity) / self.maturity, 3)
					new_concept_model.model[pair[0]] = new_model_relevance
				if pair[1] != None:
					relevance = merger_concept_model.model[pair[1]]
					new_model_relevance = round((relevance * merger_concept_model.maturity) / self.maturity, 3)
					new_concept_model.model[pair[1]] = new_model_relevance
		# Remean the concept list.
		new_concept_model.remean(mean)
		# Remove the elements of the list which fall below the cutoff.
		# print([self.model[item] for item in self.model])
		irrelevants = [item for item in new_concept_model.model if new_concept_model.model[item] <= cutoff]
		print(irrelevants)
		for item in irrelevants:
			del new_concept_model.model[item]
		# Set the current model to the optimized merged one.
		self.maturity = new_concept_model.maturity
		self.model = new_concept_model.model

	def remean(self, mean=0.5):
		"""
		Analytical method.
		Rebalances the values in the given concept list around the given mean.
		Called by `iterateModel()`.
		NOTE: Float storage in Python (as elsewhere) has prominent floating-point representation issues.
		This doesn't matter too much in the code itself, but when displaying, be sure to optimize away from display 4.99999... using e.g.:
		print('%.3f' % round(mean - current_mean, 3))
		"""
		keys = self.model.keys()
		size = len(keys)
		if size == 0:
			return self.model
		total = 0
		for key in keys:
			total += self.model[key]
		current_mean = total/size
		for key in keys:
			self.model[key] += round(mean - current_mean, 3)
		return self.model

	def addUserInputToConceptModel(self, user_input, cutoff=0.2):
		"""
		This method attempts to resolve user input (`input`) into a list of related concepts.
		At issue is the fact that user input has to be resolved somehow to the name of the nearest Wikipedia article, not always easy.
		In cases where this is not possible, this method will return a False flag.
		In cases where this happens as desired, this method will return a True flag.
		"""
		# Fetch the precise name of the node (article title) associated with the institution.
		concept_node = event_insight_lib.annotateText(user_input, backend.getToken())
		# If the correction call is successful, keep going.
		if 'annotations' in concept_node.keys() and len(concept_node['annotations']) != 0:
			concept_node_title = concept_node['annotations'][0]['concept']['label']
			related_concepts = event_insight_lib.fetchRelatedConcepts(concept_node_title, backend.getToken())
			model = backend.parseRawConceptCall(related_concepts, cutoff)
			new_concept_model = ConceptModel(model=model, maturity=1)
			self.iterateModel(new_concept_model)
			return True
		# Otherwise, if the call was not successful, return a False flag.
		else:
			return None

	def addEventToConceptModel(self, event_text, cutoff=0.2):
		"""
		In the case that we are resolving a known concept, we can skip the verification step present in the above method.
		We also use a different Watson API call entirely to retrieve what we want.
		"""
		merger_model = ConceptModel(model=backend.parseRawEventCall(event_insight_lib.annotateText(event_text, backend.getToken()), cutoff))
		self.iterateModel(merger_model)

	def addExplodedConceptToConceptModel(self, concept, cutoff=0.2):
		"""
		In the case that we are resolving a known concept, we can skip the verification step present in the above method.
		We also use a different Watson API call entirely to retrieve what we want.
		"""
		pass