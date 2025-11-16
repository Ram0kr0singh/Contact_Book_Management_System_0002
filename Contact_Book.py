import csv
import json
from datetime import datetime

CSV_FILE = "contacts.csv"
JSON_FILE = "contacts.json"
LOG_FILE = "error_log.txt"


def log_error(message, operation):
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {operation}: {message}\n")


def add_contact():
    try:
        name = input("Enter Name: ").strip()
        phone = input("Enter Phone Number: ").strip()
        email = input("Enter Email Address: ").strip()

        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, phone, email])

        print("Contact added successfully.\n")

    except Exception as e:
        log_error(str(e), "Add Contact")
        print("Error while adding contact.")


def display_contacts():
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            contacts = list(reader)

        if not contacts:
            print("No contacts found.\n")
            return

        print("\nName\t\tPhone\t\tEmail")
        print("-" * 50)

        for row in contacts:
            if len(row) == 3:
                name, phone, email = row
                print(f"{name}\t\t{phone}\t\t{email}")

        print()

    except FileNotFoundError:
        log_error("CSV file not found.", "Display Contacts")
        print("No contacts have been saved yet.\n")


def search_contact():
    name_to_search = input("Enter name to search: ").strip()

    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) == 3:
                    name, phone, email = row
                    if name.lower() == name_to_search.lower():
                        print(f"\nFound Contact:\nName: {name}\nPhone: {phone}\nEmail: {email}\n")
                        return

        print("Contact not found.\n")

    except Exception as e:
        log_error(str(e), "Search Contact")
        print("Error searching contact.\n")


def update_contact():
    name_to_update = input("Enter name to update: ").strip()

    try:
        updated = False
        contacts = []

        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                contacts.append(row)

        for contact in contacts:
            if len(contact) == 3 and contact[0].lower() == name_to_update.lower():
                print("What do you want to update?")
                print("1. Phone")
                print("2. Email")
                choice = input("Enter choice: ")

                if choice == "1":
                    contact[1] = input("Enter new phone: ").strip()
                elif choice == "2":
                    contact[2] = input("Enter new email: ").strip()

                updated = True

        if updated:
            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(contacts)
            print("Contact updated successfully.\n")
        else:
            print("Contact not found.\n")

    except Exception as e:
        log_error(str(e), "Update Contact")
        print("Error updating contact.\n")


def delete_contact():
    name_to_delete = input("Enter name to delete: ").strip()

    try:
        contacts = []
        deleted = False

        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) == 3 and row[0].lower() != name_to_delete.lower():
                    contacts.append(row)
                else:
                    if len(row) == 3:
                        deleted = True

        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(contacts)

        if deleted:
            print("Contact deleted successfully.\n")
        else:
            print("Contact not found.\n")

    except Exception as e:
        log_error(str(e), "Delete Contact")
        print("Error deleting contact.\n")


def export_to_json():
    try:
        contacts = []

        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    name, phone, email = row
                    contacts.append({"name": name, "phone": phone, "email": email})

        with open(JSON_FILE, "w") as file:
            json.dump(contacts, file, indent=4)

        print("Contacts exported to JSON successfully.\n")

    except Exception as e:
        log_error(str(e), "Export JSON")
        print("Error exporting to JSON.\n")


def load_from_json():
    try:
        with open(JSON_FILE, "r") as file:
            contacts = json.load(file)

        print("\nContacts from JSON:")
        print("-" * 50)
        for c in contacts:
            print(f"{c['name']}\t{c['phone']}\t{c['email']}")
        print()

    except Exception as e:
        log_error(str(e), "Load JSON")
        print("Error loading JSON.\n")


print("Welcome to the Contact Book Manager!")

while True:
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Export to JSON")
    print("7. Load from JSON")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        display_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        update_contact()
    elif choice == "5":
        delete_contact()
    elif choice == "6":
        export_to_json()
    elif choice == "7":
        load_from_json()
    elif choice == "8":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Try again.\n")
