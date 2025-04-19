from PIL import Image
import pytesseract
import requests


def perform_ocr(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def call_ollama(prompt):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt
    })
    return response.json()

image_text = perform_ocr("./bill.png")
result = call_ollama(f"Please analyze this text:\n\n{image_text}")
print(result["response"])
