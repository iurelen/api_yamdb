import secrets
import string


def code_generator(code='', code_length=6):
    for i in range(code_length):
        code += ''.join(secrets.choice(string.digits))
    return code
