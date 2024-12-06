# fridaylabs/client.py

import requests
from .utils.colors import Colors

class FridayLabsClient:
    def __init__(self, api_key, api_url='https://api.fridaylabs.ai', verbose=False):
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.verbose = verbose

    def _send_request(self, method, endpoint, payload=None):
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
            self._handle_http_error(response, http_err)
        except requests.exceptions.RequestException as req_err:
            self._handle_request_exception(req_err)
        except Exception as err:
            self._handle_generic_exception(err)

    def _handle_http_error(self, response, http_err):
        if self.verbose:
            print(f"{Colors.FAIL}{Colors.BOLD}HTTP error occurred: {Colors.ENDC}{http_err}")
            self._suggest_solution(response)
        raise http_err

    def _handle_request_exception(self, req_err):
        if self.verbose:
            print(f"{Colors.FAIL}{Colors.BOLD}Request error occurred: {Colors.ENDC}{req_err}")
            print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
            print(f"1. Check your network connection.")
            print(f"2. Verify the API URL: {self.api_url}")
            print(f"3. Ensure your API key is correct.")
        raise req_err

    def _handle_generic_exception(self, err):
        if self.verbose:
            print(f"{Colors.FAIL}{Colors.BOLD}An unexpected error occurred: {Colors.ENDC}{err}")
        raise err

    def _suggest_solution(self, response):
        status_code = response.status_code
        if self.verbose:
            print(f"{Colors.FAIL}Response content: {response.content}{Colors.ENDC}")
            print(f"{Colors.WARNING}Status code: {status_code}{Colors.ENDC}")
            # Add suggestions based on status code
            # Similar to your existing suggest_solution method
