import os

from base64 import urlsafe_b64encode  # , urlsafe_b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from dkdc_env import Env

env = Env()

SCRYPT_N = 1 << 15  # CPU/memory cost
SCRYPT_R = 1 << 4  # block size
SCRYPT_P = 1 << 1  # parallelization factor
KEY_LENGTH = 1 << 6  # length of the derived key

SALT_SIZE = KEY_LENGTH
PEPPER_SIZE = KEY_LENGTH
CAYENNE = ("dkdc" * (1 << 3)).encode()


def generate_salt() -> bytes:
    return os.urandom(SALT_SIZE)


def generate_pepper() -> bytes:
    return os.urandom(PEPPER_SIZE)


def get_cayenne() -> bytes:
    cayenne = env.get("CAYENNE")
    return cayenne.encode() if cayenne else CAYENNE


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(A ^ B for A, B in zip(a, b))


def hash_passphrase(
    passphrase: str, salt: bytes = None, pepper: bytes = None
) -> (str, bytes, bytes):
    assert isinstance(passphrase, str)

    salt = salt or generate_salt()
    pepper = pepper or generate_pepper()
    cayenne = get_cayenne()

    pp = passphrase.encode() + xor(salt, pepper) + cayenne

    kdf = Scrypt(
        salt=salt,
        length=KEY_LENGTH,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=default_backend(),
    )
    key = kdf.derive(pp)
    pp_hash = urlsafe_b64encode(key).decode()
    return (pp_hash, salt, pepper)


def verify_passphrase(
    passphrase: str,
    stored_hash: str,
    salt: bytes = None,
    pepper: bytes = None,
) -> bool:
    try:
        new_hash, *_ = hash_passphrase(passphrase, salt=salt, pepper=pepper)
        return new_hash == stored_hash

    except Exception as e:
        print(f"Error: {e}")
        return False
