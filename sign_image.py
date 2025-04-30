"""
import libraries
"""
import os
import argparse
import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from PIL import Image

def load_private_key(key_path):
    """
    Load the private key from a PEM file.
    """
    with open(key_path, 'rb') as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

def sign_image():
    """
    Signs a PNG image with an RSA signature.
    """
    parser = argparse.ArgumentParser(description='Signs PNG images with an RSA signature')
    parser.add_argument('image_path', help='The path to a PNG image')
    parser.add_argument('--private_key', default='keys/private_key.pem',
                      help='The path to the private key')
    parser.add_argument('--output', help='Path for a signed imageя')

    args = parser.parse_args()

    if not args.image_path.lower().endswith('.png'):
        print("Error: Only PNG format is supported")
        return

    if args.output:
        output_path = args.output
    else:
        filename, ext = os.path.splitext(args.image_path)
        output_path = f"{filename}_signed.png"

    private_key = load_private_key(args.private_key)

    img = Image.open(args.image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    pixels = np.array(img)

    digest = hashes.Hash(hashes.SHA256())
    digest.update(pixels.tobytes())
    image_hash = digest.finalize()

    signature = private_key.sign(
        image_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    img.save(output_path, format='PNG')

    with open(output_path, 'ab') as f:
        f.write(signature)

    print(f"The image is captioned. Result: {output_path}")
    print(f"Signature size: {len(signature)} bytes")

if __name__ == '__main__':
    sign_image()
