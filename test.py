import backend
from conceptmodel import ConceptModel
from user import User
from event import Event

user = User().loadUser('test@baruchmail.cuny.edu', filename='accounts.json')
print(user.email + str(user.model.model))

# User testing.
user = backend.User(email='test_new@baruchmail.cuny.edu', exceptions=['Test'], password='Testing')
user.saveUser(filename='test.json')
user.saveUser()
user.loadUser('test@baruchmail.cuny.edu', filename='accounts.json')
print(user.email)
user.updateUser(maturity=5, filename='test.json')
print(user.model.maturity)
user.deleteUser(filename='test.json')
user_index = int([data['accounts'].index(account) for account in data['accounts'] if account['email'] == self.email][0])
print(user_index)

# ConceptModel merging testing.
a = b = ConceptModel(model={'A': 0.1, 'B': 0.05})
a.iterateModel(b)
print('`iterateModel()` test for two same-definition ConceptModel objects.\n' + str(a.model))
a = ConceptModel(model={'A': 0.5, 'B':0.2})
b = ConceptModel(model={'C': 0.1, 'D': 0.1})
a.iterateModel(b, cutoff=0.5)
print('`iterateModel()` test for two different-definition ConceptModel objects.\n' + str(a.model))
print('Before' + str(a.model))
a.addUserInputToConceptModel('Test')
a.addEventToConceptModel('The Intrepid Museum’s new exhibition On the Line: Intrepid and the Vietnam War explores the events and impact of the Vietnam War through the lens of Intrepid’s history. The exhibition, which opened in 2015 to mark the 40th anniversary of the conclusion of the war, offers a site-specific immersion into an important chapter of American history. The legendary aircraft carrier Intrepid served three tours of duty in Vietnam between 1966 and 1969. Set within the very spaces where men lived and served, the exhibition focuses on the experiences of Intrepid and its crew “on the line”—the periods when the ship was active in the Gulf of Tonkin, launching aircraft for missions over mainland Vietnam. This localized history serves as the starting point for understanding the larger historical landscape, including the Cold War, Operation Rolling Thunder and protests at home.')
print('After' + str(a.model))

i = Event(description='The Intrepid Museum’s new exhibition On the Line: Intrepid and the Vietnam War explores the events and impact of the Vietnam War through the lens of Intrepid’s history. The exhibition, which opened in 2015 to mark the 40th anniversary of the conclusion of the war, offers a site-specific immersion into an important chapter of American history. The legendary aircraft carrier Intrepid served three tours of duty in Vietnam between 1966 and 1969. Set within the very spaces where men lived and served, the exhibition focuses on the experiences of Intrepid and its crew “on the line”—the periods when the ship was active in the Gulf of Tonkin, launching aircraft for missions over mainland Vietnam. This localized history serves as the starting point for understanding the larger historical landscape, including the Cold War, Operation Rolling Thunder and protests at home.')
print(str(i.model.model))
a = Event()
a.loadEvent('On the Line: Intrepid and the Vietnam War')
print(a.compareTo(b))
a.deleteEvent()
a.saveEvent()
a = User().loadUser(email='test@baruchmail.cuny.edu')
b = a.getBestEvent()
print(b.name)