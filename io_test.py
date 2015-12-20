from event import Event, save_event, load_event
from user import User, save_user, load_user, update_user_credentials
from concept import Concept
from conceptmodel import ConceptModel, convert_concept_model_to_data, load_concept_model_from_data

mock_user = User(model=ConceptModel([Concept('IBM'), Concept('Microsoft'), Concept('Apple Inc.')]),
                 user_id='test@baruchmail.cuny.edu',
                 exceptions=None,
                 password='Test')
mock_event = Event("Apple", "Apple Inc. is an American multinational technology company headquartered in Cupertino, "
                   "California, that designs, develops, and sells consumer electronics, computer software, "
                   "and online services. Its hardware products include the iPhone smartphone, the iPad tablet "
                   "computer, the Mac personal computer, the iPod portable media player, and the Apple Watch "
                   "smartwatch. Apple's consumer software includes the OS X and iOS operating systems, the iTunes "
                   "media player, the Safari web browser, and the iLife and iWork creativity and productivity "
                   "suites. Its online services include the iTunes Store, the iOS App Store and Mac App Store, "
                   "and iCloud.")
u_d = convert_concept_model_to_data(mock_user.model)
e_d = convert_concept_model_to_data(mock_event.model)
print("User-assigned labels: " + str(mock_user.labels()))
print("Event-assigned labels: " + str(mock_event.labels()))
print("User storage conversion: " + str(u_d))
print("Event storage conversion: " + str(e_d))
print("Attempting to convert user model data back into ConceptModel...")
print("Got: " + str(load_concept_model_from_data(e_d).labels()))
print("Attempting to save the user model...")
save_user(mock_user)
print("OK.")
print("Attempting to load the user model...")
mock_user = load_user('test@baruchmail.cuny.edu')
print(mock_user.labels())
print("OK.")
print("Attempting to save the event model...")
save_event(mock_event)
print("OK.")
print("Attempting to load the event model...")
mock_event = load_event(mock_event.name)
print(mock_event.labels())
print("OK.")
print("Attempting to update user credentials...")
print("User id before updating: " + mock_user.id)
mock_user.id = 'apple@baruchmail.cuny.edu'
update_user_credentials(mock_user)
mock_user = load_user('apple@baruchmail.cuny.edu')
print("User id after updating: ")
print(mock_user.id)
