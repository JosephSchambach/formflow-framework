from ff_framework.context.context_logging import ContextLogger

class AuthenticationAPI:
    def __init__(self, logger: ContextLogger, database):
        self.logger = logger 
        self.database = database
        self.logger.log("AuthenticationAPI initialized successfully.", level='info')
        
    def register_user(self, attribute, context_method, execution_method):
        registration_data = getattr(self, attribute)
        columns = registration_data.__dict__.keys()
        values = [getattr(registration_data, column) for column in columns]
        return {
            "table": "user_authentication", 
            "columns": list(registration_data.__dict__.keys()), 
            "values": values, 
            "context_method": context_method, 
            "execution_method": execution_method
        }
