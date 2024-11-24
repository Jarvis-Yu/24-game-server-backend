from base64 import urlsafe_b64encode, urlsafe_b64decode
from typing import Callable


__all__ = ["get_encryptor_decryptor"]


def get_encryptor_decryptor() -> tuple[Callable[[str], str], Callable[[str], str]]:
    def encrypt(data: str) -> str:
        return urlsafe_b64encode(data.encode("utf-8")).decode("ascii")

    def decrypt(data: str) -> str:
        return urlsafe_b64decode(data.encode("ascii")).decode("utf-8")

    return encrypt, decrypt


if __name__ == "__main__":
    key = "key"

    encrypt, decrypt = get_encryptor_decryptor(key)
    data = "Hello, World!"
    encrypted = encrypt(data)
    decrypted = decrypt(encrypted)
    print(f"Data: {data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
