import pdfkit
from format_text import trunc
from llama_parse import LlamaParse
import os
from dotenv import load_dotenv

load_dotenv()
llamacloud_key = os.getenv("LLAMACLOUD_KEY")


def make(title, url):
    # check if txt file already exists
    if os.path.exists(f"webscraper/pages/txts_llama/llama_{trunc(title)}.txt"):
        print(f"File {trunc(title)}.txt already exists")
        return
    # title = "Computational Science and Engineering Track"
    # url = "https://www.cs.purdue.edu/undergraduate/curriculum/track-cse-fall2023.html"

    options = {
    "disable-local-file-access": None,
    "enable-local-file-access": None,
    "print-media-type": None
    }

    if pdfkit.from_url(url, f'webscraper/pages/pdfs/{trunc(title)}.pdf', options=options):
        print("PDF created successfully")
    else:
        print("Failed to create PDF")

    parser = LlamaParse(
        api_key=llamacloud_key,
        result_type="text"
    )

    documents = parser.load_data(f'webscraper/pages/pdfs/{trunc(title)}.pdf')
    with open(f"webscraper/pages/txts_llama/{trunc(title)}.txt", 'w') as file:
        file.write(url + '\n')
        file.write(documents[0].text)