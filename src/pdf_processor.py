import requests
from io import BytesIO
from pypdf import PdfReader

def download_and_extract_text(pdf_url):
    if not pdf_url:
        return ""
    response = requests.get(pdf_url)
    if response.status_code != 200:
        return ""
    reader = PdfReader(BytesIO(response.content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text