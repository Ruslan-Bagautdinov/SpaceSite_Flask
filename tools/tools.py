import base64
import requests
import random

from config import UNSPLASH_ACCESS_KEY


def save_upload_file(upload_file, destination: str):
    with open(destination, 'wb') as out_file:
        while content := upload_file.read(1024):  # Read file in chunks
            out_file.write(content)


def read_and_encode_photo(photo_path):
    try:
        with open(photo_path, 'rb') as photo_file:
            photo_data = photo_file.read()
            photo_base64 = base64.b64encode(photo_data).decode('utf-8')
            return photo_base64
    except FileNotFoundError:
        print(f"File not found: {photo_path}")
        return None
    except Exception as e:
        print(f"Error encoding photo {photo_path}: {e}")
        return None


def load_unsplash_photo(query: str = "cosmos") -> str | None:
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,
        "orientation": "landscape",
        "per_page": 50
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('results'):
            random_index = random.randint(0, len(data['results']) - 1)
            image_url = data['results'][random_index]['urls']['regular']
        else:
            image_url = None
    except requests.HTTPError as errh:
        print("HTTP error occurred:", errh)
        image_url = None
    except requests.RequestException as err:
        print("An error occurred:", err)
        image_url = None

    return image_url
