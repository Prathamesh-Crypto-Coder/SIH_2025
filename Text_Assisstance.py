import os
import google.generativeai as genai

# CAUTION: For testing only. This is not a secure way to store your API key.
# Replace 'YOUR_API_KEY_HERE' with the actual key you got from Google AI Studio.
genai.configure(api_key="AIzaSyBfETlgiegFBN91IAwVY7bnJd5dtsEc4BI")

# Choose a generative model to use.
model = genai.GenerativeModel('gemini-1.5-flash')

print("Hello! I am a simple chatbot powered by Gemini. Ask me anything.")
print("Type 'exit' to end the conversation.")

# Start a new chat session to maintain context.
chat = model.start_chat(history=[])

while True:
    # Get user input from the command line.
    user_input = input("You: ")

    # Check if the user wants to exit.
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    try:
        # Send the user's message to the Gemini model and get a response.
        response = chat.send_message(user_input)
        
        # Print the chatbot's response.
        print(f"Chatbot: {response.text}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again.")
