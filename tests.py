from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encrypt_string(input_string, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(input_string.encode())
    return cipher_text


def decrypt_string(cipher_text, key):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text


# 生成密钥
encryption_key = generate_key()

# 待加密的字符串
original_string = "S001"

# 加密字符串
encrypted_text = encrypt_string(original_string, encryption_key)
print(f"Original String: {original_string}")
print(f"Encrypted Text: {encrypted_text}")

# 解密字符串
decrypted_text = decrypt_string(encrypted_text, encryption_key)
print(f"Decrypted Text: {decrypted_text}")
