from pydantic import BaseModel
from typing import Optional

class PDF(BaseModel):
    form_fields: dict
    
class Config(BaseModel):
    organization_id: int
    form_name: str
    form_config: dict
    
class CreateConfig(BaseModel):
    config: Config
    
class GeneratePDFs(BaseModel):
    pdfs: list[PDF]
    config: Config
    send_email: Optional[bool] = False
    file_path: str
    file_name: str
    