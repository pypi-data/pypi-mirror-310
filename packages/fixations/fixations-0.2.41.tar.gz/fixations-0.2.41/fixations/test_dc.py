from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Person:
    name: str


person = Person(name='lidatong')
print(person.to_json())  # '{"name": "lidatong"}' <- this is a string
print(person.to_dict())  # {'name': 'lidatong'} <- this is a dict
Person.from_json('{"name": "lidatong"}')  # Person(1)
Person.from_dict({'name': 'lidatong'})  # Person(1)

# You can also apply _schema validation_ using an alternative API
# This can be useful for "typed" Python code

Person.from_json('{"name": 42}')  # This is ok. 42 is not a `str`, but
                                  # dataclass creation does not validate types
Person.schema().loads('{"name": 42}')  # Error! Raises `ValidationError`
