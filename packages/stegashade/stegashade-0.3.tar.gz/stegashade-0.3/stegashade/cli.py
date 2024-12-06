from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt(data, password):
    """Encrypt data using AES with a password."""
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = kdf.derive(password.encode())

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Encrypt the data
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(salt + iv + encrypted).decode()  # Combine salt, iv, and encrypted data

def decrypt(encrypted_data, password):
    """Decrypt data using AES with a password."""
    encrypted_data = base64.b64decode(encrypted_data.encode())
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = kdf.derive(password.encode())

from PIL import Image
import numpy as np
import math
common_characters =  {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 11: 'j', 12: 'k', 13: 'l', 14: 'm', 15: 'n', 16: 'o', 17: 'p', 18: 'q', 19: 'r', 21: 's', 22: 't', 23: 'u', 24: 'v', 25: 'w', 26: 'x', 27: 'y', 28: 'z', 29: 'A', 31: 'B', 32: 'C', 33: 'D', 34: 'E', 35: 'F', 36: 'G', 37: 'H', 38: 'I', 39: 'J', 41: 'K', 42: 'L', 43: 'M', 44: 'N', 45: 'O', 46: 'P', 47: 'Q', 48: 'R', 49: 'S', 51: 'T', 52: 'U', 53: 'V', 54: 'W', 55: 'X', 56: 'Y', 57: 'Z', 58: '0', 59: '1', 61: '2', 62: '3', 63: '4', 64: '5', 65: '6', 66: '7', 67: '8', 68: '9', 69: '!', 71: '@', 72: '#', 73: '$', 74: '%', 75: '^', 76: '&', 77: '*', 78: '(', 79: ')', 81: '-', 82: '_', 83: '=', 84: '+', 85: ';', 86: ':', 87: "'", 88: '"', 89: ',', 91: '.', 92: '<', 93: '>', 94: '/', 95: '?', 96: ' '}


reversed_dict = {value: key for key, value in common_characters.items()}



def image_to_array(image_path):
    with Image.open(image_path) as img:
        return np.array(img)

def array_to_image(array, output_path):
    img = Image.fromarray(array)
    img.save(output_path)


def encode_data(dat):
    l = []
    for e in dat:
        x =  reversed_dict.get(e, 0)
        if x < 10:
            y = "0"
            x = str(x)
        else:
            x = str(x)
            y = x[0]
            x = x[1]

        l.append(y)
        l.append(x)

    return l

def decode_data(dat):
    l = ""
    prev = ""
    for e in dat:
        if prev == "":
            prev = e
        else:
            if prev == "0":
                l += common_characters.get(int(e), "<Unknown Char>")
                prev = ""
            else:
                l += common_characters.get(int(prev + e), "<Unknown Char>")
                prev = ""
    return l


def process_image_array(image_array, data):
    # Create an output array to store the processed values
    processed_array = image_array.copy()

    u = 0

    for i in range(processed_array.shape[0]):
        for j in range(processed_array.shape[1]):
            for e in range(processed_array.shape[2]):
                if e  != 3:
                    x =  str(processed_array[i, j , e])

                    if len(x) == 3:
                        x = x[0] + x[1] + "0"
                    elif len(x) == 2:
                        x = x[0] + "0"
                    else:
                        x = 10

                    x = int(x)

                    if u < len(data):
                        if u%2 == 0:
                            x += int(data[u])
                        else:
                            x -= int(data[u])
                        u += 1

                    processed_array[i, j, e] = x

    return processed_array

def simple_shade_stega(image_path, output, data):
    data =  encode_data(data + "##END##")
    img = image_to_array(image_path)
    img = process_image_array(img, data)
    array_to_image(img, output)

def undo_simple_shade_stega(image_path):
    processed_array = image_to_array(image_path)
    u = 0
    data = []
    for i in range(processed_array.shape[0]):
        for j in range(processed_array.shape[1]):
            for e in range(processed_array.shape[2]):
                if e  != 3:
                    x = str(processed_array[i, j, e])
                    if u%2 == 0:
                        data.append(x[-1])
                    else:
                        data.append(str(10-int(x[-1])))
                    u += 1

    dat = decode_data(data)
    return dat.rsplit("##END##", 1)[0]

def protected_shade_stega(image_path, output, data, pwd):
    simple_shade_stega(image_path, output, encrypt(data, pwd))

def undo_protected_shade_stega(image_path, pwd):
    return decrypt(undo_simple_shade_stega(image_path), pwd)

import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED
console = Console()

def display_help():
    """
    Displays the help message with available commands.
    """
    table = Table(title="Stega Shade - Command Reference", box=ROUNDED, show_edge=False)
    table.add_column("Command", style="cyan bold", justify="right")
    table.add_column("Description", style="green")

    table.add_row(
        "encode_simple <image_path> <output_path> \"<data>\"",
        "Encodes data into an image using simple steganography.",
    )
    table.add_row(
        "decode_simple <image_path>",
        "Decodes data from an image created with simple steganography.",
    )
    table.add_row(
        "encode_protected <image_path> <output_path> \"<data>\" \"<password>\"",
        "Encodes data into an image with password protection.",
    )
    table.add_row(
        "decode_protected <image_path> \"<password>\"",
        "Decodes password-protected data from an image.",
    )
    table.add_row("help", "Displays this help message.")

    console.print(
        Panel.fit(
            table,
            title="📷 Stega Shade CLI 📷",
            subtitle="Your Image Steganography Toolkit",
            border_style="magenta",
        )
    )


def main():
    """
    Main function to handle command-line arguments and execute steganography operations.
    """
    if len(sys.argv) < 2:
        console.print("[bold red]Error:[/] No command provided. Use 'help' for usage details.")
        sys.exit(1)

    command = sys.argv[1]

    if command == "help":
        display_help()
    elif command == "encode_simple":
        if len(sys.argv) != 5:
            console.print("[bold red]Error:[/] Incorrect arguments for encode_simple.")
            sys.exit(1)
        image_path, output_path, data = sys.argv[2], sys.argv[3], sys.argv[4]
        try:
            simple_shade_stega(image_path, output_path, data)
            console.print(f"[green]Successfully encoded data into '{output_path}'.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
    elif command == "decode_simple":
        if len(sys.argv) != 3:
            console.print("[bold red]Error:[/] Incorrect arguments for decode_simple.")
            sys.exit(1)
        image_path = sys.argv[2]
        try:
            decoded_data = undo_simple_shade_stega(image_path)
            console.print(f"[green]Decoded Data:[/] {decoded_data}")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
    elif command == "encode_protected":
        if len(sys.argv) != 6:
            console.print("[bold red]Error:[/] Incorrect arguments for encode_protected.")
            sys.exit(1)
        image_path, output_path, data, password = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        try:
            protected_shade_stega(image_path, output_path, data, password)
            console.print(f"[green]Successfully encoded protected data into '{output_path}'.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
    elif command == "decode_protected":
        if len(sys.argv) != 4:
            console.print("[bold red]Error:[/] Incorrect arguments for decode_protected.")
            sys.exit(1)
        image_path, password = sys.argv[2], sys.argv[3]
        try:
            decoded_data = undo_protected_shade_stega(image_path, password)
            console.print(f"[green]Decoded Data:[/] {decoded_data}")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
    else:
        console.print(f"[bold red]Error:[/] Unknown command '{command}'. Use 'help' for usage details.")
        sys.exit(1)


if __name__ == "__main__":
    main()

