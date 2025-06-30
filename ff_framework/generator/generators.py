from PyPDFForm import PdfWrapper
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import os
import zipfile

class PDFGenerator:
    def __init__(self, logger, database):
        self.template = "C:/Users/Joseph/source/repos/formflow-framework/form-cms1500_1.pdf"
        self.second_page_template = "C:/Users/Joseph/source/repos/formflow-framework/form-cms1500_2.pdf"
        self.logger = logger
        self.database = database

    def generate(self, directives, data):
        today = datetime.today().strftime('%Y-%m-%d')
        base_file_name = directives.get("file_name", "filled_form.pdf")
        file_path = directives.get("file_path", "filled_forms/")
        send_email = directives.get("send_email", False)
        pdf = PdfWrapper(self.template)
        self.logger.log(f"Generating PDFs with base file name: {base_file_name} and file path: {file_path}", level='info')
        for i, record in enumerate(data):
            try:
                file_name = f"{i}_{today}_{base_file_name}"
                pdf.fill(record)

                # Combine filled first page and unmodified second page
                filled_pdf = PdfReader(pdf.read())
                second_page_pdf = PdfReader(self.second_page_template)

                writer = PdfWriter()
                writer.add_page(filled_pdf.pages[0])  # filled page
                writer.add_page(second_page_pdf.pages[0])  # instruction page

                os.makedirs(file_path, exist_ok=True)
                output_path = os.path.join(file_path, f"{file_name}.pdf")

                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
            except Exception as e:
                self.logger.log(f"Error generating PDF for record {i}: {e}", level='error')
                continue 
        zip_file_path = self._zip_files(file_path, base_file_name)
        self._remove_files(file_path)
        sending_email = None
        if send_email:
            organization_id = directives.get("organization_id", None)
            if organization_id is None:
                self.logger.log("Organization ID is required to send email.", level='error')
                raise ValueError("Organization ID is required to send email.")
            sending_email = self.database.select(
                table_name="organizations",
                columns=["organization_email"],
                condition={"=": ["id", organization_id]}
            )
            if sending_email.empty:
                self.logger.log(f"No email found for organization ID {organization_id}.", level='error')
                raise ValueError(f"No email found for organization ID {organization_id}.")
            sending_email = sending_email.iloc[0]['organization_email']
        return (zip_file_path, sending_email)
        
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