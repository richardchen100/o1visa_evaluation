import requests
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
#pdf_path = os.path.join(current_dir, "CVs", "Cvitanic_Jaksa_2021.pdf")
pdf_path = os.path.join(current_dir, "CVs", "khai_cv.pdf")


url = "http://127.0.0.1:8000/upload-pdf/"
files = {"file": ("filename.pdf", open(pdf_path, "rb"), "application/pdf")}
response = requests.post(url, files=files)
print(response.json())