import os
import requests
import json
import subprocess
import questionary

# Function to display the configuration UI
def configure_chatbot():
    # Model selection
    model = questionary.select(
        "Select the model:",
        choices=[
            "mistral-7b-instruct-v0.2.Q4_K_S",
            "Wizard-Vicuna-7B-Uncensored.Q5_K_M"
        ]
    ).ask()

    # Temperature selection
    temperature = questionary.select(
        "Select the temperature:",
        choices=[
            ("0.1 - Very deterministic", "0.1"),
            ("0.5 - Balanced", "0.5"),
            ("0.9 - Creative", "0.9")
        ],
        default="0.7"
    ).ask()

    # Top-p selection
    top_p = questionary.select(
        "Select the top-p (nucleus sampling):",
        choices=[
            ("0.1 - Very focused", "0.1"),
            ("0.5 - Balanced", "0.5"),
            ("0.9 - More diverse", "0.9")
        ],
        default="0.9"
    ).ask()

    # Save the configuration to a file
    config = {
        'model': model,
        'temperature': float(temperature),
        'top_p': float(top_p)
    }

    # with open('config.json', 'w') as f:
    #     json.dump(config, f)

    # print("Configuration saved.")
    return config

# Function to load configuration from file
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
    else:
        return configure_chatbot()

# Function to get response from llm server
def get_response_from_llm(message, config):
    # Get the server IP from the environment variable
    server_ip = os.getenv('LLM_SERVER_IP')
    if not server_ip:
        raise EnvironmentError("LLM_SERVER_IP environment variable is not set.")
    
    url = f'http://{server_ip}:1337/v1/chat/completions'
    # Example cURL request data
    data = {
        "messages": [
            {
                "content": "You are an helpful assistant your primary goal is helping with whatever the user requests. ",
                "role": "system"
            },
            {
                "content": message,
                "role": "user"
            }
        ],
        "model": config['model']
        "stream": True,
        "max_tokens": 2048,
        "stop": [
            "hello"
        ],
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": config['temperature'],
        "top_p": config['top_p']
    }

    # Send POST request to LLM API server
    try:
        response = requests.post(url, json=data, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Initialize an empty string to hold the complete message
            complete_message = ""

            # Parse response chunks
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        # Decode the chunk and extract the message
                        decoded_chunk = chunk.decode('utf-8').replace('data: ', '')
                        data = json.loads(decoded_chunk)
                        
                        if "choices" in data:
                            choices = data["choices"]
                            for choice in choices:
                                message = choice.get("delta", {}).get("content")
                                complete_message += message + ""

                    except json.JSONDecodeError as e:
                        # Ignore non-JSON chunks
                        pass
        
            # Print the complete message
            return complete_message.strip()

        else:
            print(f"Failed to generate response from LLM API server. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LLM API server: {e}")

def speak_text(text):
    command = f'termux-tts-speak "{text}"'
    subprocess.run(command, shell=True)

def main():
    print("Welcome to the LLM Chatbot. Type 'exit' to quit.")
    config = configure_chatbot()
    print("Configuration loaded.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        response = get_response_from_llm(user_input, config)
        print(f"LLM: {response}")
        
        speak_text(response)

if __name__ == "__main__":
    main()
