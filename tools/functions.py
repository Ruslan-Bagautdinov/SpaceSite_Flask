from flask import (
    redirect,
    session,
    url_for
)

import base64
import requests
import random
import os

from config import UNSPLASH_ACCESS_KEY, ALLOWED_EXTENSIONS
from templates.icons import WARNING_ICON, WARNING_CLASS, OK_ICON, OK_CLASS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload_file(upload_file, destination: str):
    # Ensure that the destination directory exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    # Save the file to the destination
    upload_file.save(destination)


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


def redirect_with_message(message_class: str,
                          message_icon: str,
                          message_text: str,
                          endpoint: str = None,
                          logout: bool = False):
    top_message = {
        "class": message_class,
        "icon": message_icon,
        "text": message_text,
    }
    session['top_message'] = top_message
    if logout:
        response = redirect(url_for('auth.logout', path='auth.login'))
    else:
        response = redirect(url_for(endpoint))
    return response


def error_message(message: str,
                  icon: str = WARNING_ICON,
                  endpoint: str = 'auth.login'):
    return redirect_with_message(
        message_class=WARNING_CLASS,
        message_icon=icon,
        message_text=message,
        endpoint=endpoint
    )


def ok_message(message: str,
               icon: str = OK_ICON,
               endpoint: str = 'root.root'):
    return redirect_with_message(
        message_class=OK_CLASS,
        message_icon=icon,
        message_text=message,
        endpoint=endpoint
    )
