import easyocr
from PIL import Image
import requests

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    extracted_text = " ".join([res[1] for res in results])
    return extracted_text


def query_deepseek_r1(api_key, prompt):
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

def process_image_with_deepseek(api_key, image_path):
    extracted_text = extract_text_from_image(image_path)
    prompt = f"Please analyze the following text extracted from an image :\n\n{extracted_text}"
    response = query_deepseek_r1(api_key, prompt)
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



result = process_image_with_deepseek('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' , './bill.jpg')

print_formatted_response(result)