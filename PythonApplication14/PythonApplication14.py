import os
import hashlib
from cryptography.fernet import Fernet

CONFIG_FILE = ".env"

def load_or_create_key():
    """Загружает ключ из файла или создает новый, если файла нет."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                if line.startswith("GAME_DATA_KEY="):
                    return line.strip().split("=")[1].encode()
    
    new_key = Fernet.generate_key()
    with open(CONFIG_FILE, "a") as f:
        f.write(f"\nGAME_DATA_KEY={new_key.decode()}\n")
    print(f"[INFO] Создан новый ключ в {CONFIG_FILE}. Добавьте этот файл в .gitignore!")
    return new_key

class GameSecurity:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля через SHA-256 (необратимо)."""
        return hashlib.sha256(password.encode()).hexdigest()

    def encrypt_traffic(self, data: str) -> bytes:
        """Шифрование данных перед отправкой в сеть."""
        return self.cipher.encrypt(data.encode())

    def decrypt_traffic(self, encrypted_bytes: bytes) -> str:
        """Расшифровка полученных из сети данных."""
        return self.cipher.decrypt(encrypted_bytes).decode()

if __name__ == "__main__":
    key = load_or_create_key()
    security = GameSecurity(key)

    print("-" * 30)
    
    raw_password = "player_secret_123"
    hashed = security.hash_password(raw_password)
    print(f"ПАРОЛЬ: {raw_password}")
    print(f"ХЕШ ДЛЯ БАЗЫ (SHA-256): {hashed}")

    print("-" * 30)

    game_data = '{"player_id": 42, "pos": [100, 250], "inventory": ["sword", "shield"]}'
    print(f"ИСХОДНЫЕ ДАННЫЕ: {game_data}")

    encrypted = security.encrypt_traffic(game_data)
    print(f"ЗАШИФРОВАННЫЙ ТРАФИК (Fernet): {encrypted}")

    decrypted = security.decrypt_traffic(encrypted)
    print(f"РАСШИФРОВАННЫЕ ДАННЫЕ: {decrypted}")

    print("-" * 30)
    print("Внимание: Файл .env был изменен/создан. Не забудьте добавить его в .gitignore!")
