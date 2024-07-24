import subprocess

def get_response_from_llm(message):
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
        "model": "Wizard-Vicuna-7B-Uncensored.Q5_K_M",
        "stream": True,
        "max_tokens": 2048,
        "stop": [
            "hello"
        ],
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.7,
        "top_p": 0.95
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
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        response = get_response_from_llm(user_input)
        print(f"LLM: {response}")
        
        speak_text(response)

if __name__ == "__main__":
    main()
