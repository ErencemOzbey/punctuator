from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles
from typing import List, Optional
from punctuators.models import PunctCapSegModelONNX
import string

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

m: PunctCapSegModelONNX = PunctCapSegModelONNX.from_pretrained(
    "1-800-BAD-CODE/xlm-roberta_punctuation_fullstop_truecase"
)
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
def preprocess_input(text: str) -> str:
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    return text

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def process_text(request: Request, input_text: Optional[str] = Form(None), input_file: UploadFile = File(None), split_method: str = Form("line"), split_length: int = Form(0), write_to_file: bool = Form(False)):
    if not input_text and input_file:
        input_text_content = await input_file.read()
        input_text = input_text_content.decode()

    # Preprocess the input
    input_text = preprocess_input(input_text)

    if split_method == "length":
        input_texts = split_string(input_text, split_length)
    else:
        input_texts = split_string2(input_text, split_length)

    results: List[List[str]] = m.infer(texts=input_texts, apply_sbd=True)

    finale = []
    count_of_output = 0
    for input_text, output_texts in zip(input_texts, results):
        sentences = []
        for i in output_texts:
            for j in i.split():
                sentences.append(j)
                count_of_output += 1
        finale.append(sentences)

    output_texts = [" ".join(text) for text in finale]

    if write_to_file:
        output_filename = "output.txt"
        with open(output_filename, 'w') as f:
            for text in output_texts:
                f.write(text + "\n")
        return FileResponse(output_filename, filename=output_filename)

    return templates.TemplateResponse("form.html", {"request": request, "input": input_text, "outputs": output_texts})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

