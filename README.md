# Image-to-Poetry Project

This repository contains two interconnected Python scripts:

1. **`image_cap.py`** - A Raspberry Pi-based script for capturing images and sending them to a server.
2. **`image_to_poetry.py`** - A server-side script for processing the received image, generating image labels using a pre-trained ResNet50 model, and crafting a short poem based on the detected objects.

---

## Project Workflow

1. **Image Capture and Transmission (`image_cap.py`):**
   - Runs on a Raspberry Pi.
   - Captures an image when a GPIO button is pressed.
   - Sends the image to the server using a socket connection.

2. **Image Processing and Poetry Generation (`image_to_poetry.py`):**
   - Runs on a local machine/server.
   - Receives the image via a socket.
   - Processes the image using the ResNet50 model to identify objects.
   - Uses the identified objects to generate a poem using the Gemini AI API.

---

## Setup Instructions

### Prerequisites
- Raspberry Pi with a connected camera module.
- Python 3 installed on both devices.
- Required libraries installed:
  - **On Raspberry Pi (`image_cap.py`):**
    ```bash
    pip install opencv-python RPi.GPIO
    ```
  - **On the Local Machine/Server (`image_to_poetry.py`):**
    ```bash
    pip install opencv-python pillow tensorflow numpy google-generativeai
    ```
- A valid Gemini AI API key for generating poems.

---

### Steps

#### Raspberry Pi (`image_cap.py`)
1. Connect a button to GPIO pin 10 of the Raspberry Pi.
2. Update the `SERVER_ADDRESS` variable with the IP address of the machine running `image_to_poetry.py`.
3. Run the script:
   ```bash
   python3 image_cap.py
   ```

#### Local Machine/Server (`image_to_poetry.py`)
1. Update the `GEMINI_API_KEY` with your valid Gemini AI API key.
2. Start the script:
   ```bash
   python3 image_to_poetry.py
   ```

---

## Usage
1. Press the button connected to the Raspberry Pi to capture and send an image.
2. View the generated poem in the terminal running `image_to_poetry.py`.

---

## Example Output

### Top Predicted Objects
```
1: Mountain (0.92)
2: Tree (0.88)
3: River (0.83)
4: Sky (0.78)
5: Bird (0.75)
```

### Generated Poem
```
Above the mountain high and steep,
The bird in the sky begins to leap.
By the river, where the trees bow,
Nature whispers, "Here and now."
```

---

## Notes
- Ensure both devices are connected to the same network for socket communication.
- The `GEMINI_API_KEY` must be kept secure and not shared publicly.

---

## Future Enhancements
- Add error handling for network interruptions.
- Extend support for more poetic styles and formats.
- Implement image enhancements on the Raspberry Pi before sending.

