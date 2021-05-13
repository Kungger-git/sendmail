import json
import os
import colorama
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class Manage_Users:

    def __init__(self, credentials):
        self.name = credentials[0]
        self.email = credentials[1]

    def add_user(self):
        source = JSON_Data().read_json()
        user_data = {
                'name': self.name,
                'email': self.email
        }
        temp = source['contacts']
        if user_data in temp:
            print(colorama.Fore.RED,
                f'[!!] {self.name}/{self.email} already exists.',
                colorama.Style.RESET_ALL)
        else:
            temp.append(user_data)
            JSON_Data().write_json(source)

            if user_data in source['contacts']:
                print(colorama.Fore.GREEN,
                    f'[*] {self.name}/{self.email} has been added to your contacts list',
                    colorama.Style.RESET_ALL)

    def remove_user(self):
        source = JSON_Data().read_json()

        rm_data = {
                'name': self.name,
                'email': self.email
        }
        temp = source['contacts']
        if not rm_data in temp:
            print(colorama.Fore.RED,
                f'[!!] {self.name}/{self.email} does not exist', colorama.Style.RESET_ALL)
        else:
            for i in range(len(temp)):
                if temp[i]['name'] == self.name and temp[i]['email'] == self.email:
                    del temp[i]
                    break
            if not rm_data in temp:
                print(colorama.Fore.GREEN,
                    f'[*] {self.name}/{self.email} has been removed from your contacts list',
                    colorama.Style.RESET_ALL)
        JSON_Data().write_json(source)

    def change_name(self):
        source = JSON_Data().read_json()
        old_name = ""
        for contact in source['contacts']:
            if self.email == contact['email']:
                old_name = contact['name']
                contact['name'] = self.name
                JSON_Data().write_json(source)
                print(colorama.Fore.GREEN,
                        f"[*] Name for {contact['email']} has been changed from {old_name} to {self.name}",
                        colorama.Style.RESET_ALL)


def list_contacts():
    source = JSON_Data().read_json()
    for user in source['contacts']:
        print(f"Name: {user['name']}\tEmail: {user['email']}")


class JSON_Data:

    def read_json(self, filename='contacts.json'):
        with open(filename, 'r', encoding='utf-8') as j_source:
            source = json.load(j_source)
        return source

    def write_json(self, data, filename='contacts.json'):
        with open(filename, 'w', encoding='utf-8') as f_source:
            json.dump(data, f_source, indent=2)

    def make_json(self):
        data_set = {'user_email': ''}
        data_set['contacts'] = []

        JSON_Data().write_json(data_set)


if __name__ == '__main__':
    colorama.init()
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description='Adds/Removes Contacts from contacts.json')

    parser.add_argument('-a', '--add',
                        nargs=2, metavar='ADD',
                        action='store',
                        help="Adds a contact. (e.g. -a Bobby bobby54@bobbysite.com)")

    parser.add_argument('-rm', '--remove',
                        nargs=2, metavar='REMOVE',
                        action='store',
                        help="Removes a contact. (e.g. -rm Bobby boby54@bobbysite.com)")

    parser.add_argument('-ls', '--list',
                        action='store_true',
                        help='Lists all contacts.')

    parser.add_argument('--change-name',
                        nargs=2, metavar='CHANGE_NAME',
                        action='store',
                        help='Change contact name')

    args = parser.parse_args()
    if not os.path.exists('contacts.json'):
        JSON_Data().make_json()

    if args.add:
        Manage_Users([x for x in args.add]).add_user()

    if args.remove:
        Manage_Users([x for x in args.remove]).remove_user()

    if args.list:
       list_contacts()

    if args.change_name:
        Manage_Users([x for x in args.change_name]).change_name()
