import geopy
from geopy.geocoders import Nominatim
import googlemaps
import cv2
import os
from deepface import DeepFace
import openai
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
from pytube import Search
import sys
import time
import re

# Set up OpenAI API Key
openai.api_key = ''  # Replace with your OpenAI API key
if not openai.api_key:
    raise ValueError("API key not found.")

# Google Maps API Key
gmaps = googlemaps.Client(key='')  # Replace with your Google Maps API key

# Initialize the recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set the voice (index 1 is often a female voice)

# Load the face detection model
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

def talk(text):
    """Convert text to speech and print the response."""
    print_response(text)  # Print the response before speaking
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for a command and return it as a string."""
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'friday' in command:
                command = command.replace('friday', '').strip()
                print(f"You said: {command}")  # Print the command
            else:
                command = ""
    except:
        pass
    return command

def print_response(response):
    """Print the response that will be spoken."""
    print(f"Friday: {response}")

def get_chatgpt_response(prompt):
    """Get a response from ChatGPT based on the provided prompt."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant for an AV taxi in Singapore.\
             You need to answer passenger's questions. Keep your answers straightforward.\
             Be helpful and respectful, do not be too formal, and provide a relaxed trip for the passenger.\
             Keep your response within 50 words.\
             Update the weather information.\
             Update the traffic information"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5
    )
    return response['choices'][0]['message']['content'].strip()

def search_youtube(query):
    search = Search(query)
    video = search.results[0]
    video_url = video.watch_url
    print(f"Playing video: {video_url}")
    webbrowser.open(video_url)

def generate_greeting_and_reminders(age, door_open):
    """Generate greeting and reminders based on age, and door status."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning, welcome aboard"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon, welcome aboard"
    else:
        greeting = "Good evening, welcome aboard"

    if age < 12:
        reminder = "Please make sure your seatbelt is fastened and your car seat is properly secured."
    elif age >= 65:
        reminder = "Please ensure your seatbelt is securely fastened and that you are comfortable."
    else:
        reminder = "Please make sure your seatbelt is fastened."

    return greeting, reminder

# Flag for door status
door_open = False
door_close = False

# Read a frame from the webcam feed
ret, frame = cap.read()
if not ret:
    raise Exception("Failed to capture image from webcam")

# Display the frame
cv2.imshow('Press "d" to Simulate Door Opening', frame)

# Check for 'd' key press to simulate door opening
key = cv2.waitKey(0) & 0xFF  # Wait for a key press
if key == ord('d'):
    print("DOOR OPENED")
    door_open = True

if door_open:
    # Wait for 2 seconds after the door is closed
    time.sleep(2)
    # Detect age
    results = DeepFace.analyze(frame, actions=['age'], enforce_detection=False)

    # If results are a list, get the first dictionary
    if isinstance(results, list):
        result = results[0]
    else:
        result = results

    age = result.get('age', "Unknown")

    # Generate a greeting and reminder
    greeting, reminder = generate_greeting_and_reminders(age, door_open)
    response = greeting + " " + " " + reminder + " " 
    talk(response)

    while door_close:
        key = cv2.waitKey(0) & 0xFF  # Wait for a key press
        if key == ord('c'):
           print("DOOR CLOSED")
           door_close = True
           talk(" Door closed. We are ready to go! My name is Friday, if you need any help, just shout out my name!")

    # Wait for 2 seconds before checking door closure
    time.sleep(2)

    # Wait for the door to be closed
    while not door_close:
        talk("Waiting for the door to close...")
        cv2.imshow('Press "c" to Simulate Door Closing', frame)
        key = cv2.waitKey(0) & 0xFF  # Wait for a key press
        if key == ord('c'):
            print("DOOR CLOSED")
            door_close = True
            talk("The door is now closed. We are ready to go! My name is Friday, if you need any help, just shout out my name!")

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

def get_current_location():
    """Get the current location based on IP address and return address details."""
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode("Singapore")  
    if location:
        address = geolocator.reverse((location.latitude, location.longitude), exactly_one=True)
        address_details = address.raw.get('address', {})
        postcode = address_details.get('postcode', 'Unknown')
        formatted_address = address_details.get('road', '') + ', ' + address_details.get('suburb', '') + ', ' + address_details.get('city', '') + ', ' + address_details.get('country', '')
        
        #print(f"Current location: Latitude {location.latitude}, Longitude {location.longitude}")
        #print(f"Address: {formatted_address}, Postcode: {postcode}")
        return location.latitude, location.longitude, formatted_address, postcode
    else:
        print("Failed to get location")
        return None, None, 'Unknown', 'Unknown'

def get_route_details(origin, destination, avoid_erp=False):
    """Get the route details using Google Maps API, optionally avoiding ERP."""
    if avoid_erp:
        directions_result = gmaps.directions(origin, destination, mode="driving", avoid=["tolls"])
    else:
        directions_result = gmaps.directions(origin, destination, mode="driving")

    if directions_result:
        distance = directions_result[0]['legs'][0]['distance']['text']
        duration = directions_result[0]['legs'][0]['duration']['text']
        return distance, duration
    else:
        print("Failed to get route details")
        return None, None

def extract_destination(command):
    """Extract the destination from the user's command."""
    patterns = [
        r"i want to go to (.+)",
        r"bring me to (.+)",
        r"take me to (.+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            destination = match.group(1).strip()
            print(f"Extracted destination: {destination}")
            return destination

    print("Destination not found")
    return None

def navigate_to_destination(command):
    """Navigate the user to their desired destination based on the command."""
    destination = extract_destination(command)
    
    if destination:
        # Get current location
        latitude, longitude, formatted_address, postcode = get_current_location()
        origin = f"{latitude}, {longitude}"

        # Get route details with and without ERP
        distance_no_erp, duration_no_erp = get_route_details(origin, destination, avoid_erp=True)
        distance_with_erp, duration_with_erp = get_route_details(origin, destination, avoid_erp=False)

               # Respond to the user
        response = (
            f"Here are the routes to {destination}:\n"
            f"Route 1: Without ERP - Distance: {distance_no_erp}, Duration: {duration_no_erp}\n"
            f"Route 2: With ERP - Distance: {distance_with_erp}, Duration: {duration_with_erp}"
        )
        talk(response)
    else:
        talk("I didn't catch that. Please repeat the destination.")

def run_Friday():
    """Process commands and perform actions."""
    command = take_command()
    if command:
        if 'play' in command:
            song = command.replace('play', '')
            if song:
                response = f'Playing {song}'
                talk(response)
                search_youtube(song)
        elif any(keyword in command for keyword in ['navigate', 'directions', 'go to', 'bring me to', 'take me to']):
            navigate_to_destination(command)
        elif 'time' in command:
            time = datetime.now().strftime('%I:%M %p')
            response = f'Current time is {time}'
            talk(response)
        elif any(exit_command in command for exit_command in ['bye', "that's all", 'stop', 'exit']):
            response = 'Goodbye! Have a good day!'
            talk(response)
            sys.exit()
        else:
            response = get_chatgpt_response(command)
            print_response(response)
            talk(response)

# Main loop
while True:
    run_Friday()

           
