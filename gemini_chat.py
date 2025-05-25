import google.generativeai as genai # Import the Google Generative AI SDK
import os # To access environment variables securely

# --- 1. Configure the Gemini API Key ---
# This is crucial for authenticating your requests with Google's API.
# We fetch the API key from an environment variable named GOOGLE_API_KEY.
try:
  #  API_KEY = os.environ.get("GOOGLE_API_KEY")
    API_KEY = '*******8'

    if not API_KEY:
        # If the environment variable isn't set, we'll stop the program and inform the user.
        raise ValueError("GOOGLE_API_KEY environment variable not found.")
    genai.configure(api_key=API_KEY)
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    print("You can get a key from: https://aistudio.google.com/app/apikey")
    exit() # Exit if we can't configure the API key

# --- 2. Initialize the Generative Model ---
# We create an instance of the GenerativeModel.
# 'gemini-pro' is a great general-purpose model for text conversations.
# If you encounter a '404 not found' error, try 'gemini-1.5-flash' instead,
# as model availability can vary by region and access.
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 3. Start a Chat Session ---
# This creates a 'chat' object that automatically manages the conversation history.
# We start with an empty history. Gemini automatically handles the 'user' and 'model' roles.
chat = model.start_chat(history=[])

# --- 4. Main Chat Loop ---
# This loop keeps our chatbot running indefinitely, allowing for a continuous conversation.
print("Welcome to the Google Gemini API Chatbot (Multi-Turn Mode)!")
print("Type 'exit' or 'quit' to end the conversation.")

while True:
    # --- 5. Get User Input ---
    # Prompt the user to type their message for the current turn.
    user_message = input("You: ")

    # --- 6. Handle Exit Condition ---
    # Check if the user wants to quit the chatbot.
    if user_message.lower() in ['exit', 'quit']:
        print("Chatbot: Goodbye! 👋")
        break # Exit the 'while' loop

    # --- 7. Send User Message and Get Reply ---
    # We use a try-except block to gracefully handle any potential errors
    # during the API call (e.g., network issues, API limits, invalid input).
    try:
        # The 'chat.send_message()' method sends the user's message.
        # The Gemini API automatically appends this to the conversation history
        # and generates a response based on the full context.
        response = chat.send_message(user_message)

        # --- 8. Extract Chatbot's Reply ---
        # The generated text from the model is found in the 'text' attribute of the response object.
        chatbot_reply = response.text

        # --- 9. Print Chatbot's Reply ---
        print(f"Chatbot: {chatbot_reply}")

        # The 'chat' object automatically updates its internal history after each 'send_message' call,
        # so you don't need to manually add the user's or assistant's messages to a separate list.

    except Exception as e:
        # --- 10. Error Reporting ---
        # If an error occurs, print a helpful message and the error details.
        print(f"Chatbot Error: Failed to get a response from Gemini.")
        print(f"Please check your internet connection, API key, or model availability.")
        print(f"Error details: {e}")
        # The loop will continue, allowing the user to try another question.