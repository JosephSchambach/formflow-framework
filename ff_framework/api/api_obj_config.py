import ff_framework.api.authentication_api as auth_api
import ff_framework.api.pdf_api as pdf_api

def api_obj_config():
    data = {
        "CreateUserRegistration": {
            "parent_method": auth_api.AuthenticationAPI.register_user,
            "kwargs": {
                "attribute": "user_registration",
                "context_method": "database",
                "execution_method": "insert"
            }
        },
        "ProcessUserAuthentication": {
            "parent_method": auth_api.AuthenticationAPI.authenticate_user,
            "kwargs": {
                "attribute": "user_authentication",
                "context_method": "database",
                "execution_method": "select"
            }
        },
        "CreateConfig": {
            "parent_method": pdf_api.PDFAPI.store_config,
            "kwargs": {
                "attribute": "config",
                "context_method": "database",
                "execution_method": "insert"
            }
        },
        "GeneratePDFs": {
            "parent_method": pdf_api.PDFAPI.generate_pdf,
            "kwargs": {
                "attribute": "pdfs",
                "secondary_attribute": "config",
                "context_method": "generators",
                "execution_method": "generate"
            }
        }
    }
    return data