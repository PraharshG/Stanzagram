import socket
import cv2
import RPi.GPIO as GPIO 
import os
import io
import struct
import time
import pickle
import zlib

SERVER_ADDRESS = "" #your server address

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
	print("Error opening video stream")

while True:
	if GPIO.input(10) == GPIO.HIGH:
		ret, frame = cap.read()
		if not ret:
			print("No frame Recieved")
		cv2.imwrite("image.jpeg", frame)
		break

IMAGE_PATH = "image.jpg"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, 12346))
connection = client_socket.makefile('wb')

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

data = pickle.dumps(frame, 0)
size = len(data)

print("{}: {}".format(img_counter, size))
client_socket.sendall(struct.pack(">L", size) + data)