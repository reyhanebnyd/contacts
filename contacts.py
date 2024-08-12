import re
import csv
import pandas as pd


class Contact:
    def __init__(self, name, number, email):
        self.name = name
        self.number = number
        self.email = email

    def __str__(self):
        return 'Name: {}\nPhoneNumber: {}\nemail: {}'.format(self.name, self.number, self.email)


class ContactManager:
    def __init__(self):
        self.Allcontacts = []
        self.myfile = 'contact.csv'
        self.load_contact()

    def load_contact(self):
        try:
            with open(self.myfile, 'r') as file:
                first_line = file.readline().strip()
                if not first_line:
                    print('hello')
                    with open(self.myfile, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['name', 'number', 'email'])
                else:
                    with open(self.myfile, mode='r', newline='') as file:
                        reader = csv.reader(file)
                        next(reader)
                        for row in reader:
                            if row:  # Avoid empty rows
                                self.Allcontacts.append(Contact(row[0], row[1], row[2]))
        except FileNotFoundError:
            pass

    def save_contact(self, contact: Contact):
        with open(self.myfile, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([contact.name, contact.number, contact.email])

    def add_contact(self, name, number, email):
        find = self.check_existence(name)
        if not find:
            if not re.match(r'^[a-zA-Z0-9\.\_]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$', email):
                print('Invalid email address')
                return
            if not re.match(r'^(09\d{9}|\+989\d{9}|00989\d{9})$', number):
                print('Invalid phone number')
                return
            self.Allcontacts.append(Contact(name, number, email))
            self.save_contact(Contact(name, number, email))
            print("contact added successfully")
        else:
            print('The contact already exists.')

    def delete_contact(self, name):
        find = self.check_existence(name)
        if find:
            for contact in self.Allcontacts:
                if contact.name == name:
                    s = contact
            df = pd.read_csv('contact.csv')
            value_to_delete = name
            df = df[df['name'] != value_to_delete]
            df.to_csv('contact.csv', index=False)
            self.Allcontacts.remove(s)
        else:
            print('The contact does not exist')

    def edit_contact(self, old_name, new_name, new_phone, new_email):
        find = self.check_existence(old_name)
        if find:
            self.delete_contact(old_name)
            self.add_contact(new_name, new_phone, new_email)
            print('contact got edited.')
        else:
            print('The contact does not exist')

    def display_contact(self):
        for index, contact in enumerate(self.Allcontacts):
            print(index+1)
            print(contact)
            print('---------------------------------')

    def sort_contacts(self):
        self.Allcontacts.sort(key=lambda c: c.name)
        self.display_contact()

    def check_existence(self, name):
        find = False
        for contact in self.Allcontacts:
            if contact.name == name:
                find = True
        return find


def main():
    manager = ContactManager()

    while True:
        print("\n1. Add Contact")
        print("2. Edit Contact")
        print("3. Delete Contact")
        print("4. Display Contacts")
        print("5. Sort Contacts")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            email = input("Enter email: ")
            manager.add_contact(name, phone, email)
        elif choice == '2':
            old_name = input("Enter name of contact to edit: ")
            find = manager.check_existence(old_name)
            if not find:
                print('the contact does not exist')
            else:
                new_name = input("Enter new name: ")
                new_phone = input("Enter new phone: ")
                new_email = input("Enter new email: ")
                manager.edit_contact(old_name, new_name, new_phone, new_email)
        elif choice == '3':
            name = input("Enter name of contact to delete: ")
            manager.delete_contact(name)
        elif choice == '4':
            manager.display_contact()
        elif choice == '5':
            print("Contacts sorted by name:")
            manager.sort_contacts()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


