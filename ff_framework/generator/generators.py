from PyPDFForm import PdfWrapper
from datetime import datetime
import os
import zipfile

class PDFGenerator:
    def __init__(self):
        self.template = "C:/Users/Joseph/source/repos/formflow-framework/form-cms1500.pdf"

    def generate(self, directives, data):
        today = datetime.today().strftime('%Y-%m-%d')
        base_file_name = directives.get("file_name", "filled_form.pdf")
        file_path = directives.get("file_path", "filled_forms/")
        send_email = directives.get("send_email", False)
        pdf = PdfWrapper(self.template)
        for i, record in enumerate(data):
            file_name = f"{i}_{today}_{base_file_name}"
            pdf.fill(record)
            os.makedirs(file_path, exist_ok=True)
            with open(f"{file_path}{file_name}", "wb+") as output_pdf:
                output_pdf.write(pdf.read())
        zip_file_path = self._zip_files(file_path, base_file_name)
        self._remove_files(file_path)
        if send_email:
            print(f"Email sent with {len(data)} PDFs to be processed.")
            pass
        self._download_zip(zip_file_path)
        self._remove_zip(zip_file_path)
        
    def _remove_zip(self, zip_file_path):
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
            print(f"Removed zip file: {zip_file_path}")
        else:
            print(f"Zip file not found: {zip_file_path}")
        
    def _download_zip(self, zip_file_path):
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(downloads_folder, exist_ok=True)
        dest_zip_path = os.path.join(downloads_folder, os.path.basename(zip_file_path))
        os.replace(zip_file_path, dest_zip_path)
        with open(dest_zip_path, "rb") as f:
            return f.read()
        
    def _zip_files(self, file_path, base_file_name):
        zip_file_path = os.path.join(file_path, f"{base_file_name}.zip")
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(file_path):
                for file in files:
                    if file.endswith('.pdf'):
                        abs_path = os.path.join(root, file)
                        arcname = os.path.relpath(abs_path, file_path)
                        zipf.write(abs_path, arcname)
        return zip_file_path
    
    def _remove_files(self, file_path):
        for root, _, files in os.walk(file_path):
            for file in files:
                if file.endswith('.pdf'):
                    os.remove(os.path.join(root, file))
        print(f"Removed all PDF files from {file_path}.")