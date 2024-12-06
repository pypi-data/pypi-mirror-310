# fridaylabs/endpoints/chat.py
import requests
from ..utils.colors import Colors

class Chat:
    """
    Chat endpoint class for making chat-related API calls.
    """
    def __init__(self, api_key, api_url='https://api.fridaylabs.ai', verbose=False):
        """
        Initialize the Chat endpoint.
        
        Args:
            api_key (str): Your FridayLabs API key
            api_url (str, optional): API base URL. Defaults to 'https://api.fridaylabs.ai'
            verbose (bool, optional): Enable verbose output. Defaults to False
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.verbose = verbose

    def _send_request(self, method, endpoint, payload=None):
        """
        Send an HTTP request to the API.
        
        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            endpoint (str): API endpoint
            payload (dict, optional): Request payload. Defaults to None
            
        Returns:
            dict: JSON response from the API
            
        Raises:
            requests.exceptions.HTTPError: If the HTTP request fails
            requests.exceptions.RequestException: If there's a network error
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        if self.verbose:
            print(f"{Colors.HEADER}{Colors.BOLD}Sending {method.upper()} request to {url}{Colors.ENDC}")

        try:
            response = requests.request(method, url, headers=headers, json=payload)
            response.raise_for_status()
            if self.verbose:
                print(f"{Colors.OKGREEN}{Colors.BOLD}Request successful!{Colors.ENDC}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if self.verbose:
                print(f"{Colors.FAIL}{Colors.BOLD}HTTP error occurred: {Colors.ENDC}{http_err}")
            raise http_err
        except Exception as err:
            if self.verbose:
                print(f"{Colors.FAIL}{Colors.BOLD}An unexpected error occurred: {Colors.ENDC}{err}")
            raise err

    def chat_completion(self, model, messages, temperature=1, max_tokens=256,
                       top_p=1, frequency_penalty=0, presence_penalty=0):
        """
        Create a chat completion.
        
        Args:
            model (str): The model to use
            messages (list): List of message dictionaries
            temperature (float, optional): Sampling temperature. Defaults to 1
            max_tokens (int, optional): Maximum tokens to generate. Defaults to 256
            top_p (float, optional): Nucleus sampling parameter. Defaults to 1
            frequency_penalty (float, optional): Frequency penalty. Defaults to 0
            presence_penalty (float, optional): Presence penalty. Defaults to 0
            
        Returns:
            dict: The API response containing the generated chat completion
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        return self._send_request('POST', '/chat', payload)