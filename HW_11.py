from collections import UserDict
from datetime import datetime, timedelta, date
from itertools import islice


class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
    
    
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return super().__str__()


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    def __str__(self):
        return super().__str__()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, phone):
        if phone.isdigit():
            self._value = phone
        else:
            raise ValueError("Phone number must contains only digits.")


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        return super().__str__() if self.value else ''

    @property
    def value(self):
        return self._value
    
    @value.setter
    def  value(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Incorrect date format, should be dd.mm.yyyy")
        self._value = value


class Record:
    def __init__(self, name:Name, phone:Phone=None, birthday:Birthday=None) -> None:
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday if birthday is not None else Birthday(None)

    def __str__(self):
        return str(self.phones)
    
    def __repr__(self):
        return str(self.phones)
    
    def add_number(self, phone:Phone):
        self.phones.append(phone)
    
    def del_phone(self, phone):
        
        for i, p in enumerate(self.phones):
            if p.value == phone.value:
                return self.phones.pop(i)
    
    def change_phone(self, old_phone, new_phone):
        
        del_phone = self.del_phone(old_phone)
        if del_phone:
            self.add_number(new_phone)
            return True
        return False
    
    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            raise ValueError('Not correct birthday')
        
    def days_to_birthday(self):
        if not self.birthday.value:
            return None
        
        today = datetime.now()
        bday = datetime.strptime(self.birthday.value, "%d.%m.%Y")

        if bday < today:
            bday = bday.replace(year = today.year + 1)
            delta = bday - today
        elif bday > today:
            bday = bday.replace(year= today.year)
            delta = today - bday
        
        return delta.days
    

    
class Addressbook(UserDict):
    def add_record(self, rec:Record):
        self.data[rec.name.value] = rec

    def iterator(self, page=None):
        while True:
            if self.start_iterate >= len(self.data):
                break
            yield list(islice(self.data.items(), self.start_iterate, self.start_iterate + page))
            self.start_iterate += page
            start += page


contacts = Addressbook()


def input_errors(func):
    def inner(*args):
        try:
            return func(*args)
        except (KeyError, IndexError, ValueError):
            return "Not enough arguments."
    return inner


@input_errors
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[-1])
    rec = contacts.get(name.value)
    if rec:
        rec.add_number(phone)
        return f'phone number {phone} added successfully to contact {name}'
    rec = Record(name, phone, birthday)
    contacts.add_record(rec)
    return f'contact {name} with phone number {phone} and {birthday} added successfully'


@input_errors
def change_phone_number(*args):
    name = Name(args[0])
    
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    if contacts.get(name.value):
        # contacts[name] = new_phone
        contacts[name.value].change_phone(old_phone, new_phone)
        return f"Phone number for contact {name} changed"
    return f"No contact with name {name}"


@input_errors
def print_phone_number(*args):
    name = Name(args[0])
                              
    rec = contacts.get(name.value)
    if rec:
        return rec.phones
    return f"No contact with name {name}"


def show_all(*args, contacts=contacts, page=None):
    contact_list = []
    for name, rec in contacts.data.items():
        phones = ", ".join(str(phone) for phone in rec.phones)
        days_to_birthday = rec.days_to_birthday()
        contact_list.append(f"{name} {phones} days to birthday:{days_to_birthday}")

    if not contacts.data:
        return 'No contacts'

    if page==None:
        return "\n".join(contact_list)
    else:
        for records in contacts.iterator(contacts.data, int(page)):
            print('\n'.join([str(record) for record in records]))
    


def hello(*args):
    return "How can I help you?"


def good_bye(*args):
    return 'Good bye!'


def no_command(*args):
    return "Unknown command, try again"


COMMANDS = {'hello': hello,
            'add': add,
            'good bye': good_bye,
            'exit': good_bye,
            'close': good_bye,
            'show all': show_all,
            'change': change_phone_number,
            'phone': print_phone_number,
           
}


def command_handler(text):
    for kword, command in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip().split()
    return no_command, None


def main():
    print(hello())
    while True:
        user_input = (input(">>>")) 
        command, data = command_handler(user_input)
        print(command(*data))
        if command == good_bye:
            break
            

if __name__ == '__main__':
    main()