'''
This is used to generate a password containing strings and numbers

'''

import random
import string


def password_generator(number_of_characters):
    '''
    Generates a password containing characters and numbers

    parameter(number_of_characters):
    To specify the number of charactes needed to generate the password

    Retruns:
    The password as a string

    '''

    password = ("".join(random.choices(
        string.ascii_letters + string.digits, k=number_of_characters)))
    return password
