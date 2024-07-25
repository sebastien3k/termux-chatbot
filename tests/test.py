import os
import requests
import json
import subprocess

# Check if the LLM_SERVER_IP environment variable is set
server_ip = os.getenv('LLM_SERVER_IP')
if not server_ip:
    print("Error: LLM_SERVER_IP environment variable is not set.")
    print("Please set it using: export LLM_SERVER_IP=your_server_ip_here")
    exit(1)

# Set up the API endpoint
api_url = f"http://{server_ip}:1337/v1/chat/completions"

# Initialize conversation history
conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def send_request(message):
    conversation.append({"role": "user", "content": message})
    
    payload = {
        "messages": conversation,
        "model": "mistral-7b-instruct-v0.2.Q4_K_S",
        "stream": False,
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.95
    }
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to connect to the LLM server. {e}")
        return None

def speak_response(text):
    try:
        subprocess.run(["termux-tts-speak", text], check=True)
    except subprocess.CalledProcessError:
        print("Error: Unable to use termux-tts-speak. Make sure Termux:API is installed.")

print("Welcome to the Termux Chatbot!")
print("Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    response_data = send_request(user_input)
    
    if response_data:
        assistant_response = response_data['choices'][0]['message']['content']
        print(f"Assistant: {assistant_response}")
        speak_response(assistant_response)
        conversation.append({"role": "assistant", "content": assistant_response})
    else:
        print("Sorry, I couldn't get a response. Please try again.")
