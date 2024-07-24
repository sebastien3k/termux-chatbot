# termux-chatbot

## Overview

This project is a local chatbot application that interacts with a locally running Large Language Model (LLM) server. It includes speech-to-text (STT) integration, allowing users to receive responses audibly. 

**Note:** Due to limitations with Termux:API on android-5 variants, the current implementation focuses on text-to-speech, with future plans to integrate speech-to-text capabilities.

## Features

- **Local LLM Server Integration:** Communicates with a locally running LLM server using OpenAPI styled endpoints.
- **Text-to-Speech (TTS):** Converts the chatbot's responses to speech using `termux-tts-speak`.
- **Command-Line Configuration:** Allows users to configure model parameters and settings using `questionary` before starting the chat.

## Setup

### Prerequisites

- **Python:** Ensure Python is installed on your system.
- **Termux:** Installed on your Android device (for TTS functionality).
- **LLM Server:** A local LLM server running and accessible.

  ### Installation

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/sebastien3k/termux-chatbot
   cd termux-chatbot
   ```

2. **Install Required Packages:**

   Install the necessary Python packages using `pip`:

   ```sh
   pip install requests questionary
   ```

3. **Configure Environment Variables:**

   Create a `.env` file in the project directory to store the LLM server's IP address:

   ```env
   LLM_SERVER_IP=127.0.0.1
   ```

   Alternatively, export the environmental variable in your .bashrc file:
   ```.bashrc
   export LLM_SERVER_IP=127.0.0.1
   ```

### Usage

1. **Start the Chatbot:**

   This script will prompt you to select the model and configure the parameters:

   ```sh
   python main.py
   ```

   The script will initialize the chatbot with the configured settings and enter the chat loop. Interact with the chatbot using text input.

2. **Text-to-Speech (TTS) Integration:**

   The chatbot's responses will be spoken aloud using `termux-tts-speak`. Ensure `termux-tts-speak` is correctly installed and working on your device.

## Code Overview

### `main.py`

1. **Configuration:**

   Uses `questionary` to present a command-line interface for selecting the model and setting parameters (`temperature`, `top_p`).

2. **Send Request:**

   Sends user input to the LLM server and retrieves the response. Handles streaming responses and updates the chatbot’s state accordingly.

3. **Text-to-Speech:**

   Converts the LLM’s responses to speech using `termux-tts-speak`.

## Troubleshooting

- **LLM Server Issues:** Ensure the LLM server is correctly running and accessible. Check server logs for any errors.

## Future Plans

- **Speech-to-Text Integration:** Explore alternative solutions or updates to Termux:API for integrating speech-to-text functionality.
- **Additional Features:** Consider adding more configuration options or integrating additional features based on user feedback.
