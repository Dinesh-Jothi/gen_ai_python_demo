import google.generativeai as genai # Import the Google Generative AI SDK
import os # For securely accessing environment variables
#pip install google-generativeai

# --- 1. Configure the Gemini API Key ---
# This step authenticates your application with Google's services.
# It's best practice to load the API key from an environment variable.
try:
 #   API_KEY = os.environ.get("GOOGLE_API_KEY")
    API_KEY = '***'
   
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=API_KEY)
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    print("You can get a key from: https://aistudio.google.com/app/apikey")
    exit() # Exit the script if we can't configure the API key

# --- 2. Initialize the Generative Model ---
# We specify the model to use. 'gemini-pro' is a good choice for text-only tasks.
# For multimodal (text + image) tasks, you might use 'gemini-pro-vision'.
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 3. Main Chat Loop ---
# This loop keeps the chatbot running, allowing you to ask multiple questions.
print("Welcome to the Google Gemini API Chatbot (Single Turn Mode)!")
print("Type 'exit' or 'quit' to end the conversation.")

while True:
    # --- 4. Get User Input ---
    # Prompt the user for their question.
    question = input("Ask something (or type 'exit' to quit): ")

    # --- 5. Handle Exit Condition ---
    # Check if the user wants to quit the chat.
    if question.lower() in ['exit', 'quit']:
        print("Goodbye! 👋")
        break # Exit the loop if the user types 'exit' or 'quit'

    # --- 6. Send Prompt to Gemini Model ---
    # Use the 'model.generate_content()' method for single-turn requests.
    # We use a try-except block to catch potential network or API errors.
    try:
        response = model.generate_content(question)

        # --- 7. Extract and Print Model's Answer ---
        # The generated text is found in the 'text' attribute of the response object.
        print("Answer:", response.text)

    except Exception as e:
        # --- 8. Error Handling ---
        # If something goes wrong (e.g., no internet, API error, rate limit exceeded),
        # an exception is caught and an error message is printed.
        print(f"Chatbot Error: Could not get a response from Gemini. Please check your API key, network connection, or usage limits.")
        print(f"Error details: {e}")
        # The loop will continue, allowing the user to try again.