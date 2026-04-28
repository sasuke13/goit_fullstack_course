class PersonAddress:
    def __init__(self, zip, city, street):
        self.zip = zip
        self.city = city
        self.street = street

    def get_address(self):
        return f'{self.zip}, {self.city}, {self.street}'


class Person:
    def __init__(self, name, address: PersonAddress):
        self.name = name
        self.address = address


person = Person('Olexander', '36007', 'Poltava', 'European, 28')
print(person.get_address())
