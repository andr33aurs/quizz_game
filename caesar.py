# abc -> def cheie de 3
import time


def encrypt(text, key=3) -> str:
    '''This function has the role to encrypt a text using caesar code'''
    encrypted_text = ''
    for char in text:
        encrypted_text += chr(ord(char) + key)
    return encrypted_text


def decrypt(encrypted_text, key=3) -> str:
    '''This function has the role to decrypt using caesar code'''
    text = ''
    for char in encrypted_text:
        text += chr(ord(char) - key)
    return text


