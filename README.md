# Self-Driving Car Assistant

Welcome to the Self-Driving Car Assistant project! This repository contains code for an intelligent assistant for autonomous vehicles, designed to interact with passengers, manage navigation, and respond to various commands. 

## Features

- **Voice Commands**: The assistant can recognize and process voice commands for various tasks.
- **Face Detection and Age Recognition**: Uses a webcam to detect faces and estimate age for personalized greetings and reminders.
- **Navigation**: Provides driving directions using Google Maps API, with options to avoid ERP (Electronic Road Pricing) where applicable.
- **YouTube Integration**: Can search and play YouTube videos based on user requests.
- **Text-to-Speech**: Converts text responses into speech to interact with passengers.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/self-driving-car-assistant.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd self-driving-car-assistant
    ```

3. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**

    Create a `.env` file in the project directory and add your API keys:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_MAPS_API_KEY=your_google_maps_api_key
    ```

## Usage

1. **Run the application:**

    ```bash
    python main.py
    ```

2. **Interact with the assistant:**

    - **Voice Commands**: Speak commands like "Play a song" or "Navigate to Ngee Ann Poly".
    - **Text Commands**: Type commands and get responses via the terminal.

## Key Components

- **`main.py`**: Main script that runs the assistant, handles voice and text commands, and integrates various features.
- **`requirements.txt`**: Lists the necessary Python packages for the project.
- **`.env`**: Contains environment variables for API keys.

## Dependencies

The project relies on the following Python packages:

- `openai`
- `googlemaps`
- `geopy`
- `opencv-python`
- `deepface`
- `pytube`
- `SpeechRecognition`
- `pyttsx3`
- `python-dotenv`

Install these packages using:

```bash
pip install -r requirements.txt

