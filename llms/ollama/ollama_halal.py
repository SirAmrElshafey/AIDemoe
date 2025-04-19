import fitz  # PyMuPDF
import requests
import requests
import http.client
import json

def call_ollama_manual(prompt):
   # Define the connection to the local Ollama API
    conn = http.client.HTTPConnection("localhost", 11434)

    # Prepare the payload (data) to send in the request
    payload = json.dumps({
        "model": "llama3.2",
        "prompt": prompt
    })

    # Set headers for the request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    conn.request("POST", "/api/generate", body=payload, headers=headers)

    # Get the response
    response = conn.getresponse()

    # Read the response data
    response_data = response.read()

    # Log the raw response to inspect the content
    print("Raw Response Data:", response_data.decode('utf-8'))

    try:
        # Split the response into separate JSON objects (chunks)
        chunks = response_data.decode('utf-8').splitlines()
        full_response = ""

        # Process each chunk (line) and collect the responses
        for chunk in chunks:
            if chunk:  # If the chunk is not empty
                try:
                    data = json.loads(chunk)  # Try parsing each chunk
                    full_response += data.get("response", "")  # Append the response text
                    if data.get("done", False):  # Stop if the "done" field is True
                        break
                except json.JSONDecodeError as e:
                    print("Error decoding chunk:", e)

        # Return the full response as a plain string (not in chunks)
        return full_response.strip()

    except json.JSONDecodeError as e:
        return {"error": "Failed to decode JSON", "details": str(e)}

    finally:
        # Close the connection after the request is done
        conn.close()


# Example of calling the function
# result = call_ollama_manual("Hello, how are you?")
# print(result)


def extract_text_from_pdf(pdf_path):
    """
    Extracts and returns all text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

#pdf_text = extract_text_from_pdf("./hallal.pdf")
#print(pdf_text)

def call_ollama(prompt):
    # Make the request to Ollama API
    response = requests.post("http://localhost:11434/api/chat", json={
        "model": "llama3.2:1b",
        "prompt": prompt
    },stream=True)
    
    # Check if the request was successful (HTTP status 200)
    if response.status_code == 200:
        # Parse and return the response as JSON
        return response
    else:
        # Handle errors (optional)
        return {"error": "Request failed", "status_code": response.status_code}

def process_image_with_ollama(image_path):
    extracted_text = extract_text_from_pdf(image_path)
    
    prompt = f"Please analyze the following text extracted from an pdf ? return Result In JSON fromat:\n\n{extracted_text}"
    prompt2 = f"Please analyze the following text extracted from an pdf  and return fromated JSON fromat with each key and value :\n\n{extracted_text}"
    response = call_ollama_manual(prompt2)
    return response



result = process_image_with_ollama( './files/hallal.pdf')
print(result);



