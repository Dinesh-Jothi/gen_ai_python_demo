#bash code pip install PyPDF2 python-docx transformers torch nltk


# Import necessary libraries
import PyPDF2  # For extracting text from PDF files
import docx  # For extracting text from Word documents (.docx)
from transformers import AutoModelForQuestionAnswering, AutoTokenizer  # For chatbot functionality
import torch  # For deep learning
import nltk  # For natural language processing
from nltk.tokenize import word_tokenize  # Not used in this script, but imported for potential future use

# Load pre-trained model and tokenizer for question answering
model_name = "deepset/bert-base-cased-squad2"  # Model name
model = AutoModelForQuestionAnswering.from_pretrained(model_name)  # Load model
tokenizer = AutoTokenizer.from_pretrained(model_name)  # Load tokenizer

# Function to extract text from PDF files
def extract_text_from_pdf(file_path):
    """
    Extract text from PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF file.
    """
    with open(file_path, 'rb') as f:  # Open the PDF file in binary mode
        pdf_reader = PyPDF2.PdfReader(f)  # Create a PDF reader object
        text = ''  # Initialize an empty string to store the extracted text
        for page in range(len(pdf_reader.pages)):  # Iterate over each page in the PDF
            text += pdf_reader.pages[page].extract_text()  # Extract text from the page and append it to the text string
    return text  # Return the extracted text

# Function to extract text from Word documents (.docx)
def extract_text_from_docx(file_path):
    """
    Extract text from Word document (.docx).

    Args:
        file_path (str): Path to the Word document.

    Returns:
        str: Extracted text from the Word document.
    """
    doc = docx.Document(file_path)  # Create a Word document object
    text = ''  # Initialize an empty string to store the extracted text
    for para in doc.paragraphs:  # Iterate over each paragraph in the document
        text += para.text  # Extract text from the paragraph and append it to the text string
    return text  # Return the extracted text

# Function to implement chatbot functionality
# Function to implement chatbot functionality
def chatbot(query, context):
    """
    Chatbot functionality.

    Args:
        query (str): User's query.
        context (str): Context (extracted text) from the document.

    Returns:
        str: Answer to the user's query.
    """
    # Tokenize the query and context, convert to tensors
    # Crucially, pass BOTH query and context here
    inputs = tokenizer(
        query,
        context,
        return_tensors='pt',
        truncation=True,  # Important for long contexts, otherwise it will error
        padding='longest' # Ensures consistent input length
    )
    
    # Get the model's output
    # No change needed here, model receives the correctly formatted inputs
    outputs = model(**inputs, return_dict=True)
    
    # Get the start and end scores for the answer
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits
    
    # Get the start and end indices of the answer
    # You need to identify the token with the highest start/end score.
    # The [0] is important because model outputs usually come in batches,
    # even if your input has a batch size of 1.
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1
    
    # Convert the answer indices to tokens and then to a string
    # Ensure you're slicing from the input_ids that were actually processed.
    # The input_ids[0] selects the first (and only) item in the batch.
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs.input_ids[0][answer_start:answer_end]))
    
    # A common check for "no answer" or bad answers
    if answer.startswith('[CLS]') or answer.startswith('[SEP]') or answer == '':
        return "Sorry, I couldn't find a direct answer in the document."
    
    return answer

# Main function
def main():
    # Get the file path from the user
    file_path = input("Enter the file path (PDF or Word document): ")
    

    # Extract text from the file based on its type
    if file_path.endswith('.pdf'):
        context = extract_text_from_pdf(file_path)
        print(context[:500]) # Print first 500 characters to verify

    elif file_path.endswith('.docx'):
        context = extract_text_from_docx(file_path)
        print(context[:500]) # Print first 500 characters to verify

    else:
        print("Unsupported file format")
        return
    
    # Chatbot loop
    while True:
        # Get the user's query
        query = input("Ask a question: ")
        
        # Get the answer to the query
        answer = chatbot(query, context)
        
        # Print the answer
        print("Answer:", answer)

# Run the main function
if __name__ == "__main__":
    main()