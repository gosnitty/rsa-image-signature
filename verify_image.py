"""
import libraries
"""
import argparse
import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from PIL import Image

def load_public_key(key_path):
    """
    Load the public key from a PEM file.
    """
    with open(key_path, 'rb') as key_file:
        return serialization.load_pem_public_key(
            key_file.read()
        )

def verify_image():
    """
    Verifies the RSA signature of a PNG image.
    """
    parser = argparse.ArgumentParser(description='Checks RSA signature of a PNG image')
    parser.add_argument('image_path', help='The path to a PNG image')
    parser.add_argument('--public_key', default='keys/public_key.pem',
                      help='The path to the public key')

    args = parser.parse_args()

    try:
        if not args.image_path.lower().endswith('.png'):
            print("Error: Only PNG format is supported")
            return False

        public_key = load_public_key(args.public_key)

        with open(args.image_path, 'rb') as f:
            data = f.read()

        iend_pos = data.rfind(b'IEND') + 8
        if iend_pos == 7:
            raise ValueError("Failed to find the IEND marker in PNG")

        signature = data[iend_pos:]

        img = Image.open(args.image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        pixels = np.array(img)

        digest = hashes.Hash(hashes.SHA256())
        digest.update(pixels.tobytes())
        image_hash = digest.finalize()

        public_key.verify(
            signature,
            image_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("The signature is valid.")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == '__main__':
    verify_image()
