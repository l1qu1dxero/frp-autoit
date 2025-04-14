import os
import subprocess
import sys
import ghostUSB  # Ensure ghostUSB.py is in the same directory or installed as a module


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def list_devices():
    """Lists all connected Android devices."""
    try:
        output = subprocess.check_output(["adb", "devices"], universal_newlines=True)
        devices = output.strip().split("\n")[1:]  # Skip the header line
        if not devices:
            print("No devices connected.")
        else:
            print("Connected devices:")
            for index, device in enumerate(devices):
                print(f"{index + 1}. {device.split()[0]}")
    except Exception as e:
        print(f"Error listing devices: {e}")


def transfer_file_to_device(device_id, local_file, remote_path):
    """Transfers a file to the connected Android device."""
    try:
        subprocess.check_call(["adb", "-s", device_id, "push", local_file, remote_path])
        print(f"File {local_file} successfully transferred to {remote_path}.")
    except Exception as e:
        print(f"Error transferring file: {e}")


def pull_file_from_device(device_id, remote_file, local_path):
    """Pulls a file from the connected Android device."""
    try:
        subprocess.check_call(["adb", "-s", device_id, "pull", remote_file, local_path])
        print(f"File {remote_file} successfully pulled to {local_path}.")
    except Exception as e:
        print(f"Error pulling file: {e}")


def reboot_device(device_id):
    """Reboots the connected Android device."""
    try:
        subprocess.check_call(["adb", "-s", device_id, "reboot"])
        print(f"Device {device_id} is rebooting.")
    except Exception as e:
        print(f"Error rebooting device: {e}")


def show_menu():
    """Displays the menu options."""
    clear_screen()
    print("==== Ethical Android Management Tool ====")
    print("1. List connected devices")
    print("2. Transfer file to device")
    print("3. Pull file from device")
    print("4. Reboot device")
    print("5. Exit")
    print("=========================================")


def main():
    while True:
        show_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                list_devices()
            elif choice == 2:
                device_id = input("Enter device ID: ")
                local_file = input("Enter local file path: ")
                remote_path = input("Enter remote path on device: ")
                transfer_file_to_device(device_id, local_file, remote_path)
            elif choice == 3:
                device_id = input("Enter device ID: ")
                remote_file = input("Enter remote file path: ")
                local_path = input("Enter local path on computer: ")
                pull_file_from_device(device_id, remote_file, local_path)
            elif choice == 4:
                device_id = input("Enter device ID: ")
                reboot_device(device_id)
            elif choice == 5:
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
