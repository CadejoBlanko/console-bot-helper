from collections import UserDict
from datetime import date, datetime
import pickle

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self._validate_phone()

    def _validate_phone(self):
        if not self._value.isdigit():
            raise ValueError("Phone number should only contain digits.")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self._validate_birthday()

    def _validate_birthday(self):
        try:
            datetime.strptime(self._value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Please use the format 'DD-MM-YYYY'.")


class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phones(self):
        self.phones.clear()

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            next_birthday = date(today.year, int(self.birthday.value[3:5]), int(self.birthday.value[0:2]))
            if next_birthday < today:
                next_birthday = date(today.year + 1, int(self.birthday.value[3:5]), int(self.birthday.value[0:2]))
            days_left = (next_birthday - today).days
            return days_left
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return iter(self.data.values())


def normalization_text(user_text):
    lower_user_text = user_text.lower()
    return lower_user_text


def input_error(user_text, normalization_user_text):
    user_text_split = user_text.split(" ")
    normalization_user_text_split = normalization_user_text.split(" ")
    tuple_cmd = ("hello", "add", "change", "phone", "show all", "search", "exit", "good bye", "close")

    if not normalization_user_text.startswith(tuple_cmd):
        print(f"Wrong command {normalization_user_text_split[0]}. Please try again.")
        return False

    if normalization_user_text.startswith(("add", "change")):
        if not len(user_text_split) >= 3:
            print("Give me name and phone please")
            return False
        elif not user_text_split[1].isalpha() and not user_text_split[2].isdigit() and not user_text_split[2].startswith("+"):
            print("Give me name and phone please")
            return False
        elif not user_text_split[1].isalpha():
            print("Enter user name")
            return False
        elif user_text_split[2].startswith("+"):
            if not user_text_split[2][1:].isdigit():
                print("Enter phone")
                return False
        elif not user_text_split[2].isdigit():
            print("Enter phone")
            return False

    if normalization_user_text.startswith("phone"):
        if not user_text_split[1].isalpha():
            print("Enter user name")
            return False
    return True


def cmd_hello():
    print("How can I help you?")


address_book = AddressBook()


def save_address_book(filename):
    with open(filename, 'wb') as file:
        pickle.dump(address_book, file)


def load_address_book(filename):
    global address_book
    try:
        with open(filename, 'rb') as file:
            address_book = pickle.load(file)
    except FileNotFoundError:
        address_book = AddressBook()


def cmd_search(text):
    search_query = text.split(" ", 1)[1].lower()
    found_contacts = []
    for record in address_book:
        if search_query in record.name.value.lower() or any(search_query in phone.value.lower() for phone in record.phones):
            found_contacts.append(record)
    
    if found_contacts:
        for record in found_contacts:
            print(f"{record.name.value}:")
            if record.phones:
                for phone in record.phones:
                    print(phone.value)
            else:
                print("No phone numbers found for this contact.")
            if record.birthday:
                days_left = record.days_to_birthday()
                if days_left is not None:
                    print(f"Days left until birthday: {days_left}")
    else:
        print("No contacts found matching the search query.")


def cmd_add(text):
    text_split = text.split(" ")
    name = Name(text_split[1])
    phone = Phone(text_split[2])
    birthday = Birthday(text_split[3]) if len(text_split) > 3 else None

    if name.value not in address_book:
        record = Record(name, birthday)
        record.add_phone(phone)
        address_book.add_record(record)
        print("Contact added successfully.")
    else:
        print("Contact already exists.")


def cmd_change(text):
    text_split = text.split(" ")
    name = Name(text_split[1])
    phone = Phone(text_split[2])

    if name.value in address_book:
        record = address_book[name.value]
        record.remove_phones()
        record.add_phone(phone)
        print("Contact updated successfully.")
    else:
        print("Contact not found.")


def cmd_phone(text):
    text_split = text.split(" ")
    name = Name(text_split[1])

    if name.value in address_book:
        record = address_book[name.value]
        if record.phones:
            for phone in record.phones:
                print(phone.value)
        else:
            print("No phone numbers found for this contact.")
    else:
        print("Contact not found.")


def cmd_show_all():
    if address_book:
        for record in address_book:
            print(f"{record.name.value}:")
            if record.phones:
                for phone in record.phones:
                    print(phone.value)
            else:
                print("No phone numbers found for this contact.")
            if record.birthday:
                days_left = record.days_to_birthday()
                if days_left is not None:
                    print(f"Days left until birthday: {days_left}")
    else:
        print("Address book is empty.")


def main():
    
    load_address_book("address_book.pickle")

    work = True
    while work:
        user_text = input()
        normalization_user_text = normalization_text(user_text)
        if input_error(user_text, normalization_user_text):
            if normalization_user_text.startswith("hello"):
                cmd_hello()
            elif normalization_user_text.startswith("add"):
                cmd_add(user_text)
            elif normalization_user_text.startswith("change"):
                cmd_change(user_text)
            elif normalization_user_text.startswith("phone"):
                cmd_phone(user_text)
            elif normalization_user_text.startswith("show all"):
                cmd_show_all()
            elif normalization_user_text.startswith("search"):
                cmd_search(user_text)
            elif normalization_user_text.startswith("exit"):
                work = False

    save_address_book("address_book.pickle")


if __name__ == "__main__":
    main()
