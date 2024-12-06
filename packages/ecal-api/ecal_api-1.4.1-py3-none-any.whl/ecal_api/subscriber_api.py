# subscriber_api.py

import requests
import json
from .utils import m5_signature, status_code

class SubscriberAPI:
    def __init__(self, api_key, secret):
        """
        Initialize the SubscriberAPI object with API key and secret.

        Args:
            api_key (str): The API key provided by ECAL.
            secret (str): The secret key for signing requests.
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = 'https://api.ecal.com/'

    def get_subscriber(self, subscriber_id):
        """
        Get details of a single subscriber.

        Args:
            subscriber_id (str): The ID of the subscriber.

        Returns:
            dict: Details of the subscriber.
        """
        # Define the endpoint URL for retrieving a single subscriber's details
        endpoint = f'{self.base_url}apiv2/subscriber/{subscriber_id}'
        
        # Ensure params is a dictionary and add the API key to the parameters
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        
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

    def get_subscription(self, email_address):
        """
        Get subscription details by email address.

        Args:
            email_address (str): The email address of the subscriber.

        Returns:
            dict: Details of the subscription.
        """
        # Define the endpoint URL for retrieving subscription details by email address
        endpoint = f'{self.base_url}apiv2/subscriber/{email_address}'
        
        # Ensure params is a dictionary and add the API key to the parameters
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        
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
