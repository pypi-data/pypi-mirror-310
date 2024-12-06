import base64


def log(message):
    """Logs a message to the console."""
    print(message)


def invert_bits(byte_str):
    """Inverts each bit in a byte string."""
    return bytearray([~b & 0xFF for b in byte_str])


def encrypt(input_string):
    """
    Encrypts a string by inverting its bits and encoding it in Base64.

    Args:
        input_string (str): The string to encrypt.

    Returns:
        str: The encrypted Base64 string.
    """
    log(f"Original string: {input_string}")

    # Convert string to bytes
    byte_str = input_string.encode('utf-8')
    log(f"Converted string to bytes: {byte_str}")

    # Invert the bits
    inverted_bytes = invert_bits(byte_str)
    log(f"Inverted bits: {inverted_bytes}")

    # Encode the inverted bytes in Base64
    base64_encoded = base64.b64encode(inverted_bytes).decode('utf-8')
    log(f"Encrypted string in Base64: {base64_encoded}")

    return base64_encoded


def decrypt(base64_string):
    """
    Decrypts a Base64 string by decoding it and restoring the original bits.

    Args:
        base64_string (str): The Base64-encoded string to decrypt.

    Returns:
        str: The decrypted original string.
    """
    # Decode Base64 to bytes
    decoded_bytes = base64.b64decode(base64_string)
    log(f"Decoded string from Base64: {decoded_bytes}")

    # Restore the original bits
    restored_bytes = invert_bits(decoded_bytes)
    log(f"Bytes after restoring (bit inversion): {restored_bytes}")

    # Convert bytes back to a string
    restored_str = restored_bytes.decode('utf-8', errors='ignore')
    log(f"Restored string: {restored_str}")

    return restored_str
