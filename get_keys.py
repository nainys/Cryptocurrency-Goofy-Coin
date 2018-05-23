import ecdsa
from binascii import unhexlify,hexlify
import os
import User

class Keys:
    @classmethod
    def load_key(cls, name, key_type):
        if key_type == 'public_key':
            ecdsa_key = ecdsa.VerifyingKey
            extension = ".pk"
        elif key_type =='secret_key':
            ecdsa_key = ecdsa.SigningKey
            extension = ".sk"
        else:
            raise ValueError('Third argument key_type needs to be either public_key or secret_key.')
        path = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(path+"/keys", name + extension )
        with open(key_path, 'rb') as temp_file:
            hex_key = temp_file.read().split('\n')
            bytes_key = unhexlify(hex_key[0])
            key = ecdsa_key.from_string(bytes_key, ecdsa.SECP256k1)

        return key

    @classmethod
    def load_public_key(cls, name):
        return cls.load_key(name, 'public_key')
        print("Public key loaded.")

    @classmethod
    def load_secret_key(cls, name):
        return cls.load_key(name, 'secret_key')
        print("Secret key loaded.")
