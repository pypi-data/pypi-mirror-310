import getpass
import os

import requests

from cobalt.config import load_config, save_config


class AnyAPIWrapper:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = ""
        if not self.api_key:
            raise ValueError("API key is required")

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        response = requests.get(url, headers=headers, params=params)
        return self.handle_response(response)

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        response = requests.post(url, headers=headers, json=data)
        return self.handle_response(response)

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        response = requests.put(url, headers=headers, json=data)
        return self.handle_response(response)

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        response = requests.delete(url, headers=headers)
        return self.handle_response(response)

    @staticmethod
    def handle_response(response):
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            response.raise_for_status()


class OpenAIWrapper(AnyAPIWrapper):
    def __init__(self, api_key=None):
        self.api_key = api_key
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"

    @property
    def name(self):
        return "OpenAI APi Wrapper"

    def do_something(self, params):
        # TODO: add specific endpoints for Open AI ?
        pass

    def __repr__(self):
        return self.name


API_CLIENT_MAP = {"openai": {"cls": OpenAIWrapper, "env_var_name": "OPENAI_API_KEY"}}


def setup_api_client():
    """Set up the API client by updating or adding the API key to the JSON config file."""
    config = load_config()

    api_name = input(
        f"Choose API client from the list: {list(API_CLIENT_MAP.keys())}: "
    ).strip()
    api_client_config = API_CLIENT_MAP.get(api_name)

    if not api_client_config:
        raise ValueError(
            f"Unrecognized API client name. Valid names are: {list(API_CLIENT_MAP.keys())}"
        )

    api_key = getpass.getpass(f"Enter your valid API KEY for {api_name}: ").strip()
    api_client_env_name = api_client_config["env_var_name"]

    # Check if the API key already exists in the config
    if api_client_env_name in config["api_keys"]:
        overwrite = (
            input(
                f"API key for {api_name} already exists. Do you want to overwrite it? (yes/no): "
            )
            .strip()
            .lower()
        )
        if overwrite == "yes":
            config["api_keys"][api_client_env_name] = api_key
            print(f"API key for {api_name} was updated.")
        else:
            print(f"API key for {api_name} was not updated.")
    else:
        # Add new API key to the config
        config["api_keys"][api_client_env_name] = api_key
        print(f"API key for {api_name} saved.")

    # Save the updated config back to the JSON file
    save_config(config)


def get_api_client(api_name: str = "openai"):
    """Get the API client by loading the API key from the JSON config or environment variables."""
    config = load_config()  # Load existing config from JSON

    api_client_config = API_CLIENT_MAP.get(api_name)
    if not api_client_config:
        raise ValueError(
            f"Unrecognized API client name. Valid names are: {list(API_CLIENT_MAP.keys())}"
        )

    api_client_cls = api_client_config["cls"]
    api_client_env_name = api_client_config["env_var_name"]

    # Try to get the API key from the JSON config first
    api_key = config["api_keys"].get(api_client_env_name)

    # Check if the API key is set in the environment variables
    api_key_from_env = os.getenv(api_client_env_name)
    if not api_key and not api_key_from_env:
        raise ValueError(
            "You need to configure your API client first. "
            "Run Workspace.setup_api_client()"
        )

    # If the environment variable is set, it overrides the config file key
    if api_key_from_env:
        api_key = api_key_from_env
    return api_client_cls(api_key=api_key)
