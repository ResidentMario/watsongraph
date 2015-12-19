from event import Event
from user import User
from concept import Concept
from conceptmodel import ConceptModel

mock_user = User()
mock_user.model = ConceptModel([Concept('IBM'), Concept('Microsoft'), Concept('Apple Inc.')])
mock_event = Event("Apple", "Apple Inc. is an American multinational technology company headquartered in Cupertino, "
                   "California, that designs, develops, and sells consumer electronics, computer software, "
                   "and online services. Its hardware products include the iPhone smartphone, the iPad tablet "
                   "computer, the Mac personal computer, the iPod portable media player, and the Apple Watch "
                   "smartwatch. Apple's consumer software includes the OS X and iOS operating systems, the iTunes "
                   "media player, the Safari web browser, and the iLife and iWork creativity and productivity "
                   "suites. Its online services include the iTunes Store, the iOS App Store and Mac App Store, "
                   "and iCloud.")
print(mock_event.model.labels())
print(str(mock_user.model.intersection_with(mock_event.model)))
mock_correlation = mock_user.interest_in(mock_event)
print(mock_correlation)
mock_best_event = mock_user.get_best_event([mock_event])
print(mock_best_event.name)
