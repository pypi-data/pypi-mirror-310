# event_api.py

import requests
import json
from .utils import m5_signature, status_code

class EventAPI:
    def __init__(self, api_key, secret):
        """
        Initialize the EventAPI object with API key and secret.

        Args:
            api_key (str): The API key provided by ECAL.
            secret (str): The secret key for signing requests.
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = 'https://api.ecal.com/'

    def get_events(self, params=None):
        """
        Get a list of events.

        Args:
            params (dict): Parameters for filtering events.

        Returns:
            dict: Response containing a list of events.
        """
        # Define the endpoint URL for retrieving the list of events
        endpoint = f'{self.base_url}apiv2/event'
        
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

    def get_event(self, event_id, params=None):
        """
        Get details of a single event.

        Args:
            event_id (str): The ID of the event.
            params (dict, optional): Additional parameters.

        Returns:
            dict: Details of the event.
        """
        # Define the endpoint URL for retrieving a single event's details
        endpoint = f'{self.base_url}apiv2/event/{event_id}'
        
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

    def create_event(self, event_data):
        """
        Create a new event.

        Args:
            event_data (dict): Data for creating the event.

        Returns:
            dict: Response data.
        """
        # Define the endpoint URL for creating a new event
        endpoint = f'{self.base_url}apiv2/event/'
        
        # Set up the parameters for the request, including the API key and event data
        params = {'apiKey': self.api_key, 'json_data': json.dumps(event_data)}
        
        # Generate the API signature using the provided utility function
        api_sign = m5_signature(self.api_key, self.secret, params)
        
        # Construct the full URL with parameters and the API signature, excluding 'json_data'
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items() if key != "json_data"]) + f'&apiSign={api_sign}'
        
        # Make the POST request to the API with the event data
        response = requests.post(full_url, json=event_data)
        
        # Check the status code of the response using the provided utility function
        exit = status_code(response.status_code)
        
        # If the status code indicates success, return the JSON response
        if exit['result']:
            return response.json()
        else:
            # If the status code indicates an error, return the error details
            return exit

    def update_event(self, event_id, event_data):
        """
        Update an existing event.

        Args:
            event_id (str): The ID of the event to update.
            event_data (dict): Updated event data.

        Returns:
            dict: Response data.
        """
        # Define the endpoint URL for updating an existing event
        endpoint = f'{self.base_url}apiv2/event/{event_id}'
        
        # Set up the parameters for the request, including the API key and event data
        params = {'apiKey': self.api_key, 'json_data': json.dumps(event_data)}
        
        # Generate the API signature using the provided utility function
        api_sign = m5_signature(self.api_key, self.secret, params)
        
        # Construct the full URL with parameters and the API signature, excluding 'json_data'
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items() if key != "json_data"]) + f'&apiSign={api_sign}' + json.dumps(event_data)
        
        # Make the PUT request to the API with the updated event data
        response = requests.put(full_url, json=event_data)
        
        # Check the status code of the response using the provided utility function
        exit = status_code(response.status_code)
        
        # If the status code indicates success, return the JSON response
        if exit['result']:
            return response.json()
        else:
            # If the status code indicates an error, return the error details
            return exit

    def delete_event(self, event_id):
        """
        Delete an event.

        Args:
            event_id (str): The ID of the event to delete.

        Returns:
            dict: Response data.
        """
        # Define the endpoint URL for deleting an event
        endpoint = f'{self.base_url}apiv2/event/{event_id}'
        
        # Set up the parameters for the request, including the API key
        params = {'apiKey': self.api_key}
        
        # Generate the API signature using the provided utility function
        api_sign = m5_signature(self.api_key, self.secret, params)
        
        # Construct the full URL with parameters and the API signature
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        
        # Make the DELETE request to the API
        response = requests.delete(full_url)
        
        # Check the status code of the response using the provided utility function
        exit = status_code(response.status_code)
        
        # If the status code indicates success, return the JSON response
        if exit['result']:
            return response.json()
        else:
            # If the status code indicates an error, return the error details
            return exit
