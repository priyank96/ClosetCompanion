import requests
import streamlit as st
import http.client
import typing
import urllib.request
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Image, Part

access_token = st.session_state.token['access_token']
r = requests.get('https://photoslibrary.googleapis.com/v1/albums', headers = {
    'Authorization': f"Bearer {access_token}"
})

r_json = r.json()
st.write(r_json)

# create helper function
def load_image_from_url(image_url: str) -> Image:
    with urllib.request.urlopen(image_url) as response:
        response = typing.cast(http.client.HTTPResponse, response)
        image_bytes = response.read()
    return Image.from_bytes(image_bytes)

def vertex(image_url):
    vertexai.init(project='wise-diagram-419102', location = "us-central1")
        # Load the model
    model = GenerativeModel(model_name="gemini-pro-vision")

    # Load example image
    image_content = load_image_from_url(image_url)

    # Query the model
    response = model.generate_content([image_content, "what is this image?"])
    st.write(response)

    return response.text

for album in r_json['albums']:
    if album['title'] == 'Meryl Streep':
        id = album['id']
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
        response = requests.post(url, json = {'albumId': id}, headers = {'Authorization': f"Bearer {access_token}"}).json()
        # print(response)
        for mediaItems in response['mediaItems']:
            image_url = mediaItems['baseUrl']
            image_data = requests.get(image_url, headers = {'Authorization': f"Bearer {access_token}"}).content
            st.image(image_data)
            resp = vertex(image_url)
            # st.write(image_url)
            
        