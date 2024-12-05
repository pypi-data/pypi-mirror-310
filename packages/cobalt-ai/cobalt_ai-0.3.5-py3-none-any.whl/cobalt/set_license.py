import getpass
import os
import re
import shutil
from enum import Enum

import requests

from cobalt import check_license
from cobalt.config import (
    CONFIG_FILE_PATH,
    REGISTER_API_URL,
    is_colab_environment,
    load_config,
    save_config,
)


class RegisterType(Enum):
    NONCOMMERCIAL = "n"
    TRIAL = "t"


def register_license():
    print("Thank you for registering this copy of BluelightAI Cobalt!")
    config = load_config()
    register_type = input(
        "Enter 'n' to register for noncommercial use, "
        "or 't' to register for commercial trial use: "
    ).strip()
    if register_type == RegisterType.NONCOMMERCIAL.value:
        print(
            "Please enter your name and email address to register this copy for noncommercial use."
        )
        result = register_by_license_type(RegisterType.NONCOMMERCIAL.value)

    elif register_type == RegisterType.TRIAL.value:
        print(
            "Please enter your name, email address, and company to register and begin your trial."
        )
        result = register_by_license_type(RegisterType.TRIAL.value)
    else:
        result = {}
        print(f"Error: Invalid registration type {register_type}!")
        config["config"]["license_type"] = LicenseType.UNREGISTERED.value

    if result.get("message"):
        data = result["message"]["data"]["attributes"]
        license_key = data["key"]
        config["license_key"] = license_key
        info_to_update = {
            "name": data["metadata"]["name"],
            "email": data["metadata"]["email"],
            "company": data["metadata"].get("company"),
            "license_type": data["metadata"]["licenseType"],
        }
        config["config"].update(info_to_update)
    if result.get("error"):
        config["config"]["license_type"] = LicenseType.UNREGISTERED.value
    save_config(config)
    check_license()


def register_by_license_type(license_type):
    payload = {}
    result = {}
    error_email_msg = (
        "Invalid email address. Please run cobalt.register_license() again."
    )

    if license_type == RegisterType.NONCOMMERCIAL.value:
        name = input("Name: ")
        email = input("Email: ")
        if not is_valid_email(email):
            print(error_email_msg)
            result["error"] = error_email_msg
            return result

        payload["license_type"] = LicenseType.NONCOMMERCIAL.value
        payload["name"] = name
        payload["email"] = email
        success_msg = "Your noncommercial license is now registered."
    else:
        name = input("Name: ")
        email = input("Email: ")
        if not is_valid_email(email):
            print(error_email_msg)
            result["error"] = error_email_msg
            return result
        company = input("Company: ")
        payload["license_type"] = LicenseType.TRIAL.value
        payload["name"] = name
        payload["email"] = email
        payload["company"] = company
        success_msg = "Your trial is now registered."

    result = register_cobalt(payload)
    if result["error"]:
        print(f"Registration failed due to an error: {result['error']}")
    else:
        print(success_msg)
    return result


def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None


def setup_license():
    """Prompts for a license key and sets it in the configuration file.

    The license key will be saved in ~/.config/cobalt/cobalt.json.
    """
    print("Welcome to the Cobalt License Setup Wizard!")
    # Online license setup
    license_key = getpass.getpass("Please enter your license key: ").strip()
    setup_key(license_key)
    print("License key successfully set up!")
    print("validating license key...")
    check_license()


def setup_license_offline():
    license_key = getpass.getpass("Please enter your license key: ").strip()
    # Offline license setup via license file
    license_file = input(
        "Please enter the path to your license file (leave empty for the current directory): "
    ).strip()
    if not license_file:
        license_file = os.path.join(os.getcwd(), "license.lic")
        print("No path provided. Using default license file: license.lic")

    # Check if the file exists and validate
    if os.path.isfile(license_file):
        if license_file_not_empty(license_file):
            try:
                setup_key(license_key)

                config_dir = os.path.dirname(CONFIG_FILE_PATH)
                shutil.copy(license_file, config_dir)
                print("validating license file...")
                check_license()
            except Exception as e:
                print(f"Failed to set up offline license: {e}")
            print("License successfully set up using the license file!")
        else:
            print("Invalid license file content")
    else:
        print(
            f"License file not found at '{license_file}'. Please check the path and try again."
        )


def license_file_not_empty(license_file_path):
    try:
        with open(license_file_path) as file:
            license_data = file.read().strip()
            return bool(license_data)
    except Exception as e:
        print(f"Error reading license file: {e}")
        return False


def setup_key(license_key):
    config_data = load_config()
    config_data["license_key"] = license_key
    save_config(config_data)


class LicenseType(Enum):
    UNREGISTERED = "unregistered"
    TRIAL = "trial"
    NONCOMMERCIAL = "noncommercial"


def check_license_type():
    show_register_message = False
    config = load_config()
    license_type = config["config"].get("license_type")
    if not license_type:
        config["config"]["license_type"] = LicenseType.UNREGISTERED.value
        save_config(config)
        show_register_message = True
    elif license_type == LicenseType.UNREGISTERED.value:
        show_register_message = True

    if show_register_message and not is_colab_environment():
        print(
            "Thank you for using BluelightAI Cobalt!\n"
            "This version is licensed for noncommercial and trial use.\n"
            "Please register by running cobalt.register_license()"
        )


def register_cobalt(payload):
    result = {"error": None, "message": None}
    headers = {"x-cobalt-license-request": "true"}
    response = requests.post(
        f"{REGISTER_API_URL}/create-license", data=payload, headers=headers
    )
    if response.status_code != 200:
        result["error"] = response.json()
    else:
        message = response.json()
        if message.get("error"):
            result["error"] = message["error"]
        else:
            result["message"] = message
    return result
