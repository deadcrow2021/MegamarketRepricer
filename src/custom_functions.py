from cryptography.fernet import Fernet

from src.constants import keys


def get_shop_name(filename: str) -> str:
    shop = filename.split('.')[0]
    shop = shop.replace('_', ' ')
    shop = shop.title()
    return shop


def encrypt_data(data: str) -> str:
    f = Fernet(keys['encryption_key'].encode())
    encr = f.encrypt(data.encode())
    return encr.decode()


def decrypt_data(data: str) -> str:
    f = Fernet(keys['encryption_key'].encode())
    decr = f.decrypt(data.encode())
    return decr.decode()
