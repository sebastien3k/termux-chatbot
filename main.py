import subprocess

def get_response_from_llm(user_input):
    # Replace this with the actual command or API call to your local LLM
    # Here, we're just echoing the input for demonstration purposes
    response = f"Echoing: {user_input}"
    return response

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
