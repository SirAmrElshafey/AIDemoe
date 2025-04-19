import fitz  # PyMuPDF
import easyocr
from PIL import Image
import requests

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
import uuid

app = FastAPI()



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



def query_deepseek_r1( prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    data = {
        "model": "deepseek/deepseek-r1-zero:free",
        "messages": [ {"role": "user", "content": prompt},
         
        ],
      "stream": "false"  
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def process_image_with_deepseek(image_path):
    extracted_text = extract_text_from_pdf(image_path)
    prompt = f"Please analyze the following text extracted from an pdf ? return Result In JSON fromat:\n\n{extracted_text}"
    response = query_deepseek_r1(prompt)
    return response

def print_formatted_response(response_json):
    try:
        message = response_json["choices"][0]["message"]
        content = message.get("content", "")
        reasoning = message.get("reasoning", "")
        
        print("<content>")
        print(content)
        print("<content>\n")
        
        print("<reasoning>")
        print(reasoning)
        print("<reasoning>")
    except (KeyError, IndexError) as e:
        print("Invalid response format:", e)

#result = process_image_with_deepseek( './hallal.pdf')
#print_formatted_response(result)



