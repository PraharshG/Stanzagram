import socket
from PIL import Image

import cv2
import pickle

import struct ## new
import zlib

import sys

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np


GEMINI_API_KEY = "" #your gemini api key
# Load the ResNet50 model pre-trained on ImageNet data
model = ResNet50(weights='imagenet')

HOST='localhost'
PORT=12346

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.imwrite("received_image.jpg",frame)
    cv2.waitKey(1)


img_path = "received_image.jpg" # Replace with the path to your image file

img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# Make predictions
predictions = model.predict(img_array)

# Decode and print the top 5 predicted classes and their probabilities
decoded_predictions = decode_predictions(predictions, top=5)[0]

print("Top 5 Predictions:")
for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
    print(f"{i + 1}: {label} ({score:.2f})")
print()

import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)     

model = genai.GenerativeModel('gemini-pro')
objects=decoded_predictions

#objects = ["mountain", "stars", "falls", "bird", "tree", "house", "dog", "rain"]
# Extract labels from decoded_predictions   
labels = [label for _, label, _ in decoded_predictions]

# Convert labels to strings and join them
objects = ', '.join(labels)

prompt = f"""You are a poem generator.
Your task is to generate a single short poem (nothing else) given a list of words.
The poem must contain all 5 words in the list.
The poem can use synonyms of the words given in the list.
Generate a poem given the following list of words: {objects}\n"""
response = model.generate_content(prompt)
print("Generated Poem:")
print(response.text)

'''
to_markdown(response.text)

# ADDED THIS
import markdown2

# Convert Markdown text to plain text
plain_text = markdown2.markdown(response.text, extras=["markdown-in-html", "tables"])

# Print the plain text
print(plain_text)
'''


