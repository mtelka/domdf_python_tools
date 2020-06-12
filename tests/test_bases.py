"""
test_bases
~~~~~~~~~~~~~~~

Test functions in bases.py

"""

# stdlib
import copy
import pickle
from collections import UserList

# 3rd party
import pytest  # type: ignore

# this package
from domdf_python_tools.bases import Dictable, namedlist
from domdf_python_tools.utils import printr, printt


class Person(Dictable):

	def __init__(self, name, age, occupation=None):
		super().__init__()

		self.name = str(name)
		self.age = int(age)
		self.occupation = occupation

	@property
	def __dict__(self):
		return dict(
				name=self.name,
				age=self.age,
				occupation=self.occupation,
				)


class Child(Person):

	def __init__(self, name, age, school):
		super().__init__(name, age, "Student")

		self.school = "school"

	@property
	def __dict__(self):
		class_dict = super().__dict__
		class_dict["School"] = self.school
		return class_dict


@pytest.fixture(scope="function")
def alice():
	return Person("Alice", 20, "IRC Lurker")


class TestDictable:

	def test_creation(self, alice):
		assert alice.name == "Alice"
		assert alice.age == 20
		assert alice.occupation == "IRC Lurker"

	def test_str(self, alice):
		assert str(alice).startswith("<tests.test_bases.Person")

	def test_equality(self):
		dolly = Person("Dolly", 6, "Sheep")
		clone = Person("Dolly", 6, "Sheep")

		assert dolly == clone

	def test_iter(self, alice):
		for key, value in alice:
			assert key == "name"
			assert value == "Alice"
			return

	def test_copy(self, alice):
		assert copy.copy(alice) == alice
		assert copy.deepcopy(alice) == alice
		assert copy.copy(alice) == copy.copy(alice)

	def test_pickle(self, alice):
		assert pickle.loads(pickle.dumps(alice)) == alice

	def test_vars(self, alice):
		assert vars(alice) == dict(alice)

	def test_subclass(self):
		person = Person("Bob", 12, "Student")
		child = Child("Bob", 12, "Big School")
		assert person == child
		assert "School" not in person.__dict__


def test_namedlist(capsys):
	mylist = namedlist()
	assert isinstance(mylist(), UserList)

	ShoppingList = namedlist("ShoppingList")
	shopping_list = ShoppingList(["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"])
	assert isinstance(shopping_list, UserList)
	assert shopping_list[0] == "egg and bacon"

	printt(shopping_list)
	printr(shopping_list)
	print(shopping_list)

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == "<class 'domdf_python_tools.bases.namedlist.<locals>.NamedList'>"
	assert stdout[1] == "['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
	assert stdout[2] == (
			"ShoppingList['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
			)
