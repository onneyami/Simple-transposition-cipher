import string

class SimpleTranspositionCipher:
    def __init__(self):
        # Алфавит: строго латинские буквы (A-Z, a-z) и пробел
        self.latin_alphabet = set(string.ascii_letters + " ")

    def validate_text(self, text: str) -> bool:
        """Проверка: открытый текст должен состоять ТОЛЬКО из латинских букв и пробелов."""
        if not text:
            return False
        return set(text).issubset(self.latin_alphabet)

    def validate_key(self, key: str) -> bool:
        """Проверка: ключ должен состоять ТОЛЬКО из латинских букв (без пробелов)."""
        if not key:
            return False
        return set(key).issubset(set(string.ascii_letters))

    def _get_key_order(self, key: str) -> list[int]:
        indexed_key = list(enumerate(key))
        sorted_key = sorted(indexed_key, key=lambda x: x[1])
        return [item[0] for item in sorted_key]

    def encrypt(self, plain_text: str, key: str) -> str:
        if not self.validate_text(plain_text):
            raise ValueError("Текст содержит нелатинские символы!")
        if not self.validate_key(key):
            raise ValueError("Ключ содержит нелатинские символы!")

        key_length = len(key)
        remainder = len(plain_text) % key_length
        if remainder != 0:
            plain_text += "X" * (key_length - remainder)

        num_rows = len(plain_text) // key_length
        order = self._get_key_order(key)

        cipher_text = []
        for col in order:
            for row in range(num_rows):
                index = row * key_length + col
                cipher_text.append(plain_text[index])

        return "".join(cipher_text)

    def decrypt(self, cipher_text: str, key: str) -> str:
        if not self.validate_text(cipher_text):
            raise ValueError("Шифртекст содержит нелатинские символы!")
        if not self.validate_key(key):
            raise ValueError("Ключ содержит нелатинские символы!")

        key_length = len(key)
        if len(cipher_text) % key_length != 0:
            raise ValueError("Длина шифртекста не кратна длине ключа!")

        num_rows = len(cipher_text) // key_length
        order = self._get_key_order(key)

        grid = [''] * len(cipher_text)
        cipher_idx = 0
        for col in order:
            for row in range(num_rows):
                grid_idx = row * key_length + col
                grid[grid_idx] = cipher_text[cipher_idx]
                cipher_idx += 1

        return "".join(grid)


# --- Вспомогательные функции безопасного ввода с проверкой ---

def input_valid_text(cipher: SimpleTranspositionCipher, prompt_message: str) -> str:
    """Запрашивает текст у пользователя до тех пор, пока не будут введены только латинские буквы."""
    while True:
        user_input = input(prompt_message)
        if cipher.validate_text(user_input):
            return user_input
        print("❌ Ошибка: Введены недопустимые символы! Используйте только ЛАТИНИЦУ (A-Z, a-z) и пробелы.\n")

def input_valid_key(cipher: SimpleTranspositionCipher, prompt_message: str) -> str:
    """Запрашивает ключ у пользователя до тех пор, пока не будут введены только латинские буквы."""
    while True:
        user_input = input(prompt_message)
        if cipher.validate_key(user_input):
            return user_input
        print("❌ Ошибка: Ключ должен состоять только из ЛАТИНСКИХ букв (без цифр, пробелов и кириллицы)!\n")


def main():
    cipher = SimpleTranspositionCipher()

    print("=== Криптосистема Простой Перестановки (Вариант 11) ===")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    choice = input("Выберите режим (1 или 2): ").strip()

    if choice == "1":
        print("\n--- Режим шифрования ---")
        plain_text = input_valid_text(cipher, "Введите открытый текст (строго латиница): ")
        key = input_valid_key(cipher, "Введите ключ (строго латинские буквы): ")

        cipher_text = cipher.encrypt(plain_text, key)
        print(f"\nУспешно! Зашифрованный текст: {cipher_text}")

    elif choice == "2":
        print("\n--- Режим расшифрования ---")
        cipher_text = input_valid_text(cipher, "Введите шифртекст (строго латиница): ")
        key = input_valid_key(cipher, "Введите ключ (строго латинские буквы): ")

        try:
            decrypted_text = cipher.decrypt(cipher_text, key)
            print(f"\nУспешно! Расшифрованный текст: {decrypted_text}")
        except ValueError as e:
            print(f"\n❌ Ошибка: {e}")
    else:
        print("Неверный выбор режима.")

if __name__ == "__main__":
    main()