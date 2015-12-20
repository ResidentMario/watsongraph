from conceptmodel import ConceptModel
from conceptmodel import convert_concept_model_to_data, load_concept_model_from_data
from concept import Concept

mock_model = ConceptModel([Concept('IBM'), Concept('IBM Watson')])
d = convert_concept_model_to_data(mock_model)
print(d)
mock_model_loaded = load_concept_model_from_data(d)
print(mock_model_loaded.labels())
print(mock_model_loaded.maturity)