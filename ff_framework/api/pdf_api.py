

class PDFAPI:
    def __init__(self):
        pass
        
    def store_config(self, attribute, context_method, execution_method):
        config_data = getattr(self, attribute)
        columns = list(config_data.__dict__.keys())
        values = list(config_data.__dict__.values())
        return {
            "table": "form_configs",
            "columns": columns,
            "values": values,
            "context_method": context_method,
            "execution_method": execution_method
        }
        
    def generate_pdf(self, attribute, secondary_attribute, context_method, execution_method):
        pdf_data = getattr(self, attribute)
        config_data = getattr(self, secondary_attribute)
        pdf_list = []
        pdf_form_fields = list(config_data.form_config.keys())
        for pdf in pdf_data:
            pdf_form_field_values = [pdf.form_fields[key] for key in pdf_form_fields if key in pdf.form_fields]
            pdf_field_mapping = dict(zip(pdf_form_fields, pdf_form_field_values))
            pdf_list.append(pdf_field_mapping)    
        return {
            "table": "PDFGenerator",
            "columns": {
                "file_name": self.file_name, 
                "file_path": self.file_path,
                "send_email": self.send_email
            },
            "values": pdf_list,
            "context_method": context_method,
            "execution_method": execution_method
        }