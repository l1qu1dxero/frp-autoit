import os
import signal
import sys
import usb.core
import usb.util
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import secrets

class USBGhostTool:
    def __init__(self, password: str):
        self.password = password.encode()
        self.salt = os.urandom(16)
        self.key = self.generate_key(self.password, self.salt)
        self.device = None

    def generate_key(self, password: bytes, salt: bytes) -> bytes:
        """Generate an encryption key using PBKDF2."""
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            return kdf.derive(password)
        except Exception as e:
            print(f"Error generating encryption key: {e}")
            sys.exit(1)

    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data using AES encryption."""
        try:
            iv = secrets.token_bytes(16)  # Initialization vector
            cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            return iv + encryptor.update(data) + encryptor.finalize()
        except Exception as e:
            print(f"Error encrypting data: {e}")
            return b""

    def decrypt_data(self, data: bytes) -> bytes:
        """Decrypt data using AES encryption."""
        try:
            iv = data[:16]
            cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            return decryptor.update(data[16:]) + decryptor.finalize()
        except Exception as e:
            print(f"Error decrypting data: {e}")
            return b""

    def detect_usb(self):
        """Detect connected USB devices."""
        try:
            print("Detecting USB devices...")
            devices = usb.core.find(find_all=True)
            for device in devices:
                print(f"Device Found: ID {device.idVendor}:{device.idProduct}")
                self.device = device
                return device
            print("No USB devices found.")
        except usb.core.USBError as e:
            print(f"USB detection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def handle_usb_transfer(self):
        """Handle encrypted data transfer through USB."""
        if not self.device:
            print("No USB device detected. Aborting transfer.")
            return

        try:
            print("Initializing data transfer...")
            test_data = b"Hello USB Ghost!"
            encrypted_data = self.encrypt_data(test_data)
            print(f"Encrypted Data: {encrypted_data}")

            # Example: Writing and reading data to/from USB endpoint (mocked here)
            print("Sending encrypted data to USB...")
            # self.device.write(endpoint, encrypted_data) # Uncomment and adjust for your endpoint

            print("Receiving encrypted data from USB...")
            received_data = encrypted_data  # Simulating a loopback for demonstration

            # Decrypt received data
            decrypted_data = self.decrypt_data(received_data)
            print(f"Decrypted Data: {decrypted_data.decode()}")
        except usb.core.USBError as e:
            print(f"USB transfer error: {e}")
        except Exception as e:
            print(f"Unexpected error during USB transfer: {e}")

    def run(self):
        """Run the USB ghost tool."""
        try:
            self.detect_usb()
            if self.device:
                self.handle_usb_transfer()
        except KeyboardInterrupt:
            print("\nExiting USB Ghost Tool gracefully...")
        except Exception as e:
            print(f"Error: {e}")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\nExiting gracefully...")
    sys.exit(0)


if __name__ == "__main__":
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting USB Ghost Tool...")
    password = "secure_password"  # Use a strong password
    ghost_tool = USBGhostTool(password)

    print(f"Encryption Key (Keep this safe!): {ghost_tool.key.hex()}")
    print("Press CTRL+C to stop the tool.")

    # Run the tool
    ghost_tool.run()
