"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
Before running this:
export GOOGLE_APPLICATION_CREDENTIALS="service-account-bahama-ta-stage.json"
Save the kannada text to speak in input.txt
"""
from google.cloud import texttospeech
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("languageCode", help="en-IN or hi-IN or kn-IN")
parser.add_argument("name", help="en-IN-Wavenet-D or kn-IN-Wavenet-A")
args = parser.parse_args()

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code=args.languageCode, name=args.name, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=0.8
)

with open("input.txt", "r") as input:
    lines = input.read().splitlines()
for line in lines:
    if line.find('/') != -1:
        continue
    items = line.split("\t")
    if len(items) != 2 or not items[0].endswith('.mp3'):
        print('Error: '+items)
        continue
    # The response's audio_content is binary.
    with open(items[0], "wb") as out:
        # line = line.replace('_', ' ')
        synthesis_input = texttospeech.SynthesisInput(text=items[1])
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # Write the response to the output file.
        out.write(response.audio_content)
        print(line)