Autonomous Vehicle Assistant

This project creates an autonomous vehicle assistant that integrates conversational AI, voice processing, real-time navigation, and webcam-based interactions. The assistant, named "Friday," leverages OpenAI’s GPT-4 model to interact with passengers, provide navigation instructions, and respond to voice commands.

Features
Conversational AI: Uses OpenAI GPT-4 to handle passenger queries, providing natural and helpful responses.
Voice Command Processing: Recognizes and responds to voice commands using speech_recognition and pyttsx3 for text-to-speech.
Navigation: Integrates Google Maps API for route planning, with options to avoid tolls.
Geolocation: Retrieves current location details and addresses using geopy.
Webcam Processing: Detects faces and processes age information using OpenCV and DeepFace, simulating door status.
YouTube Integration: Searches for and plays YouTube videos based on user commands.
Installation
To set up the project, follow these steps:

Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
Install Dependencies:

Make sure you have Python 3.x installed. Then, install the required packages using pip:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables:

Create a .env file in the root directory and add your API keys:

plaintext
Copy code
OPENAI_API_KEY=your_openai_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
Usage
Run the Assistant:

Start the assistant by running the main script:

bash
Copy code
python assistant.py
Voice Commands:

The assistant listens for commands starting with "Friday." Commands include requests for navigation, playing songs, checking the time, and more.

Simulate Door Status:

The assistant simulates door opening and closing using the webcam. Press 'd' to simulate opening and 'c' to simulate closing.

Code Structure
assistant.py: Main script for running the assistant. Handles voice commands, navigation, and interactions.
requirements.txt: List of Python dependencies required for the project.
.env: Configuration file for storing API keys and other sensitive information.
Dependencies
openai: For interacting with GPT-4.
googlemaps: For route planning and navigation.
geopy: For geolocation services.
cv2 (OpenCV): For image processing and face detection.
deepface: For face analysis and age detection.
pytube: For searching and playing YouTube videos.
speech_recognition: For voice command recognition.
pyttsx3: For text-to-speech conversion.
dotenv: For managing environment variables.
Challenges & Future Work
Face Detection Accuracy: Improving the accuracy of face detection and age estimation.
Voice Command Recognition: Enhancing the robustness of voice command recognition in noisy environments.
API Rate Limits: Managing API rate limits and optimizing requests to avoid service interruptions.