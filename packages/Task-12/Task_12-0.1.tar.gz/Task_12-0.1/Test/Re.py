import re

regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

email = input('Enter email:')

if not re.fullmatch(regex_email, email):
    print("Invalid email")
    correct_credential = False
else:
    correct_credential = True
    print("Correct email")