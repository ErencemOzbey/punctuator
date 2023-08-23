# Text Restoration API

Welcome to the Text Restoration API. This API is designed to restore punctuation and capitalization of a given text or file, ensuring that the structure and legibility of your content remain intact.

## Features

- **Punctuation Restoration**: Brings back the missing punctuation marks in your text.
- **Capitalization Restoration**: Fixes the capitalization to ensure correct sentence beginnings, proper nouns, and other contextual capitalizations.
- **GUI Support**: For a more visual and interactive usage, a Graphical User Interface is available.
- **File Input**: You can provide input in the form of files.
- **File Output**: Get the restored text as a file output.
- **Input Parsing**: The input can be parsed line by line or split according to a specific length.

## Getting Started

### Installation

1. Download and place the required files in a directory on your computer.
   
### Requirements

2. If Python isn't installed on your machine, install Python3 and pip.
3. Use pip to install the necessary dependencies: `fastapi`, `uvicorn`, `jinja2`, `starlette`, and `punctuators`.

### Execution

4. Navigate to the directory containing your files in a terminal.
5. Run the command: `uvicorn main:app --reload`.
6. Access the GUI by visiting `http://127.0.0.1:8000` in your browser.

## API Usage

There's an additional `main.py` file in the `API` directory. This is distinct from the other main file since it employs Swagger for the GUI. If you prefer using the API with Swagger, refer to this version.

## GUI Instructions

1. Open your browser and go to `http://127.0.0.1:8000`.
2. Follow the on-screen instructions to either upload your file or paste your text directly.
3. Click on the "Restore" button.
4. Review the results and download the corrected text, if desired.

## Feedback and Contribution

We value your feedback. If you encounter any issues or have suggestions, please let us know. Interested contributors can refer to our contributing guidelines (assuming there are any provided).
