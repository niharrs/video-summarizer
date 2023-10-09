import pytube
import requests
import os
from dotenv import find_dotenv, load_dotenv
import openai
import streamlit as st

st.title('YouTube Video Summarization')

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN=os.getenv("HUGGINGFACE_API_TOKEN")

# Extract audio from YouTube
def get_audio(video_url):
    # Create a PyTube object for the video.
    youtube_video = pytube.YouTube(video_url)

    # Get the audio stream from the video.
    audio_stream = youtube_video.streams.filter(only_audio=True)

    # Get title
    st.write("Now summarizing: ", youtube_video.streams[0].title)

    # Download the audio stream to a file.
    audio_stream[0].download(output_path="audios", filename="audio.mp3")

# Audio to text
def get_text(filename):
    audio_file= open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

# Summarize
def summarize(transcript):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}

    payload = {
        "inputs": transcript
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


youtube_link = st.text_input('YouTube Video:', 'Enter URL here')

def process_input(youtube_link):
    get_audio(youtube_link)
    video_text = get_text("audios/audio.mp3")
    video_text = video_text.text
    summary = summarize(video_text)
    return summary[0]

# Create a button to trigger the function
if st.button("Summarize Video"):
    result = process_input(youtube_link)  # Call the function with user input
    st.write("Summary", result)  # Display the result
