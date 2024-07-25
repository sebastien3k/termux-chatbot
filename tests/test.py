import os
import requests
import json
import subprocess
import questionary

# Check for the LLM_SERVER_IP environment variable
LLM_SERVER_IP = os.getenv('LLM_SERVER_IP')
if not LLM_SERVER_IP:
    print("Error: LLM_SERVER_IP environment variable is not set.")
    print("Please set it using: export LLM_SERVER_IP=your_server_ip_here")
    exit(1)

# Set up the API endpoint
API_URL = f"http://{LLM_SERVER_IP}:1337/v1/chat/completions"

# Model options
MODEL_OPTIONS = [
    "tinyllama-1.1b",
    "mistral-7b-instruct-v0.2.Q4_K_S",
    # Add other models here
]

# Temperature options
TEMPERATURE_OPTIONS = [
    0.7,
    0.8,
    0.9,
    1.0
]

# Top_p options
TOP_P_OPTIONS = [
    0.95,
    0.9,
    0.85,
    0.8
]

def configure_chat():
    model = questionary.select(
        "Choose a model:",
        choices=MODEL_OPTIONS
    ).ask()

    temperature = questionary.select(
        "Choose a temperature:",
        choices=[str(t) for t in TEMPERATURE_OPTIONS]
    ).ask()

    top_p = questionary.select(
        "Choose a top_p value:",
        choices=[str(p) for p in TOP_P_OPTIONS]
    ).ask()

    return {
        "model": model,
        "temperature": float(temperature),
        "top_p": float(top_p)
    }

def send_message(message, config):
    conversation.append({"role": "user", "content": message})
    
    payload = {
        "messages": conversation,
        "model": config["model"],
        "stream": False,
        "max_tokens": 2048,
        "temperature": config["temperature"],
        "top_p": config["top_p"]
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the server: {e}")
        return None

def speak_text(text):
    try:
        subprocess.run(["termux-tts-speak", text], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to run termux-tts-speak. Make sure Termux:API is installed.")

def main():
    print("Welcome to the Termux Chatbot!")
    config = configure_chat()
    print(f"Using model: {config['model']}, temperature: {config['temperature']}, top_p: {config['top_p']}")
    print("Type 'exit' to end the conversation.")
    
    global conversation
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = send_message(user_input, config)
        if response:
            print("Assistant:", response)
            speak_text(response)
            conversation.append({"role": "assistant", "content": response})
        else:
            print("Failed to get a response. Please try again.")

if __name__ == "__main__":
    main()
