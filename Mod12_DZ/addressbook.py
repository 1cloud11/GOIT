from collections import UserDict
from datetime import datetime
import re


class AddressBook(UserDict):

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            self.data[record.name.value].add_phones(record.phones)

    def edit_record(self, old_record, new_record):
        if old_record.name.value not in self.data:
            return
        self.data[old_record.name.value].update_phone(
            old_record.phones[0], new_record.phones[0]
        )

    def delete(self, record):
        if record.name.value in self.data:
            self.data.pop(record.name.value)

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

    def __str__(self):
        return "\n".join([
            str(record) for record in self.data.values()
        ])


class Record:
    def __init__(self, name, phones = None, birthday=None):
        self.name = name
        self.birthday = birthday
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

    def __repr__(self):
        result = f"{str(self.name)}\n{20 * '='}"
        for idx, phone in enumerate(self.phones, start=1):
            result += f"\n{idx} {phone}"
        return result


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
    pass


class Phone(Field):
    def __init__(self, phone = None):
        super().__init__(phone)
        if phone:
            self.phone = phone

    @Field.value.setter
    def value(self, phone: str):
        value = phone.replace(" ", "")
        if re.match(r'\d{11}', value):
            self.__value = value
        else:
            self.__value = None
            return f"No phone number found in {phone}"
    
    def __repr__(self):
        return self.phone


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        self.__value = datetime.strptime(value, '%d%m%Y').date()