# account_api.py

import requests
import json
from .utils import m5_signature, status_code

class AccountAPI:
    def __init__(self, api_key, secret):
        """
        Initializes the AccountAPI object with API key and secret.

        Args:
            api_key (str): The API key provided by ECAL.
            secret (str): The secret key for signing requests.
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = 'https://api.ecal.com/'

    def get_accounts(self):
        """
        Retrieves details of a single account.

        Args:
            account_id (str): The ID of the account to retrieve.

        Returns:
            dict: Account details.
        """
        # Define the endpoint URL for retrieving account details
        endpoint = f'{self.base_url}apiv2/account'
        
        # Set up the parameters for the request, including the API key
        params = {'apiKey': self.api_key}
        
        # Generate the API signature using the provided utility function
        api_sign = m5_signature(self.api_key, self.secret, params)
        
        # Construct the full URL with parameters and the API signature
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        
        # Make the GET request to the API
        response = requests.get(full_url)
        
        # Check the status code of the response using the provided utility function
        exit = status_code(response.status_code)
        
        # If the status code indicates success, return the JSON response
        if exit['result']:
            return response.json()
        else:
            # If the status code indicates an error, return the error details
            return exit
