import ollama # Import the Ollama Python SDK

# --- 1. Initialize Conversation History ---
# This list will store all messages (both user and assistant) to maintain context.
# We start with a 'system' message to set the LLM's persona or instructions.
conversation_history = [
    {'role': 'system', 'content': 'You are a friendly and helpful chatbot.'}
]

# --- 2. Main Chat Loop ---
# The 'while True' loop keeps the chatbot running indefinitely until the user exits.
print("Welcome to the Ollama Chatbot!")
print("Type 'exit' or 'quit' to end the conversation.")

while True:
    # --- 3. Get User Input ---
    # Prompt the user to type their message.
    user_message = input("You: ")

    # --- 4. Handle Exit Condition ---
    # Check if the user wants to quit the chat.
    if user_message.lower() in ['exit', 'quit']:
        print("Chatbot: Goodbye! 👋")
        break # Exit the 'while' loop

    # --- 5. Add User Message to History ---
    # Append the user's current message to the 'conversation_history' list.
    # It's marked with the 'user' role.
    conversation_history.append({'role': 'user', 'content': user_message})

    # --- 6. Send Conversation to Ollama Model ---
    # Call the 'ollama.chat()' function.
    #   - 'model': Specify which LLM model you want to use (e.g., 'llama3', 'mistral').
    #     Make sure this model is downloaded and running in your local Ollama instance.
    #   - 'messages': Pass the entire 'conversation_history' list. This is how
    #     the LLM understands the context of the ongoing dialogue.
    try:
        response = ollama.chat(model='mistral', messages=conversation_history)

        # --- 7. Extract Chatbot's Reply ---
        # The response from ollama.chat() is a dictionary.
        # The actual generated text from the LLM is in response['message']['content'].
        chatbot_reply = response['message']['content']

        # --- 8. Print Chatbot's Reply ---
        print(f"Chatbot: {chatbot_reply}")

        # --- 9. Add Chatbot's Reply to History ---
        # It's crucial to also add the assistant's (chatbot's) reply to the history.
        # This ensures the model remembers what it said in previous turns.
        conversation_history.append({'role': 'assistant', 'content': chatbot_reply})

    except Exception as e:
        # --- Handle potential errors (e.g., Ollama server not running, model not found) ---
        print(f"Chatbot Error: Could not get a response. Is Ollama running and the model '{'mitral'}' available?")
        print(f"Error details: {e}")
        # Optionally, you might want to break here or offer retry options
        # For simplicity, we'll just continue the loop after an error.