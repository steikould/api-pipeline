import json
import logging
import time
import re
from typing import Dict, List, Union, Optional
from google.cloud import secretmanager
from google.cloud import storage

from google.api_core.exceptions import NotFound, GoogleAPIError, InvalidArgument

import base64
import requests


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_json_to_gcs(data: dict, bucket_name: str, blob_name: str, content_type: str = 'application/json') -> str:
    """
    Uploads a Python dictionary as a JSON file to a GCS bucket.

    This method is designed to be robust and production-ready for Google Cloud
    environments like Dataflow or Cloud Run, where authentication is handled
    automatically by Application Default Credentials (ADC).

    Args:
        data (dict): The Python dictionary to be converted to JSON and uploaded.
        bucket_name (str): The name of the GCS bucket.
        blob_name (str): The full path where the JSON file will be stored within the bucket
                         (e.g., 'output/results_2025-07-14.json').
        content_type (str, optional): The MIME type of the uploaded content. Defaults to 'application/json'.
    Returns:
        str: The public URL of the uploaded blob, if successful.

    Raises:
        json.JSONEncodeError: If the input data cannot be serialized to JSON.
        GoogleAPIError: If there's any issue interacting with the GCS API (e.g., permissions).
        Exception: For any other unexpected errors during the process.
    """
    logging.info(f"Attempting to upload JSON data to gs://{bucket_name}/{blob_name}")
    
    with storage.Client() as storage_client:  # ADC handles authentication automatically

        try:
            # Convert the Python dictionary to a JSON string
            # `ensure_ascii=False` allows non-ASCII characters (e.g., emojis, other language)
            json_string = json.dumps(data, ensure_ascii=False, indent=None)  # indent=None for minimal size - change to 2 for readibility

            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)

            # upload_from_string() method has built-in retries for transient errors.
            blob.upload_from_string(json_string, content_type=content_type)

            # [FUTURE] - Compression (gzip)

            logging.info(f"Successfully uploaded JSON data to gs://{bucket_name}/{blob_name}")
            return f"gs://{bucket_name}/{blob_name}"

        except json.JSONEncodeError as e:
            logging.error(f"Error encoding data to JSON for blob '{blob_name}'. Details: {e}")
            raise
        except GoogleAPIError as e:
            logging.error(f"Error interacting with Google Cloud Storage API for '{blob_name}'. Details: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while uploading JSON to '{blob_name}'. Details: {e}")
            raise


def get_secret_value(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Retrieves the value of a secret from Google Secret Manager.

    This function is designed to be robust and production-ready for Google Cloud
    environments like Dataflow or Cloud Run, where authentication is handled
    automatically by Application Default Credentials (ADC).

    Args:
        project_id (str): The Google Cloud project ID where the secret is stored.
        secret_id (str): The ID of the secret (e.g., 'my-api-key').
        version_id (str, optional): The version of the secret to retrieve.
                                    Defaults to 'latest'. Can also be a specific
                                    version number (e.g., '1', '2').

    Returns:
        str: The secret value as a string.

    Raises:
        NotFound: If the secret or the specified version does not exist.
        InvalidArgument: If the project ID or secret ID format is invalid.
        GoogleAPIError: For other API-related errors (e.g., permission denied).
        ValueError: If input validation fails.
        Exception: For any other unexpected errors during the process.
    """
    # Input validation
    if not project_id or not isinstance(project_id, str):
        raise ValueError("project_id must be a non-empty string")
    if not secret_id or not isinstance(secret_id, str):
        raise ValueError("secret_id must be a non-empty string")
    if not re.match(r'^[a-zA-Z0-9_-]+$', secret_id):
        raise ValueError("secret_id contains invalid characters")
    
    # Initialize the Secret Manager client.
    # ADC handles authentication automatically in Google Cloud environments.
    with secretmanager.SecretManagerServiceClient() as client:

        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        logging.info(f"Attempting to access secret: {name}")

        try:
            # Access the secret version.
            # The client library automatically handles retries for transient errors.
            response = client.access_secret_version(request={"name": name})

            # Extract the payload (secret data) and decode it.
            secret_value = response.payload.data.decode("UTF-8")
            logging.info(f"Successfully retrieved secret '{secret_id}' (version: {version_id}).")
            return secret_value

        except NotFound as e:
            logging.error(f"Secret '{secret_id}' (version: {version_id}) not found in project '{project_id}'. Details: {e}")
            raise
        except InvalidArgument as e:
            logging.error(f"Invalid argument provided for secret access (e.g., malformed project/secret ID). Details: {e}")
            raise
        except GoogleAPIError as e:
            logging.error(f"Google Secret Manager API error for secret '{secret_id}'. Details: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while getting secret '{secret_id}'. Details: {e}")
            raise


def get_basic_auth_header(access_id: str, access_key: str) -> Dict[str, str]:
    """
    Generates a Basic Authentication header for HTTP requests.
    
    Args:
        access_id (str): The access ID/username for authentication.
        access_key (str): The access key/password for authentication.
        
    Returns:
        Dict[str, str]: Dictionary containing Authorization and Content-Type headers.
    """
    logging.info("Generating Authentication Header for Request...")
    credentials = f"{access_id}:{access_key}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
    return {'Authorization': f'Basic {encoded_credentials}', "Content-Type": "application/json"}


def fetch_endpoint_data(
    base_url: str, 
    endpoint: str, 
    headers: Dict[str, str],
    page_size: int = 10000,
    rate_limit_delay: float = 0.1
) -> List[Dict]:
    """
    Fetch data from Enablon API with pagination support and rate limiting.
    
    Args:
        base_url (str): The base URL for the API.
        endpoint (str): The specific endpoint to fetch data from.
        headers (Dict[str, str]): Headers to include in the request.
        page_size (int, optional): Number of records to fetch per request. Defaults to 10000.
        rate_limit_delay (float, optional): Delay between requests in seconds. Defaults to 0.1.
        
    Returns:
        List[Dict]: List of records fetched from the endpoint.
        
    Raises:
        requests.exceptions.RequestException: If there's an HTTP error.
        Exception: For any other unexpected errors during the process.
    """
    url = f"{base_url}{endpoint}"
    logging.info(f"Fetching data from endpoint: {endpoint}")

    params = {
        "$top": page_size,
        "$skip": 0
    }

    data = []
    page_count = 0
    
    while True:
        try:
            # Rate limiting
            if page_count > 0:
                time.sleep(rate_limit_delay)
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            # Parse response
            json_response = response.json()

            if "value" in json_response:
                new_data = json_response["value"]
                if not new_data:
                    break
                data.extend(new_data)
                
                page_count += 1
                logging.info(f"Fetched page {page_count}, records: {len(new_data)}, total: {len(data)}")

                # Update skip parameter for next page
                params["$skip"] += len(new_data)
            else:
                if json_response:
                    data.append(json_response)
                break

        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP error fetching {endpoint}: {e}")
            raise
        except Exception as e:
            logging.error(f"Error fetching {endpoint}: {e}")
            raise

    logging.info(f"Successfully fetched {len(data)} total records from {endpoint}")
    return data