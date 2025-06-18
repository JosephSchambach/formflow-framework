import ff_framework.api.authentication_api as auth_api

def api_obj_config():
    data = {
        "CreateUserRegistration": {
            "parent_method": auth_api.AuthenticationAPI.register_user,
            "kwargs": {
                "attribute": "user_registration",
                "context_method": "database",
                "execution_method": "insert"
            }
        }
    }
    return data