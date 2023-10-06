from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, storage
import os
import requests
from moviepy.editor import *

app = Flask(__name__)
CORS(app)

# Firebase configuration
PROJECT_ID = os.environ.get('PROJECT_ID')
PRIVATE_KEY_ID = os.environ.get('PRIVATE_KEY_ID')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY').replace('\\n', '\n')
CLIENT_EMAIL = os.environ.get('CLIENT_EMAIL')
CLIENT_ID = os.environ.get('CLIENT_ID')
AUTH_URI = os.environ.get('AUTH_URI')
TOKEN_URI = os.environ.get('TOKEN_URI')
AUTH_PROVIDER_CERT_URL = os.environ.get('AUTH_PROVIDER_CERT_URL')
CLIENT_CERT_URL = os.environ.get('CLIENT_CERT_URL')
ELEVEN_API_KEY=os.environ.get('ELEVEN_API_KEY')

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": PROJECT_ID,
    "private_key_id": PRIVATE_KEY_ID,
    "private_key": PRIVATE_KEY,
    "client_email": CLIENT_EMAIL,
    "client_id": CLIENT_ID,
    "auth_uri": AUTH_URI,
    "token_uri": TOKEN_URI,
    "auth_provider_x509_cert_url": AUTH_PROVIDER_CERT_URL,
    "client_x509_cert_url": CLIENT_CERT_URL
})

firebase_admin.initialize_app(
    cred, {'storageBucket': 'storyboard-739ee.appspot.com'})

def upload_to_firebase(file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)
    blob.make_public()
    return blob.public_url

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    voice_id_name = request.json.get('voice_id')
    text = request.json.get('text')
    if voice_id_name=="Bella":
        voice_id="EXAVITQu4vr4xnSDxMaL"
    if voice_id_name=="Elli":
        voice_id="MF3mGyEYCl7XYWbV9V6O"
    if voice_id_name=="Emily":
        voice_id="LcfcDJNUP1GQjkzn1xUU"
    if voice_id_name=="Grace":
        voice_id="oWAxZDx7w5VEj9dCyTzz"
    if voice_id_name=="Josh":
        voice_id="TxGEqnHWrfWFTfGW9XjX"
    if voice_id_name=="Daniel":
        voice_id="onwK4e9ZLuTAKqWW03F9"
    if voice_id_name=="Dave":
        voice_id="CYw3kZ02Hs0563khs1Fj"
    if voice_id_name=="Dorothy":
        voice_id="ThT5KcBeYPX3keUQqHPh"
    if voice_id_name=="Joseph":
        voice_id="Zlb1dXrM653N07WRdFW3"
    if voice_id_name=="Matthew":
        voice_id="Yko7PKHZNXotIFUBG7I9"
    audio_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    audio_response = requests.post(audio_url, json=data, headers=headers)
    audio_path = "output.mp3"
    
    with open(audio_path, 'wb') as f:
        f.write(audio_response.content)

    audio_url = upload_to_firebase(audio_path)
    
    return jsonify({"audio_url": audio_url})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')