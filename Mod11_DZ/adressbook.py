from collections import UserDict
from datetime import datetime
import re


class AdressBook(UserDict):

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            self.data[record.name.value].add_phones(record.phones)

    def iterator(self, item_number):
        counter = 0
        result = ""
        for name, record in self.data.items():
            result += str(record) + "\n"
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ""
        yield result


class Record:
    def __init__(self, phones = None, birthday=None):
        self.name = Name.name
        if phones is None:
            self.phones = []
        else:
            self.phones = phones

    def add_phone(self, phone_number):
        self.phones.append(phone_number)
    
    def delete_phone(self, phone_number):
        self.phones.remove(phone_number)

    def edit_phone(self, phone_number, new_phone):
        idx = self.phones.index(phone_number)
        self.phones[idx] = new_phone

    def days_to_birthday(self):
        if not self.birthday:
            return
        now = datetime.today()
        if (self.birthday.value.replace(year=now.year) - now).days > 0:
            return (self.birthday.value.replace(year=now.year) - now).days
        return (self.birthday.value.replace(year=now.year+1) - now).days


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return f"{self.__class__.__name__}: {self.value}"


class Name(Field):
    def __init__(self, name):
        self.name = name


class Phone(Field):
    def __init__(self, phone = None):
        if phone:
            self.phone = phone
    
    def __repr__(self):
        return self.value

    @Field.value.setter
    def value(self, phone: str):
        value = phone.replace(" ", "")
        if re.match(r'\d{11}', value):
            self.__value = value
        else:
            self.__value = None
            return f"No phone number found in {phone}"


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        self.__value = datetime.strptime(value, '%d%m%Y').date()