import os
import json
import smtplib
import colorama
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from getpass import getpass


class User:

    def __init__(self, conn, email, password):
        self.conn = conn
        self.email = email
        self.password = password

    def select_messenger_client(self, user_email, user_data):
        selection_data = {}
        for index, contact in enumerate(user_data['contacts'], start=1):
            selection_data[index] = (contact['name'], contact['email'])
            print(f"{index} - {contact['name']}")

        try:
            user_selection = int(input('Select Client Index: '))
            if user_selection in selection_data:
                message = []
                try:
                    while True:
                        prompt_message = str(input(f'Message To {selection_data[user_selection][0]}: '))
                        if prompt_message == "cancel" or prompt_message == "quit":
                            quit()
                        else:
                            message.append(prompt_message)
                except KeyboardInterrupt:
                    User(self.conn, self.email, self.password).send_mails(
                            user_email, selection_data[user_selection][0], selection_data[user_selection][1], '\n'.join(message))
        except KeyboardInterrupt:
            print('\n\nStopped!')

    def send_mails(self, sender_email, client_name, client_email, sender_message):
        try:
            message = f"Subject: Hello, {client_name}\n{sender_message}"
            if self.conn.sendmail(sender_email, client_email, message) == {}:
                print(colorama.Fore.GREEN,
                    f'\n[*] Successfully sent mail to: {client_name}', colorama.Style.RESET_ALL)
        except smtplib.SMTPException as send_err:
            print(colorama.Fore.RED,
                f'\n[!!] Failed to send mail to: {client_email} {send_err}', colorama.Style.RESET_ALL)

class Connection:

    def __init__(self, login_email, login_password):
        self.login_email = login_email
        self.login_password = login_password

    def server_connection(self):
        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            return self.server
        except smtplib.SMTPException as err:
            print(colorama.Fore.RED,
                    f'[!!] Something I dont know has failed! {err}',
                    colorama.Style.RESET_ALL)

    def gmail_login(self, connection):
        try:
            if connection.login(self.login_email, self.login_password):
                print(colorama.Fore.GREEN,
                    '[*] You have successfully logged in to your gmail SMTP',
                    colorama.Style.RESET_ALL)
                return connection
        except smtplib.SMTPAuthenticationError as autherr:
            print(colorama.Fore.RED,
                f'[!!] Authentication Error! {autherr}', colorama.Style.RESET_ALL)
            quit()


class JSON_Data:

    def read_json(self, filename='contacts.json'):
        with open(filename, 'r', encoding='utf-8') as j_source:
            source = json.load(j_source)
        return source

    def write_json(self, data, filename='contacts.json'):
        with open(filename, 'w', encoding='utf-8') as f_source:
            json.dump(data, f_source, indent=2)


def login():
    source = JSON_Data().read_json()
    if source['user_email'] == "":
        my_email = str(input('Enter Email: '))
        source['user_email'] = my_email
        JSON_Data().write_json(source)
    else:
        my_email = source['user_email']

    my_pass = getpass('Enter Password: ')
    connection = Connection(my_email, my_pass)
    my_user = User(connection.gmail_login(connection.server_connection()), my_email, my_pass)

    if not source['contacts'] == []:
        my_user.select_messenger_client(my_email, source)
    else:
        print(colorama.Fore.RED,
            '[!!] No contacts', colorama.Style.RESET_ALL)

    if connection.server_connection().close() == None:
        print(colorama.Fore.GREEN,
            '\n[*] Server has been successfully closed\n', colorama.Style.RESET_ALL)


class User_Info:

    def current_email(self):
        source = JSON_Data().read_json()
        print(colorama.Fore.YELLOW,
                f"[!] Current User/Sender Email: ",
                colorama.Style.RESET_ALL, source['user_email'])

    def change_email(self, new_email):
        source = JSON_Data().read_json()
        for email in new_email:
            if not email.endswith('@gmail.com'):
                print(colorama.Fore.RED,
                        f"[!!] {email} is not a valid google email address",
                        colorama.Style.RESET_ALL)
            else:
                if source['user_email'] == email:
                    print(colorama.Fore.YELLOW,
                            f"[!] {email} is already the current User/Sender Email being used",
                            colorama.Style.RESET_ALL)
                else:
                    source['user_email'] = email
                    JSON_Data().write_json(source)
                    print(colorama.Fore.GREEN,
                            f"[*] User/Sender Email has been changed to {source['user_email']}",
                            colorama.Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description='Write mails to whoever you want.')

    parser.add_argument('--change-email',
                        nargs=1, type=str,
                        metavar='CHANGE_EMAIL',
                        help='Change user/sender email')

    parser.add_argument('--current-email',
                        action='store_true',
                        help='Views current User/Sender Email')

    args = parser.parse_args()
    if args.change_email:
        User_Info().change_email([x for x in args.change_email])
    elif args.current_email:
        User_Info().current_email()
    else:
        if not os.path.exists('contacts.json'):
            print(colorama.Fore.RED,
                f'[!!] Could not perform operation if there is not a contact list',
                colorama.Style.RESET_ALL)
        else:
            login()
