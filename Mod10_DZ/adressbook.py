from collections import UserDict


class AdressBook(UserDict):

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            self.data[record.name.value].add_phones(record.phones)

class Record:
    def __init__(self, phones = None):
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

class Name:
    def __init__(self, name):
        self.name = name

class Field:
    pass

class Phone:
        def __init__(self, phone = None):
            if phone:
                self.phone = phone