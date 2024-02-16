import requests 
from pydantic import FilePath

def send_model_to_staging(api_url: str, model_file: FilePath):
    try:
        response = requests.post(api_url, files=model_file)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None 