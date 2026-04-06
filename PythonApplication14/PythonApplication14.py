import os
import hashlib
from cryptography.fernet import Fernet

ENV_PATH = ".env"

def get_secret_key():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            content = f.read()
            for line in content.splitlines():
                if "GAME_DATA_KEY" in line:
                    return line.split("=")[1].strip().encode()

    key = Fernet.generate_key()
    mode = "a" if os.path.exists(ENV_PATH) else "w"
    with open(ENV_PATH, mode) as f:
        f.write(f"\nGAME_DATA_KEY={key.decode()}\n")
    
    print(f">> Created new key in {ENV_PATH}. Check your .gitignore!")
    return key

class Crypto:
    def __init__(self, key):
        self.f = Fernet(key)

    @staticmethod
    def quick_hash(text: str):
        return hashlib.sha256(text.encode()).hexdigest()

    def pack(self, data: str):
        return self.f.encrypt(data.encode())

    def unpack(self, token: bytes):
        return self.f.decrypt(token).decode()

if __name__ == "__main__":
    crypt = Crypto(get_secret_key())
    
    pwd = "player_secret_123"
    print(f"Hash: {crypt.quick_hash(pwd)}")

    payload = '{"id": 42, "items": ["sword", "shield"]}'
    token = crypt.pack(payload)
    
    print(f"Encrypted: {token[:30]}...") 
    print(f"Decrypted: {crypt.unpack(token)}")
