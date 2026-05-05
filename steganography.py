from PIL import Image
import numpy as np
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

STOP_MARKER = "###END###"


def generate_key_from_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")
    sha256_key = hashlib.sha256(password_bytes).digest()
    return base64.urlsafe_b64encode(sha256_key)


def encrypt_message_with_password(message: str, password: str) -> str:
    key = generate_key_from_password(password)
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(message.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")


def decrypt_message_with_password(encrypted_message: str, password: str) -> str:
    key = generate_key_from_password(password)
    fernet = Fernet(key)

    try:
        decrypted_bytes = fernet.decrypt(encrypted_message.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except InvalidToken:
        raise ValueError("Senha incorreta ou mensagem corrompida.")


def text_to_bits(text: str) -> str:
    data = text.encode("utf-8")
    return "".join(format(byte, "08b") for byte in data)


def encode_in_image(image_path: str, secret_message: str, password: str):
    image = Image.open(image_path).convert("RGB")
    data = np.array(image)
    flat = data.flatten()

    encrypted_message = encrypt_message_with_password(secret_message, password)
    final_message = encrypted_message + STOP_MARKER
    bits = text_to_bits(final_message)

    if len(bits) > len(flat):
        raise ValueError("Mensagem muito grande para a imagem.")

    for i, bit in enumerate(bits):
        flat[i] = (flat[i] & 0b11111110) | int(bit)

    new_data = flat.reshape(data.shape)
    return Image.fromarray(np.uint8(new_data))


def extract_encrypted_text_from_image(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    data = np.array(image)
    flat = data.flatten()

    bits = ""
    message = ""

    for value in flat:
        bits += str(value & 1)

        if len(bits) == 8:
            char = chr(int(bits, 2))
            message += char
            bits = ""

            if STOP_MARKER in message:
                return message.replace(STOP_MARKER, "")

    raise ValueError("Nenhuma mensagem encontrada na imagem.")


def extract_from_image(image_path: str, password: str) -> str:
    encrypted_text = extract_encrypted_text_from_image(image_path)
    return decrypt_message_with_password(encrypted_text, password)