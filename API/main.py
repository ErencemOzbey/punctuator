from fastapi import FastAPI, Depends
from pydantic import BaseModel
from punctuators.models import PunctCapSegModelONNX
from typing import List, Optional

import string

app = FastAPI()

m: PunctCapSegModelONNX = PunctCapSegModelONNX.from_pretrained(
    "1-800-BAD-CODE/xlm-roberta_punctuation_fullstop_truecase"
)

class TextInput(BaseModel):
    input_text: str
    split_method: Optional[str] = "line"
    split_length: Optional[int] = 0
    write_to_file: Optional[bool] = False

def preprocess_input(text: str) -> str:
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    return text

@app.post("/process/")
async def process_text(data: TextInput):
    input_text = data.input_text
    split_method = data.split_method
    split_length = data.split_length
    write_to_file = data.write_to_file

    # Preprocess the input
    input_text = preprocess_input(input_text)

    # Splitting the input text
    if split_method == "length":
        input_texts = split_string(input_text, split_length)
    else:
        input_texts = split_string2(input_text, split_length)

    results: List[List[str]] = m.infer(texts=input_texts, apply_sbd=True)

    finale = []
    for input_text, output_texts in zip(input_texts, results):
        sentences = [j for i in output_texts for j in i.split()]
        finale.append(sentences)

    output_texts = [" ".join(text) for text in finale]

    if write_to_file:
        output_filename = "output.txt"
        with open(output_filename, 'w') as f:
            for text in output_texts:
                f.write(text + "\n")
        return FileResponse(output_filename, filename=output_filename)

    return {"outputs": output_texts}

def split_string(input_string, k):
    return split_string1(input_string, k)

def split_string1(input_string, k):
    words = input_string.split()
    result = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= k:
            current_line += word + " "
        else:
            result.append(current_line.rstrip())
            current_line = word + " "
    if current_line:
        result.append(current_line.rstrip())
    return result

def split_string2(input_string, k):
    return input_string.splitlines()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
