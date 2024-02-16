import requests 

import requests 

def send_model_to_staging(api_url: str, model_file: str):
    try:
        with open(model_file, 'rb') as file:
            files = {'modelFile': file}  
            response = requests.post(api_url, files=files)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None 
    
if __name__ == "__main__":
    result = send_model_to_staging("http://0.0.0.0:8000/upload/model", "./my-model/clf_lda.joblib")
    if result:
        print("File successfully uploaded to the API")
        print("Response from API: ", result)
    else:
        print("Failed to upload file to the API")